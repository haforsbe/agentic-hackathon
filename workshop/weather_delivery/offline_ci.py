"""Publish offline coverage without implying a live agent test or release."""

import argparse
import json
import sys
from pathlib import Path

from workshop.weather_delivery.contract import ContractError, write_ci_record


PACKAGE_LABELS = {
    "absent": "NOT CHECKED (manifest absent; delivery-code tests only)",
    "passed": "PASSED (manifest structure and reviewed file hashes only)",
    "failed": "FAILED (invalid manifest or reviewed files)",
    "not-run": "NOT RUN (delivery-code tests did not pass)",
}


def report_coverage(commit, manifest_path, output_dir, tests_outcome, *, root="."):
    if tests_outcome not in {"success", "failure", "cancelled", "skipped"}:
        raise ContractError("Unknown delivery-code test outcome")
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    record_path = output / "weather-delivery-check.json"
    record_path.unlink(missing_ok=True)
    package_status = "not-run"
    error = None
    if tests_outcome == "success":
        try:
            record = write_ci_record(commit, manifest_path, record_path, root=root)
            package_status = (
                "passed" if record["status"] == "manifest-contract-passed" else "absent"
            )
        except (ContractError, KeyError, OSError, json.JSONDecodeError) as failure:
            package_status = "failed"
            error = str(failure)
    report = {
        "schema_version": 1,
        "source_commit": commit,
        "delivery_code_tests": tests_outcome,
        "participant_package": package_status,
        "live_agent_tests": "not-run",
        "deployment": "not-run",
        "eligible_for_release": False,
    }
    (output / "coverage.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    suite_label = (
        "PASSED (synthetic/offline)"
        if tests_outcome == "success"
        else f"NOT PASSED ({tests_outcome})"
    )
    summary = (
        "## Weather delivery: offline coverage only\n\n"
        "| Check | Result |\n|---|---|\n"
        f"| Delivery-code tests | {suite_label} |\n"
        f"| Participant package | {PACKAGE_LABELS[package_status]} |\n"
        "| Live Microsoft Foundry agent tests | NOT RUN |\n"
        "| Deployment / release | NOT RUN; not eligible for release |\n\n"
        "Green means only the offline checks above passed. It does not prove "
        "project access, runtime identity, MCP execution or human approval, "
        "memory behavior/isolation, telemetry, or a working consumer endpoint.\n"
    )
    (output / "summary.md").write_text(summary, encoding="utf-8")
    return report, summary, error


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--tests-outcome", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--summary", required=True)
    args = parser.parse_args(argv)
    try:
        report, summary, error = report_coverage(
            args.commit, args.manifest, args.output_dir, args.tests_outcome
        )
        with Path(args.summary).open("a", encoding="utf-8") as target:
            target.write(summary)
        print(summary)
        if error:
            print(f"BLOCKED: {error}", file=sys.stderr)
        return int(
            report["delivery_code_tests"] != "success"
            or report["participant_package"] == "failed"
        )
    except (ContractError, OSError) as error:
        print(f"BLOCKED: offline coverage report could not be written: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
