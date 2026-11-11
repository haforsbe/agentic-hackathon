import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import uuid

from fixtures import SERVER_LABELS, SPECIALISTS, SyntheticSpecialists, trip
from starlette.testclient import TestClient

import trip_server
from trip_responses import parse_response, prepare_options


class ChatContractTests(unittest.TestCase):
    """Checkpoint 15 synthetic adapter prerequisites, not live W04 evidence."""

    def setUp(self):
        temporary = self.enterContext(tempfile.TemporaryDirectory())
        folder = Path(temporary)
        self.specialists = SyntheticSpecialists()
        self.enterContext(patch.object(trip_server, "NativeInvoker", return_value=self.specialists))
        self.enterContext(patch.object(trip_server, "AIProjectClient"))
        self.enterContext(patch.object(trip_server, "platform_credential"))
        self.enterContext(patch.object(trip_server, "root", folder / "runtime"))
        self.enterContext(patch.dict(os.environ, {"AGENTSERVER_STATE_ROOT": str(folder / "state")}))
        app = trip_server.WorkflowHost(
            workflow=trip_server.response_workflow,
            parse_response=parse_response, prepare_options=prepare_options,
        )
        self.client = self.enterContext(TestClient(app))
        self.session = "synthetic-" + uuid.uuid4().hex

    def post(self, payload):
        response = self.client.post(
            "/responses?agent_session_id=" + self.session,
            headers={
                "x-agent-user-id": "synthetic-user",
                "x-agent-foundry-call-id": uuid.uuid4().hex,
            },
            json={"model": "", "store": True, "agent_session_id": self.session, **payload},
        )
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()

    def start(self):
        return self.post({"input": (
            "Plan a visit to the Metropolitan Museum of Art in New York on "
            + trip()["visit_date"]
        )})

    def decision(self, current, approved):
        requests = [item for item in current["output"] if item["type"] == "mcp_approval_request"]
        self.assertEqual(len(requests), 1, current)
        return self.post({
            "previous_response_id": current["id"],
            "input": [{
                "type": "mcp_approval_response", "approval_request_id": requests[0]["id"],
                "approve": approved,
            }],
        })

    @staticmethod
    def text(result):
        return "\n".join(
            part["text"] for item in result["output"] if item["type"] == "message"
            for part in item["content"] if part["type"] == "output_text"
        )

    def test_two_separate_decisions_produce_sourced_reply(self):
        """Local W04 prerequisite: both decisions precede sourced final assembly."""
        for invalid_summary in (False, True):
            with self.subTest(invalid_summary=invalid_summary):
                self.session = "synthetic-" + uuid.uuid4().hex
                self.specialists.calls.clear()
                self.specialists.executed_tools.clear()
                if invalid_summary:
                    self.specialists.final_text["culture"] = (
                        "## Guidance\nI'm waiting for separate human approval.\n\n"
                        "## Source\nhttps://culture.example/source\n\n"
                        "## Uncertainty\nAccessibility is not verified."
                    )
                first = self.start()
                weather = next(item for item in first["output"] if item["type"] == "mcp_approval_request")
                self.assertEqual(weather["name"], SPECIALISTS["weather"][2])
                self.assertEqual(weather["server_label"], SERVER_LABELS["weather"])
                self.assertEqual(self.specialists.executed_tools, [])
                second = self.decision(first, True)
                self.assertEqual(second["status"], "completed", second)
                culture = next(item for item in second["output"] if item["type"] == "mcp_approval_request")
                self.assertEqual(culture["name"], SPECIALISTS["culture"][2])
                self.assertEqual(self.specialists.executed_tools, ["weather"])
                final = self.decision(second, True)
                self.assertEqual(self.specialists.executed_tools, ["weather", "culture"])
                text = self.text(final)
                self.assertIn("Workflow result: " + ("partial" if invalid_summary else "completed"), text)
                self.assertIn("https://weather.example/source", text)
                self.assertIn("https://culture.example/source", text)
                self.assertIn("Workflow run:", text)
                if invalid_summary:
                    self.assertIn("Cultural guide (failed)", text)
                    self.assertIn("Accessibility is not verified", text)
                    self.assertNotIn("I'm waiting", text)
                else:
                    self.assertIn("accessibility are not verified", text)

    def test_denial_stays_partial_without_executing_denied_tool(self):
        """W02/local W04 prerequisite: each exact denial remains authoritative."""
        for denied in ("weather", "culture"):
            with self.subTest(denied=denied):
                self.session = "synthetic-" + uuid.uuid4().hex
                self.specialists.calls.clear()
                self.specialists.executed_tools.clear()
                first = self.start()
                second = self.decision(first, denied != "weather")
                final = self.decision(second, denied != "culture")
                self.assertNotIn(denied, self.specialists.executed_tools)
                text = self.text(final)
                self.assertIn("Workflow result: partial", text)
                label = "Weather" if denied == "weather" else "Cultural guide"
                self.assertIn(label + " (denied)", text)
                self.assertIn("Tool execution was denied", text)
