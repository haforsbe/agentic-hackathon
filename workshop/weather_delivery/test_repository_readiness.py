import json
import io
import subprocess
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from workshop.weather_delivery.repository_readiness import (
    REQUIRED_VARIABLES,
    REQUIRED_WORKFLOWS,
    _read_api,
    inspect_repository,
    main,
)


class RepositoryReadinessTests(unittest.TestCase):
    def inspect(self, *, variables=None, permission=True, branch="FY27", workflows=None):
        names = REQUIRED_VARIABLES if variables is None else variables
        responses = [
            ("read", {"default_branch": branch, "permissions": {"admin": permission}}),
            ("read", {"enabled": True, "allowed_actions": "selected"}),
            ("read", [{"workflows": [
                {"path": path, "state": "active"}
                for path in (REQUIRED_WORKFLOWS if workflows is None else workflows)
            ]}]),
            ("read", [{"variables": [{"name": name, "value": "DO-NOT-PRINT"} for name in names]}]),
        ]
        with patch(
            "workshop.weather_delivery.repository_readiness._read_api",
            side_effect=responses,
        ):
            return inspect_repository("example/owned-workshop", "FY27")

    def test_configured_metadata_is_never_live_readiness(self):
        report = self.inspect()
        self.assertTrue(all(value == "passed" for value in report["checks"].values()))
        self.assertEqual(report["cloud_variables"]["status"], "configured-not-authenticated")
        self.assertEqual(report["live_readiness"], "not-verified")
        self.assertEqual(report["actions_policy"], "selected")
        self.assertNotIn("DO-NOT-PRINT", json.dumps(report))

    def test_only_successful_variable_listing_can_prove_missing_names(self):
        report = self.inspect(variables=[])
        self.assertEqual(report["cloud_variables"]["status"], "missing")
        self.assertEqual(report["cloud_variables"]["missing_names"], sorted(REQUIRED_VARIABLES))

    def test_denied_variable_listing_does_not_claim_missing_configuration(self):
        with patch(
            "workshop.weather_delivery.repository_readiness._read_api",
            side_effect=[
                ("read", {"default_branch": "FY27", "permissions": {"admin": False}}),
                ("unknown: denied", None),
                ("unknown: denied", None),
                ("unknown: denied", None),
            ],
        ):
            report = inspect_repository("example/workshop", "FY27")
        self.assertEqual(report["cloud_variables"], {"status": "unknown: denied"})
        self.assertEqual(report["checks"]["workflow_availability"], "unknown: denied")
        self.assertEqual(report["checks"]["actions_enabled"], "unknown: denied")

    def test_wrong_branch_non_admin_and_missing_workflows_block_repository_setup(self):
        report = self.inspect(permission=False, branch="main", workflows=[])
        for status in report["checks"].values():
            if status != "passed":
                self.assertTrue(status.startswith("blocked:"), status)
        self.assertIn("differs", report["checks"]["default_branch"])
        self.assertIn("not an administrator", report["checks"]["administrator_access"])
        self.assertIn("absent", report["checks"][REQUIRED_WORKFLOWS[0]])

    def test_paginated_metadata_checks_all_pages_without_exposing_values(self):
        with patch(
            "workshop.weather_delivery.repository_readiness._read_api",
            side_effect=[
                ("read", {"default_branch": "FY27", "permissions": {"admin": True}}),
                ("read", {"enabled": True}),
                ("read", [
                    {"workflows": [{"path": path, "state": "active"}]}
                    for path in REQUIRED_WORKFLOWS
                ]),
                ("read", [
                    {"variables": [{"name": name, "value": "PRIVATE"}]}
                    for name in REQUIRED_VARIABLES
                ]),
            ],
        ):
            report = inspect_repository("example/workshop", "FY27")
        self.assertEqual(report["cloud_variables"]["missing_names"], [])
        self.assertNotIn("PRIVATE", json.dumps(report))

    def test_api_errors_are_unknown_not_absent(self):
        for code, reason in ((401, "sign-in required"), (403, "denied"), (404, "hidden")):
            with self.subTest(code=code), patch(
                "workshop.weather_delivery.repository_readiness.subprocess.run",
                return_value=subprocess.CompletedProcess(
                    [], 1, "", f"gh: request failed (HTTP {code})"
                ),
            ) as run:
                status, result = _read_api("repos/example/workshop/actions/variables", paginate=True)
                self.assertIsNone(result)
                self.assertIn(reason, status)
                self.assertTrue(status.startswith("unknown:"))
                self.assertIn("--paginate", run.call_args.args[0])

    def test_missing_gh_and_invalid_response_are_explicit_unknowns(self):
        with patch(
            "workshop.weather_delivery.repository_readiness.subprocess.run",
            side_effect=FileNotFoundError,
        ):
            self.assertEqual(_read_api("repos/example/workshop")[0], "unknown: gh unavailable")
        with patch(
            "workshop.weather_delivery.repository_readiness.subprocess.run",
            return_value=subprocess.CompletedProcess([], 0, "not json", ""),
        ):
            self.assertEqual(_read_api("repos/example/workshop")[0], "unknown: invalid API response")

    def test_unknown_repository_access_stops_before_other_queries(self):
        with patch(
            "workshop.weather_delivery.repository_readiness._read_api",
            return_value=("unknown: unavailable or hidden", None),
        ) as api:
            report = inspect_repository("example/workshop", "FY27")
        self.assertEqual(api.call_count, 1)
        self.assertTrue(report["cloud_variables"]["status"].startswith("unknown:"))

    def test_disabled_actions_and_fork_workflows_are_not_ready(self):
        with patch(
            "workshop.weather_delivery.repository_readiness._read_api",
            side_effect=[
                ("read", {"default_branch": "FY27"}),
                ("read", {"enabled": False}),
                ("read", [{"workflows": [
                    {"path": path, "state": "disabled_fork"} for path in REQUIRED_WORKFLOWS
                ]}]),
                ("read", [{"variables": []}]),
            ],
        ):
            report = inspect_repository("example/workshop", "FY27")
        self.assertIn("unknown:", report["checks"]["administrator_access"])
        self.assertIn("Actions disabled", report["checks"]["actions_enabled"])
        for path in REQUIRED_WORKFLOWS:
            self.assertIn("disabled_fork", report["checks"][path])

    def test_request_timeout_is_explicit_unknown(self):
        with patch(
            "workshop.weather_delivery.repository_readiness.subprocess.run",
            side_effect=subprocess.TimeoutExpired("gh", 30),
        ):
            self.assertEqual(
                _read_api("repos/example/workshop")[0],
                "unknown: GitHub request timed out",
            )

    def test_invalid_repository_and_empty_branch_make_no_requests(self):
        with patch("workshop.weather_delivery.repository_readiness._read_api") as api:
            with self.assertRaisesRegex(ValueError, "OWNER/REPOSITORY"):
                inspect_repository("../workshop", "FY27")
            with self.assertRaisesRegex(ValueError, "intended default branch"):
                inspect_repository("example/workshop", "")
        api.assert_not_called()

    def test_cli_exit_status_distinguishes_complete_missing_and_unknown_metadata(self):
        for variables, expected_exit in (
            ({"status": "configured-not-authenticated"}, 0),
            ({"status": "missing", "missing_names": ["WEATHER_OIDC_SUBJECT"]}, 1),
            ({"status": "unknown: denied"}, 1),
        ):
            with self.subTest(variables=variables), patch(
                "workshop.weather_delivery.repository_readiness.inspect_repository",
                return_value={"checks": {"default_branch": "passed"}, "cloud_variables": variables},
            ), redirect_stdout(io.StringIO()):
                self.assertEqual(main([
                    "--repository", "example/workshop", "--expected-default-branch", "FY27",
                ]), expected_exit)


if __name__ == "__main__":
    unittest.main()
