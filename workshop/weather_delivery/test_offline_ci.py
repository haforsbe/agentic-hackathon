import hashlib
import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

from workshop.weather_delivery.offline_ci import main, report_coverage
from workshop.weather_delivery.test_contract import manifest


class OfflineCoverageTests(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.package = self.root / "student/weather-delivery"
        self.package.mkdir(parents=True)
        self.manifest_path = self.package / "manifest.json"
        self.output = self.root / "artifacts"

    def report(self, outcome="success"):
        return report_coverage(
            "1" * 40, self.manifest_path, self.output, outcome, root=self.root
        )

    def write_package(self):
        config = manifest()
        for path, digest in (
            (config["configuration_source_path"], "configuration_sha256"),
            (config["instructions"]["source_path"], "instructions"),
        ):
            content = b"synthetic reviewed file\n"
            (self.root / path).write_bytes(content)
            value = hashlib.sha256(content).hexdigest()
            if digest == "instructions":
                config[digest]["sha256"] = value
            else:
                config[digest] = value
        self.manifest_path.write_text(json.dumps(config), encoding="utf-8")

    def assert_no_live_claim(self, report, summary):
        self.assertEqual(report["live_agent_tests"], "not-run")
        self.assertEqual(report["deployment"], "not-run")
        self.assertFalse(report["eligible_for_release"])
        self.assertIn("Live Microsoft Foundry agent tests | NOT RUN", summary)
        self.assertIn("Deployment / release | NOT RUN", summary)
        self.assertIn("does not prove", summary)

    def test_absent_manifest_is_explicitly_not_a_participant_package_pass(self):
        report, summary, error = self.report()
        self.assertIsNone(error)
        self.assertEqual(report["participant_package"], "absent")
        self.assertIn("NOT CHECKED (manifest absent", summary)
        record = json.loads((self.output / "weather-delivery-check.json").read_text())
        self.assertEqual(record["status"], "contract-suite-only")
        self.assertIsNone(record["manifest_sha256"])
        self.assert_no_live_claim(report, summary)

    def test_present_valid_package_only_proves_structure_and_hashes(self):
        self.write_package()
        report, summary, error = self.report()
        self.assertIsNone(error)
        self.assertEqual(report["participant_package"], "passed")
        self.assertIn("manifest structure and reviewed file hashes only", summary)
        record = json.loads((self.output / "weather-delivery-check.json").read_text())
        self.assertEqual(record["status"], "manifest-contract-passed")
        self.assertIsNotNone(record["manifest_sha256"])
        self.assert_no_live_claim(report, summary)
        self.assertEqual(json.loads((self.output / "coverage.json").read_text()), report)
        self.assertEqual((self.output / "summary.md").read_text(), summary)

    def test_invalid_manifest_is_reported_and_never_leaves_a_passing_record(self):
        self.write_package()
        self.report()
        for content in ("{", "{}"):
            with self.subTest(content=content):
                self.manifest_path.write_text(content, encoding="utf-8")
                report, summary, error = self.report()
                self.assertEqual(report["participant_package"], "failed")
                self.assertIsNotNone(error)
                self.assertIn("FAILED (invalid manifest", summary)
                self.assertFalse((self.output / "weather-delivery-check.json").exists())
                self.assert_no_live_claim(report, summary)

    def test_changed_reviewed_file_fails_package_validation(self):
        self.write_package()
        (self.package / "instructions.md").write_text("changed", encoding="utf-8")
        report, _, error = self.report()
        self.assertEqual(report["participant_package"], "failed")
        self.assertIn("instructions file hash", error)

    def test_non_file_manifest_is_not_reported_as_absent(self):
        self.manifest_path.mkdir()
        report, _, error = self.report()
        self.assertEqual(report["participant_package"], "failed")
        self.assertIsNotNone(error)

    def test_failed_cancelled_or_skipped_tests_cannot_claim_a_pass(self):
        self.write_package()
        self.report()
        for outcome in ("failure", "cancelled", "skipped"):
            with self.subTest(outcome=outcome):
                report, summary, error = self.report(outcome)
                self.assertIsNone(error)
                self.assertEqual(report["delivery_code_tests"], outcome)
                self.assertEqual(report["participant_package"], "not-run")
                self.assertIn(f"NOT PASSED ({outcome})", summary)
                self.assertFalse((self.output / "weather-delivery-check.json").exists())
                self.assert_no_live_claim(report, summary)

    def test_cli_writes_job_summary_even_when_package_is_invalid(self):
        self.manifest_path.write_text("{}", encoding="utf-8")
        summary_path = self.root / "job-summary.md"
        stderr = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(stderr):
            result = main([
                "--commit", "1" * 40, "--manifest", str(self.manifest_path),
                "--tests-outcome", "success", "--output-dir", str(self.output),
                "--summary", str(summary_path),
            ])
        self.assertEqual(result, 1)
        self.assertIn("BLOCKED: manifest must contain exactly", stderr.getvalue())
        self.assertEqual(summary_path.read_text(), (self.output / "summary.md").read_text())

    def test_cli_absent_manifest_succeeds_without_claiming_package_or_live_checks(self):
        summary_path = self.root / "job-summary.md"
        with redirect_stdout(io.StringIO()):
            result = main([
                "--commit", "1" * 40, "--manifest", str(self.manifest_path),
                "--tests-outcome", "success", "--output-dir", str(self.output),
                "--summary", str(summary_path),
            ])
        self.assertEqual(result, 0)
        self.assertIn("NOT CHECKED (manifest absent", summary_path.read_text())
        self.assertIn("Live Microsoft Foundry agent tests | NOT RUN", summary_path.read_text())


if __name__ == "__main__":
    unittest.main()
