import json
import io
from contextlib import redirect_stdout
from subprocess import TimeoutExpired
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from workshop.weather_delivery import repository_readiness as readiness


def responses():
    return [
        ("read", {"default_branch": "FY27", "permissions": {"admin": True}}),
        ("read", {"enabled": True, "allowed_actions": "all"}),
        ("read", [
            {"workflows": [{"path": path, "state": "active"}]}
            for path in readiness.REQUIRED_WORKFLOWS
        ]),
        ("read", [{"variables": [
            {"name": name, "value": "DO-NOT-PRINT"}
            for name in readiness.REQUIRED_VARIABLES
        ]}]),
    ]


class ReadinessTests(unittest.TestCase):
    @patch.object(readiness, "_read_api")
    def test_paginated_configuration_reports_no_values_or_live_pass(self, api):
        api.side_effect = responses()
        report = readiness.inspect_repository("owner/lab", "FY27")
        self.assertTrue(all(value == "passed" for value in report["checks"].values()))
        self.assertEqual(report["cloud_variables"]["status"], "configured-not-authenticated")
        self.assertEqual(report["live_readiness"], "not-verified")
        self.assertNotIn("DO-NOT-PRINT", json.dumps(report))
        self.assertTrue(api.call_args_list[-1].kwargs["paginate"])

    @patch.object(readiness, "_read_api")
    def test_missing_is_distinct_from_denied(self, api):
        data = responses()
        data[-1] = ("read", [{"variables": []}])
        api.side_effect = data
        report = readiness.inspect_repository("owner/lab", "FY27")
        self.assertEqual(report["cloud_variables"]["status"], "missing")
        self.assertEqual(len(report["cloud_variables"]["missing_names"]), 8)
        data[-1] = ("unknown: denied", None)
        api.side_effect = data
        report = readiness.inspect_repository("owner/lab", "FY27")
        self.assertEqual(report["cloud_variables"]["status"], "unknown: denied")
        self.assertNotIn("missing_names", report["cloud_variables"])

    @patch.object(readiness, "_read_api")
    def test_branch_admin_and_disabled_workflow_block_setup(self, api):
        data = responses()
        data[0] = ("read", {"default_branch": "other", "permissions": {"admin": False}})
        data[2][1][0]["workflows"][0]["state"] = "disabled_manually"
        api.side_effect = data
        report = readiness.inspect_repository("owner/lab", "FY27")
        self.assertTrue(report["checks"]["default_branch"].startswith("blocked:"))
        self.assertTrue(report["checks"]["administrator_access"].startswith("blocked:"))
        self.assertIn("disabled_manually", report["checks"][readiness.REQUIRED_WORKFLOWS[0]])

    @patch.object(readiness, "_read_api")
    def test_repository_unknown_does_not_infer_missing_configuration(self, api):
        api.return_value = ("unknown: unavailable or hidden", None)
        report = readiness.inspect_repository("owner/lab", "FY27")
        self.assertTrue(report["cloud_variables"]["status"].startswith("unknown:"))
        self.assertEqual(api.call_count, 1)

    @patch.object(readiness.subprocess, "run")
    def test_cli_failures_are_unknown_without_disclosing_stderr(self, run):
        for code in (401, 403, 404):
            run.return_value = SimpleNamespace(
                returncode=1, stderr=f"private detail HTTP {code}", stdout=""
            )
            state, payload = readiness._read_api("repos/owner/lab")
            self.assertTrue(state.startswith("unknown:"))
            self.assertNotIn("private detail", state)
            self.assertIsNone(payload)
        for error in (FileNotFoundError(), TimeoutExpired("gh", 30)):
            run.side_effect = error
            self.assertTrue(readiness._read_api("repos/owner/lab")[0].startswith("unknown:"))

    def test_invalid_repository_and_malformed_listing_are_rejected(self):
        with self.assertRaises(ValueError):
            readiness.inspect_repository("../lab", "FY27")
        with self.assertRaises(ValueError):
            readiness._listed_items([{}], "variables")

    @patch.object(readiness, "_read_api")
    def test_cli_exit_distinguishes_configured_from_incomplete_setup(self, api):
        args = ["--repository", "owner/lab", "--expected-default-branch", "FY27"]
        api.side_effect = responses()
        with redirect_stdout(io.StringIO()):
            self.assertEqual(readiness.main(args), 0)
        api.side_effect = [("unknown: denied", None)]
        with redirect_stdout(io.StringIO()):
            self.assertEqual(readiness.main(args), 1)

    @patch.object(readiness.subprocess, "run")
    def test_api_pagination_and_invalid_json_shape(self, run):
        run.return_value = SimpleNamespace(returncode=0, stdout='[{"variables": []}]')
        self.assertEqual(
            readiness._read_api("repos/owner/lab/actions/variables", paginate=True)[0],
            "read",
        )
        self.assertEqual(run.call_args.args[0][-2:], ["--paginate", "--slurp"])
        for payload in ("not json", "null", "{}"):
            run.return_value = SimpleNamespace(returncode=0, stdout=payload)
            self.assertTrue(
                readiness._read_api("repos/owner/lab/actions/variables", paginate=True)[0]
                .startswith("unknown:")
            )


if __name__ == "__main__":
    unittest.main()
