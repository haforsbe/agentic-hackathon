from pathlib import Path
import tempfile
import unittest

from fixtures import SyntheticSpecialists, drive_reference, trip
from trip_workflow import execute_request, itinerary_text


class ReferenceWorkflowTests(unittest.IsolatedAsyncioTestCase):
    async def test_supported_trip_combines_both_specialists(self):
        """W01: the graph invokes both domains and preserves sourced tradeoffs."""
        with tempfile.TemporaryDirectory() as temporary:
            invoke = SyntheticSpecialists()
            result = await drive_reference(Path(temporary), invoke)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(invoke.calls, [
            ("weather", None), ("weather", True), ("culture", None), ("culture", True),
        ])
        self.assertTrue(result["run_id"])
        rendered = itinerary_text(result)
        for domain, version in (("weather", "2"), ("culture", "3")):
            self.assertEqual(result["specialists"][domain]["agent_version"], version)
            self.assertIn(f"https://{domain}.example/source", rendered)
        self.assertIn("Rain may favor an indoor visit", rendered)
        self.assertIn("outdoor plans remain subject to the forecast", rendered)
        self.assertIn("accessibility are not verified", rendered)

    async def test_failed_or_invalid_specialist_preserves_other_evidence(self):
        """W02/W03: failures isolate one domain, preserving the other and limits."""
        for domain in ("weather", "culture"):
            for failure in ("timeout", "invalid", "contradictory"):
                with self.subTest(domain=domain, failure=failure):
                    heading = "Answer" if domain == "weather" else "Guidance"
                    invoke = SyntheticSpecialists(
                        failure={domain: failure},
                        final_text={domain: (
                            f"## {heading}\nI am waiting for separate human approval.\n\n"
                            "## Source\nhttps://source.example/\n\n"
                            "## Uncertainty\nLive availability is not verified."
                        )} if failure == "contradictory" else None,
                    )
                    with tempfile.TemporaryDirectory() as temporary:
                        result = await drive_reference(Path(temporary), invoke)
                    other = "culture" if domain == "weather" else "weather"
                    self.assertEqual(result["status"], "partial")
                    self.assertEqual(result["specialists"][domain]["status"], "failed")
                    self.assertEqual(result["specialists"][other]["status"], "ok")
                    self.assertTrue(result["specialists"][other]["source_evidence"])
                    if failure == "contradictory":
                        self.assertTrue(result["specialists"][domain]["source_evidence"])
                        self.assertIn("https://source.example/", itinerary_text(result))
                        self.assertIn("Live availability is not verified", itinerary_text(result))
                    else:
                        self.assertEqual(result["specialists"][domain]["source_evidence"], "")
                    self.assertNotIn("I am waiting", itinerary_text(result))
                    self.assertLessEqual(len(invoke.calls), 4)

    async def test_ambiguous_request_requires_clarification(self):
        """W03: unsupported constraints are not silently discarded."""
        from trip_responses import parse_response

        class TextRequest:
            request = {}

            async def get_input_items(self):
                return [{"type": "message", "role": "user"}]

            async def get_input_text(self):
                return (
                    "Plan a visit to the Metropolitan Museum of Art in New York on "
                    + trip()["visit_date"] + " with guaranteed step-free access"
                )

        turn = await parse_response(TextRequest())
        self.assertIn("clarification", turn.input)
        self.assertIn("No specialist or tool was called", turn.input["clarification"])
        self.assertNotIn("trip", turn.input)
        invoke = SyntheticSpecialists()
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(ValueError):
                await execute_request(Path(temporary), {
                    "trip": {**trip(), "destination": "Paris"},
                }, invoke)
        self.assertEqual(invoke.calls, [])
