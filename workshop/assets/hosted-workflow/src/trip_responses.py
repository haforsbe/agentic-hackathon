import json
import logging
import re
import uuid
from typing import get_args

from agent_framework_foundry_hosting import HostedResponseRequest, WorkflowTurn
from azure.ai.agentserver.responses.models import IncludeEnum

from trip_workflow import NAME, Trip


logger = logging.getLogger("two-specialist-workflow")
INCLUDE_SELECTORS = frozenset(get_args(IncludeEnum))


def prepare_options(request: HostedResponseRequest, options: dict) -> dict:
    # Labels and include selectors belong to the outer host, never to specialists.
    unsupported = set(options) - {"model", "metadata", "include"}
    if unsupported:
        logger.warning("Unsupported workflow caller options")
        raise ValueError("Caller model, tool, instruction and runtime overrides are not supported")
    include = options.get("include")
    if include is not None and (
        not isinstance(include, list)
        or any(not isinstance(item, str) or item not in INCLUDE_SELECTORS for item in include)
    ):
        logger.warning("Rejected Responses include projection")
        raise ValueError("include must be a list of SDK-supported outer response data selectors")
    if options.get("model") not in (None, "", NAME):
        logger.warning("Rejected Responses workflow model label override")
        raise ValueError("The workflow model label cannot select another agent or deployment")
    if request.request.get("store") is False or request.request.get("background") is True:
        logger.warning("Rejected Responses storage or background override")
        raise ValueError("Use stored foreground Responses for exact human approval continuation")
    return {}


async def parse_response(request: HostedResponseRequest) -> WorkflowTurn[dict]:
    items = await request.get_input_items()
    if any(item.get("type") == "mcp_approval_response" for item in items):
        if any(set(item) - {"type", "approval_request_id", "approve", "id"} for item in items):
            raise ValueError("Only the exact pending approval ID and boolean decision are accepted")
        return WorkflowTurn(responses=await request.get_workflow_responses())
    if any(item.get("type") not in ("message",) or item.get("role") != "user" for item in items):
        raise ValueError("Supply user trip text or the exact pending MCP approval response")
    text = (await request.get_input_text() or "").strip()
    trip = None
    if text.startswith("{"):
        try:
            trip = Trip.model_validate(json.loads(text)).model_dump()
        except (ValueError, json.JSONDecodeError):
            trip = None
    else:
        dates = re.findall(r"\b\d{4}-\d{2}-\d{2}\b", text)
        if (len(dates) == 1 and re.search(r"\bNew York(?:,? NY)?\b", text, re.I)
                and re.search(r"\bMetropolitan Museum of Art\b", text, re.I)):
            # The reference supports one exact destination/museum, not free-form planning.
            supported = re.fullmatch(
                r"(?:please )?(?:plan (?:a |my |the )?(?:visit|trip) to |visit )?"
                r"(?:the )?Metropolitan Museum of Art(?: in|,)? New York(?:,? NY)?"
                r"(?: on| for)? \d{4}-\d{2}-\d{2}[.!]?", text, re.I,
            )
            if supported:
                try:
                    trip = Trip(destination="New York, NY", museum="Metropolitan Museum of Art",
                                visit_date=dates[0]).model_dump()
                except ValueError:
                    trip = None
    state = {"run_id": uuid.uuid4().hex, "findings": {}}
    if trip:
        state["trip"] = trip
    else:
        state["clarification"] = (
            "This reference supports only the Metropolitan Museum of Art in New York, NY, "
            "on one date within the next six UTC days. "
            "Please send: Plan a visit to the Metropolitan Museum of Art in New York on YYYY-MM-DD. "
            "Other destinations or additional constraints are not silently applied. "
            "No specialist or tool was called."
        )
    return WorkflowTurn(input=state)
