"""Synthetic teaching data; never evidence of a cloud call or human decision."""

from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["WORKFLOW_CONFIG_JSON"] = json.dumps({
    "participant_confirmed": True,
    "project_endpoint": "https://example.services.ai.azure.com/api/projects/reference",
    "tenant_id": "11111111-1111-4111-8111-111111111111",
    "runtime_principal_id": "22222222-2222-4222-8222-222222222222",
    "workflow_name": "trip-reference",
    "weather": {
        "agent_name": "weather-reference", "version": "2",
        "server_label": "weather-tools", "tool_name": "weather___weather_forecast",
    },
    "culture": {
        "agent_name": "culture-reference", "version": "3",
        "server_label": "culture-tools", "tool_name": "culture___find_museum_guide",
    },
})

from trip_workflow import SERVER_LABELS, SPECIALISTS, execute_request


def trip():
    return {
        "destination": "New York, NY",
        "museum": "Metropolitan Museum of Art",
        "visit_date": (datetime.now(timezone.utc).date() + timedelta(days=1)).isoformat(),
    }


class SyntheticSpecialists:
    def __init__(self, *, failure=None, final_text=None):
        self.failure = failure or {}
        self.final_text = final_text or {}
        self.calls = []
        self.executed_tools = []

    def __call__(self, domain, requested_trip, pending, approved):
        self.calls.append((domain, approved))
        if self.failure.get(domain) == "timeout":
            raise TimeoutError("Synthetic unavailable specialist")
        name, version, tool, heading = SPECIALISTS[domain]
        arguments = (
            {"lat": 40.7794, "lon": -73.9632, "hourly": False}
            if domain == "weather" else
            {"query": "Metropolitan Museum of Art", "city": "New York", "country": "US"}
        )
        if pending is None:
            output = [{
                "type": "mcp_approval_request", "id": "mcpr_synthetic_" + domain,
                "name": tool, "server_label": SERVER_LABELS[domain],
                "arguments": json.dumps(arguments),
            }]
        else:
            output = []
            if approved:
                self.executed_tools.append(domain)
                output.append({
                    "type": "mcp_call", "name": tool,
                    "server_label": SERVER_LABELS[domain],
                    "arguments": json.dumps(arguments),
                    "approval_request_id": pending["approval_request_id"],
                    "status": "completed", "error": None,
                    "output": f"Synthetic {domain} source; not live provider data",
                })
            findings = (
                "Rain may favor an indoor visit." if domain == "weather" else
                "A guide is available; outdoor plans remain subject to the forecast."
            ) if approved else "The tool call was denied; no result is available."
            text = self.final_text.get(domain, (
                f"## {heading}\n{findings}\n\n## Source\n"
                f"https://{domain}.example/source\n\n## Uncertainty\n"
                "Synthetic fixture only; live availability and accessibility are not verified."
            ))
            if self.failure.get(domain) == "invalid":
                text = "Unsupported unstructured specialist reply."
            output.append({
                "type": "message",
                "content": [{"type": "output_text", "text": text}],
            })
        return {
            "id": f"resp_synthetic_{domain}_{'final' if pending else 'initial'}",
            "status": "completed", "agent_reference": {"name": name, "version": version},
            "output": output,
        }


def final_evidence_input(domain="weather"):
    from trip_workflow import result_evidence
    requested = trip()
    invoke = SyntheticSpecialists()
    initial = invoke(domain, requested, None, None)
    item = initial["output"][0]
    pending = {
        "response_id": initial["id"], "approval_request_id": item["id"],
        "tool_name": item["name"], "server_label": item["server_label"],
        "arguments": json.loads(item["arguments"]),
    }
    final = invoke(domain, requested, pending, True)
    return result_evidence(domain, requested, final, pending, True)


async def drive_reference(folder, invoke):
    value = await execute_request(folder, {"trip": trip()}, invoke)
    while value["status"] == "awaiting_approval":
        value = await execute_request(
            folder, {"approval": {**value["approval"], "approve": True}}, invoke,
        )
    return value
