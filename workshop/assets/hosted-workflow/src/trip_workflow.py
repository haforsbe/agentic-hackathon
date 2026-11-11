import asyncio
from datetime import date, datetime, timezone
import json
import logging
from pathlib import Path
import re
from typing import Any, Literal, Never

from agent_framework import (
    Content, Executor, FileCheckpointStorage, WorkflowBuilder, WorkflowContext, handler, response_handler,
)
from azure.core.exceptions import AzureError
from openai import APIConnectionError, APIError, APITimeoutError
from opentelemetry import trace
from pydantic import BaseModel, ConfigDict, Field, model_validator

from workflow_config import load_config


CONFIG = load_config()
NAME = CONFIG.workflow_name
ENDPOINT = CONFIG.project_endpoint
SPECIALISTS = {
    "weather": (CONFIG.weather.agent_name, CONFIG.weather.version, CONFIG.weather.tool_name, "Answer"),
    "culture": (CONFIG.culture.agent_name, CONFIG.culture.version, CONFIG.culture.tool_name, "Guidance"),
}
SERVER_LABELS = {"weather": CONFIG.weather.server_label, "culture": CONFIG.culture.server_label}
tracer = trace.get_tracer(NAME)
logger = logging.getLogger(NAME)


class ApprovalStateMismatch(ValueError):
    """A final summary must not contradict a resolved native tool decision."""

    def __init__(self, message: str):
        super().__init__(message)
        self.evidence: dict[str, Any] | None = None


_PENDING_APPROVAL = re.compile(
    r"(?:^|[.!?]\s+)\s*(?:[-*]\s+)?(?:"
    r"(?:i(?:\s+am|['\u2019]m)|we(?:\s+are|['\u2019]re))\s+(?:still\s+)?"
    r"(?:waiting\s+for|awaiting)\s+(?:(?:your|separate|explicit|human|tool)\s+)*approval\b"
    r"|(?:this\s+(?:tool\s+)?(?:call|request)|(?:human|tool)\s+approval)\s+"
    r"(?:is\s+)?(?:still\s+)?(?:pending|awaiting\s+(?:human\s+)?approval)\b"
    r"|(?:status:\s*)?(?:awaiting|pending)\s+(?:separate\s+)?human\s+approval\b"
    r")",
    re.I | re.M,
)


def validate_final_approval_narrative(*values: str) -> None:
    if any(_PENDING_APPROVAL.search(value) for value in values):
        raise ApprovalStateMismatch("Final summary contradicts the resolved native tool approval")


class Trip(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    destination: Literal["New York, NY"]
    museum: Literal["Metropolitan Museum of Art"]
    visit_date: str

    @model_validator(mode="after")
    def validate_date(self):
        days = (date.fromisoformat(self.visit_date) - datetime.now(timezone.utc).date()).days
        if not 0 <= days <= 6:
            raise ValueError("Visit date must be within the next six days; provider coverage is verified separately")
        return self


class Evidence(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    schema_version: Literal["1"] = "1"
    domain: Literal["weather", "culture"]
    status: Literal["ok", "denied", "failed"]
    agent_name: str
    agent_version: str
    response_id: str | None
    requested_trip: Trip
    findings: str
    source: str
    uncertainty: str
    tool_name: str
    tool_arguments: dict[str, Any]
    source_evidence: str
    retrieved_at: str
    missing_information: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_origin(self):
        name, version, tool, _ = SPECIALISTS[self.domain]
        if (self.agent_name, self.agent_version, self.tool_name) != (name, version, tool):
            raise ValueError("Specialist origin or tool contract mismatch")
        if not self.uncertainty.strip():
            raise ValueError("Explicit uncertainty is required")
        if self.status == "ok" and (
            not self.response_id or not self.response_id.startswith("resp_")
            or not self.findings.strip() or not self.source.strip() or not self.source_evidence.strip()
        ):
            raise ValueError("Successful results require actual response and source evidence")
        if self.status in ("ok", "denied"):
            validate_final_approval_narrative(self.findings, self.source, self.uncertainty)
        return self


def atomic_json(path: Path, value: Any) -> None:
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, indent=2), encoding="utf-8")
    temporary.replace(path)


def sections(text: str, first: str) -> dict[str, str]:
    matches = list(re.finditer(r"(?m)^\s*(?:#{1,6}[ \t]+)?(?:\*\*)?(Answer|Guidance|Source|Uncertainty)(?:\*\*)?\s*:?\s*$", text))
    if [match.group(1) for match in matches] != [first, "Source", "Uncertainty"]:
        raise ValueError("Specialist reply does not match the observed three-section contract")
    return {
        match.group(1): text[match.end():matches[index + 1].start() if index + 1 < len(matches) else None].strip()
        for index, match in enumerate(matches)
    }


def result_evidence(domain: str, trip: dict, body: dict, pending: dict, approved: bool) -> dict:
    name, version, tool, first = SPECIALISTS[domain]
    reference = body["agent_reference"]
    if reference["name"] != name or reference["version"] != version or body["status"] != "completed":
        raise ValueError("Unexpected specialist version or incomplete response")
    text = "\n".join(
        part["text"] for item in body["output"] if item["type"] == "message"
        for part in item["content"] if part["type"] == "output_text"
    )
    parts = sections(text, first)
    calls = [item for item in body["output"] if item["type"] == "mcp_call"]
    if approved:
        if len(calls) != 1:
            raise ValueError("Exactly one independently approved completed tool result is required")
        call = calls[0]
        if (call["name"] != tool or call["server_label"] != pending["server_label"]
                or call["approval_request_id"] != pending["approval_request_id"]
                or json.loads(call["arguments"]) != pending["arguments"]
                or call["status"] != "completed" or call.get("error")):
            raise ValueError("Tool result does not match the exact approved request")
        source_evidence = call["output"]
    else:
        if calls:
            raise ValueError("A denied request unexpectedly executed a tool")
        source_evidence = ""
    fields = dict(
        domain=domain,
        agent_name=name, agent_version=version, response_id=body["id"],
        requested_trip=Trip.model_validate(trip), findings=parts[first], source=parts["Source"],
        uncertainty=parts["Uncertainty"], tool_name=tool, tool_arguments=pending["arguments"],
        source_evidence=source_evidence, retrieved_at=datetime.now(timezone.utc).isoformat(),
        missing_information=[] if approved else ["Tool execution was denied; no replacement evidence"],
    )
    try:
        validate_final_approval_narrative(parts[first], parts["Source"], parts["Uncertainty"])
    except ApprovalStateMismatch as error:
        fields.update(
            findings="",
            source=parts["Source"] if approved and not _PENDING_APPROVAL.search(parts["Source"]) else "",
            uncertainty=(
                parts["Uncertainty"] + " "
                if not _PENDING_APPROVAL.search(parts["Uncertainty"]) else ""
            ) + "Final specialist summary rejected: it contradicts the resolved native tool decision.",
            missing_information=["No usable final summary; no replacement facts or retry were generated"],
        )
        error.evidence = Evidence(status="failed", **fields).model_dump()
        raise
    return Evidence(status="ok" if approved else "denied", **fields).model_dump()


class NativeInvoker:
    def __init__(self, project, folder: Path):
        self.project = project
        self.path = folder / "requests.json"
        self.journal = json.loads(self.path.read_text()) if self.path.exists() else {}

    def __call__(self, domain: str, trip: dict, pending: dict | None, approved: bool | None) -> dict:
        name, version, _, _ = SPECIALISTS[domain]
        key = domain + ("-" + pending["approval_request_id"] if pending else "-initial")
        previous = self.journal.get(key)
        if previous:
            if previous.get("body"):
                return previous["body"]
            raise RuntimeError("An earlier request may have reached the service; reconcile instead of retrying")
        if len(self.journal) >= 4:
            raise RuntimeError("Four-response per-trip allowance exhausted")
        self.journal[key] = {"state": "creation-or-response-started-do-not-repeat"}
        atomic_json(self.path, self.journal)
        with self.project.get_openai_client(agent_name=name, max_retries=0, timeout=60) as client:
            if pending:
                request = {
                    "previous_response_id": pending["response_id"],
                    "input": [{"type": "mcp_approval_response",
                               "approval_request_id": pending["approval_request_id"], "approve": approved}],
                }
            else:
                try:
                    conversation = client.conversations.create()
                except APIError as error:
                    raise RuntimeError("Uncertain Conversation creation; reconcile instead of recreating") from error
                self.journal[key]["conversation_id"] = conversation.id
                atomic_json(self.path, self.journal)
                prompt = (
                    f"For {trip['visit_date']}, give a concise forecast for the Metropolitan Museum of Art "
                    "area, New York, NY, at latitude 40.7794, longitude -73.9632. Use those coordinates, "
                    "weather_forecast only. Preserve actual "
                    "forecast dates, source and uncertainty."
                    if domain == "weather" else
                    "Find a visitor guide for the Metropolitan Museum of Art, New York, US. "
                    "Use find_museum_guide with query Metropolitan Museum of Art, city New York, country US. "
                    "Preserve guide URLs, verification dates and uncertainty."
                )
                prompt += (
                    " Before the native tool decision, pause for separate human approval. "
                    "After the actual native approval and a completed tool call, give the final "
                    "findings from that result; do not claim approval is still pending. "
                    "If the native decision denies the call, report the denial and missing evidence. "
                    "Prose is never an approval, and no retry or replacement tool is authorized."
                )
                request = {"conversation": conversation.id, "input": prompt}
            self.journal[key]["state"] = "response-started-do-not-repeat"
            atomic_json(self.path, self.journal)
            try:
                response = client.responses.create(**request, store=True, max_output_tokens=500)
            except (APIConnectionError, APITimeoutError) as error:
                raise RuntimeError("Ambiguous response attempt; reconcile the journal before continuing") from error
            body = response.to_dict()
            if any(item["type"] == "memory_search_call" and item.get("memories")
                   for item in body["output"]):
                self.journal[key].update(response_id=response.id, state="blocked-unexpected-memory",
                                         usage=body.get("usage"))
                atomic_json(self.path, self.journal)
                raise RuntimeError("Unexpected memory; contents were not persisted and the run is stopped")
            self.journal[key].update(response_id=response.id, body=body, state="recorded")
            atomic_json(self.path, self.journal)
        if (body["agent_reference"]["name"], body["agent_reference"]["version"]) != (name, version):
            raise ValueError("Stable endpoint served an unexpected specialist version")
        return body


class Specialist(Executor):
    def __init__(self, domain, invoke, *, chat=False, invoker_factory=None):
        super().__init__(id=domain)
        self.domain = domain
        self.invoke = invoke
        self.chat = chat
        self.invoker_factory = invoker_factory

    @handler
    async def research(self, state: dict, ctx: WorkflowContext[dict, Content]) -> None:
        if self.chat and "clarification" in state:
            await ctx.yield_output(Content.from_text(state["clarification"]))
            return
        await self.advance(state, None, None, ctx)

    @response_handler
    async def chat_decision(self, original: Content, response: Content,
                            ctx: WorkflowContext[dict]) -> None:
        if (not self.chat or original.type != "function_approval_request"
                or response.type != "function_approval_response"
                or response.id != original.id or type(response.approved) is not bool
                or response.function_call.to_dict() != original.function_call.to_dict()):
            raise ValueError("Approval must match the stored native request")
        saved = original.additional_properties
        await self.advance(saved["state"], saved["pending"], response.approved, ctx)

    @response_handler
    async def decision(self, original: dict, response: dict, ctx: WorkflowContext[dict]) -> None:
        pending = original["pending"]
        keys = ("response_id", "approval_request_id", "server_label", "tool_name", "arguments")
        if (any(response.get(key) != pending[key] for key in keys)
                or type(response.get("approve")) is not bool):
            raise ValueError("Approval must match the exact native request, arguments and response")
        await self.advance(original["state"], pending, response["approve"], ctx)

    async def advance(self, state, pending, approved, ctx):
        with tracer.start_as_current_span("specialist." + self.domain) as span:
            span.set_attribute("workflow.run_id", state["run_id"])
            try:
                invoke = self.invoker_factory(state["run_id"]) if self.invoker_factory else self.invoke
                body = await asyncio.to_thread(invoke, self.domain, state["trip"], pending, approved)
                requests = [item for item in body["output"] if item["type"] == "mcp_approval_request"]
                if requests:
                    if pending or len(requests) != 1 or any(
                        item["type"] == "mcp_call" for item in body["output"]
                    ):
                        raise ValueError("Unexpected additional request or unapproved execution")
                    item = requests[0]
                    name, _, tool, _ = SPECIALISTS[self.domain]
                    if item["name"] != tool or item["server_label"] != SERVER_LABELS[self.domain]:
                        raise ValueError("Unexpected native tool")
                    observed = {
                        "response_id": body["id"], "approval_request_id": item["id"],
                        "server_label": item["server_label"], "tool_name": item["name"],
                        "arguments": json.loads(item["arguments"]),
                    }
                    if self.chat:
                        call = Content.from_function_call(
                            item["id"], item["name"], arguments=observed["arguments"],
                            server_name=item["server_label"],
                        )
                        await ctx.request_info(
                            Content.from_function_approval_request(
                                item["id"], call,
                                additional_properties={"state": state, "pending": observed},
                            ),
                            Content, request_id=item["id"],
                        )
                    else:
                        await ctx.request_info(
                            {"state": state, "pending": observed}, dict, request_id=item["id"],
                        )
                    return
                if not pending:
                    raise ValueError("Specialist did not request its required evidence tool")
                with tracer.start_as_current_span("validate." + self.domain):
                    evidence = result_evidence(self.domain, state["trip"], body, pending, approved)
            except (APIError, AzureError, TimeoutError, ValueError) as error:
                span.record_exception(error)
                logger.warning("Specialist %s failed contract or execution validation (%s)",
                               self.domain, type(error).__name__)
                name, version, tool, _ = SPECIALISTS[self.domain]
                if isinstance(error, ApprovalStateMismatch) and error.evidence is not None:
                    evidence = error.evidence
                else:
                    evidence = Evidence(
                        domain=self.domain, status="failed", agent_name=name, agent_version=version,
                        response_id=None, requested_trip=Trip.model_validate(state["trip"]),
                        findings="", source="",
                        uncertainty=f"Unavailable specialist evidence: {type(error).__name__}",
                        tool_name=tool, tool_arguments={}, source_evidence="",
                        retrieved_at=datetime.now(timezone.utc).isoformat(),
                        missing_information=["Specialist failed; no replacement facts were generated"],
                    ).model_dump()
            state["findings"][self.domain] = evidence
            await ctx.send_message(state)


class Assemble(Executor):
    def __init__(self, *, chat=False):
        super().__init__(id="assemble")
        self.chat = chat

    @handler
    async def assemble(self, state: dict, ctx: WorkflowContext[Never, dict | Content]) -> None:
        with tracer.start_as_current_span("validate-and-assemble") as span:
            span.set_attribute("workflow.run_id", state["run_id"])
            if set(state["findings"]) != {"weather", "culture"}:
                raise ValueError("Both independently invoked specialist outcomes are required")
            results = {key: Evidence.model_validate(value).model_dump()
                       for key, value in state["findings"].items()}
            result = {
                "schema_version": "1", "run_id": state["run_id"], "trip": state["trip"],
                "status": "completed" if all(value["status"] == "ok" for value in results.values()) else "partial",
                "specialists": results,
                "limits": "Only specialist evidence is assembled. Catalogue dates and forecast coverage "
                          "remain subject to the preserved source and uncertainty; no live availability is invented.",
            }
            await ctx.yield_output(Content.from_text(itinerary_text(result)) if self.chat else result)


def itinerary_text(result: dict) -> str:
    trip = result["trip"]
    parts = [f"# {trip['museum']} visit: {trip['visit_date']}",
             f"Destination: {trip['destination']}. Workflow result: {result['status']}."]
    for domain, item in result["specialists"].items():
        evidence = Evidence.model_validate(item).model_dump()
        findings = evidence["findings"] if evidence["status"] == "ok" else "No usable specialist summary available."
        source = evidence["source"] if evidence["source_evidence"] and evidence["source"] else "No verified source available."
        parts.append(
            f"## {'Weather' if domain == 'weather' else 'Cultural guide'} ({evidence['status']})\n"
            f"{findings}\n\n"
            f"Source: {source}\n\n"
            f"Uncertainty: {evidence['uncertainty']}\n\n"
            f"Missing information: {'; '.join(evidence['missing_information']) or 'None reported.'}\n\n"
            f"Agent: {evidence['agent_name']} v{evidence['agent_version']}. "
            f"Response: {evidence['response_id'] or 'unavailable'}."
        )
    parts.extend([result["limits"], f"Workflow run: {result['run_id']}"])
    return "\n\n".join(parts)


def build(invoke=None, storage=None, *, chat=False, invoker_factory=None):
    weather = Specialist("weather", invoke, chat=chat, invoker_factory=invoker_factory)
    culture = Specialist("culture", invoke, chat=chat, invoker_factory=invoker_factory)
    assemble = Assemble(chat=chat)
    return WorkflowBuilder(
        start_executor=weather, max_iterations=10, name=NAME, checkpoint_storage=storage,
    ).add_chain([weather, culture, assemble]).build()


async def execute_request(folder: Path, data: dict, invoke) -> dict:
    storage = FileCheckpointStorage(folder / "checkpoints")
    workflow = build(invoke, storage)
    if "trip" in data:
        if (folder / "started.json").exists():
            raise ValueError("This session already started; inspect status or resume its exact approval")
        trip = Trip.model_validate(data["trip"]).model_dump()
        state = {"run_id": folder.name, "trip": trip, "findings": {}}
        atomic_json(folder / "started.json", state)
        result = await workflow.run(state, include_status_events=True)
    elif "approval" in data:
        previous = json.loads((folder / "result.json").read_text())
        if previous["status"] != "awaiting_approval":
            raise ValueError("No approval is pending")
        result = await workflow.run(
            responses={previous["request_id"]: data["approval"]},
            checkpoint_id=previous["checkpoint_id"], checkpoint_storage=storage,
            include_status_events=True,
        )
    else:
        raise ValueError("Supply a trip or the exact pending approval")
    checkpoints = await storage.list_checkpoints(workflow_name=NAME)
    referenced = {item.previous_checkpoint_id for item in checkpoints}
    leaves = [item for item in checkpoints if item.checkpoint_id not in referenced]
    if len(leaves) != 1:
        raise ValueError("Ambiguous workflow checkpoint lineage; stop instead of replaying")
    pending = result.get_request_info_events()
    if pending:
        if len(pending) != 1:
            raise ValueError("Exactly one human tool decision must be handled at a time")
        event = pending[0]
        value = {"status": "awaiting_approval", "run_id": folder.name,
                 "request_id": event.request_id, "approval": event.data["pending"],
                 "checkpoint_id": leaves[0].checkpoint_id}
    else:
        outputs = result.get_outputs()
        if len(outputs) != 1:
            raise ValueError("Workflow produced no unique validated result")
        value = outputs[0]
    atomic_json(folder / "result.json", value)
    return value
