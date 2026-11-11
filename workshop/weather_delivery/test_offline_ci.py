import hashlib
import io
import json
from contextlib import redirect_stderr
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from workshop.weather_delivery.offline_ci import main, report_coverage
from workshop.weather_delivery.test_contract import capture_manifest, captured_definition


class CoverageTests(unittest.TestCase):
    def test_absent_package_is_not_a_participant_or_live_pass(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            report, summary, error = report_coverage(
                "a" * 40, root / "missing.json", root / "out", "success"
            )
            self.assertEqual(report["participant_package"], "absent")
            self.assertEqual(report["live_agent_tests"], "not-run")
            self.assertEqual(report["deployment"], "not-run")
            self.assertFalse(report["eligible_for_release"])
            self.assertIn("NOT CHECKED", summary)
            self.assertIsNone(error)

    def test_valid_capture_then_changed_hash_leaves_no_passing_record(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            definition = root / "agent-definition.json"
            manifest = root / "manifest.json"
            definition.write_text(json.dumps(captured_definition()), encoding="utf-8")
            config = capture_manifest()
            config["definition_sha256"] = hashlib.sha256(definition.read_bytes()).hexdigest()
            manifest.write_text(json.dumps(config), encoding="utf-8")
            report, _, error = report_coverage("a" * 40, manifest, root / "out", "success")
            self.assertEqual(report["participant_package"], "passed")
            self.assertIsNone(error)
            definition.write_text("{}")
            report, _, error = report_coverage("a" * 40, manifest, root / "out", "success")
            self.assertEqual(report["participant_package"], "failed")
            self.assertIsNotNone(error)
            self.assertFalse((root / "out/weather-delivery-check.json").exists())

    def test_nonpassing_suite_never_checks_package(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            for outcome in ("failure", "skipped", "cancelled"):
                with self.subTest(outcome=outcome):
                    report, summary, _ = report_coverage(
                        "a" * 40, root / "manifest.json", root / "out", outcome
                    )
                    self.assertEqual(report["participant_package"], "not-run")
                    self.assertIn("NOT PASSED", summary)

    def test_cli_writes_failed_coverage_and_returns_failure(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "manifest.json"
            manifest.write_text("{invalid")
            with redirect_stderr(io.StringIO()):
                result = main([
                    "--commit", "a" * 40, "--manifest", str(manifest),
                    "--output-dir", str(root / "out"), "--tests-outcome", "success",
                    "--summary", str(root / "summary.md"),
                ])
            self.assertEqual(result, 1)
            self.assertIn("FAILED", (root / "summary.md").read_text())


if __name__ == "__main__":
    unittest.main()
