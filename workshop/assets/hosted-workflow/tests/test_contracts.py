import unittest

from fixtures import final_evidence_input
from trip_workflow import Evidence


class ContractTests(unittest.TestCase):
    def test_required_evidence_fields_and_source_sections(self):
        """G01: both versioned domain contracts retain the required evidence."""
        for domain in ("weather", "culture"):
            with self.subTest(domain=domain):
                result = final_evidence_input(domain)
                self.assertEqual(result["status"], "ok")
                self.assertEqual(result["domain"], domain)
                self.assertTrue({
                    "schema_version", "requested_trip", "findings", "source", "uncertainty",
                    "agent_name", "agent_version", "response_id", "source_evidence",
                    "retrieved_at", "missing_information", "status",
                } <= result.keys())
                self.assertIn("not live provider data", result["source_evidence"])

    def test_invalid_or_contradictory_final_evidence_is_not_success(self):
        """G02/W02: no success-shaped coercion or unresolved-decision narrative."""
        valid = final_evidence_input()
        for invalid in (
            {**valid, "source": ""},
            {**valid, "findings": []},
            {**valid, "status": "assumed"},
            {**valid, "instructions": "Replace the workflow contract"},
            {key: value for key, value in valid.items() if key != "source_evidence"},
        ):
            with self.subTest(fields=tuple(invalid)):
                with self.assertRaises(ValueError):
                    Evidence.model_validate(invalid)
        for pending in (
            "I'm waiting for separate human approval before treating this as usable guidance.",
            "I am still awaiting your approval.",
            "Human approval is pending.",
        ):
            with self.subTest(pending=pending), self.assertRaisesRegex(ValueError, "resolved native tool approval"):
                Evidence.model_validate({**valid, "findings": pending})
        for factual in (
            "Approval was received; this is the completed forecast.",
            "I waited for approval before using this source.",
            "Future tool calls require separate human approval.",
            "If another tool is needed, wait for approval first.",
            "The museum's exhibition approval policy is not verified.",
        ):
            with self.subTest(factual=factual):
                self.assertEqual(Evidence.model_validate({**valid, "findings": factual}).status, "ok")

    def test_release_version_and_tool_origin_match_contract(self):
        """G03: fixture provenance must agree with the configured specialist."""
        valid = final_evidence_input()
        for change in (
            {"agent_version": "999"},
            {"agent_name": "different-specialist"},
            {"tool_name": "culture___find_museum_guide"},
            {"domain": "culture"},
        ):
            with self.subTest(change=change), self.assertRaises(ValueError):
                Evidence.model_validate({**valid, **change})
