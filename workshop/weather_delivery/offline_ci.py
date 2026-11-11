"""Report offline delivery checks without implying a live agent test."""

import argparse
import json
import sys
from pathlib import Path

from workshop.weather_delivery.contract import ContractError, write_ci_record


PACKAGE_LABELS = {
    "absent": "NOT CHECKED (manifest absent; delivery-code tests only)",
    "passed": "PASSED (package structure and file hashes only)",
    "failed": "FAILED (invalid package or reviewed files)",
    "not-run": "NOT RUN (delivery-code tests did not pass)",
}


def report_coverage(commit, manifest_path, output_dir, tests_outcome):
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
            record = write_ci_record(commit, manifest_path, record_path)
            package_status = (
                "absent" if record["status"] == "contract-suite-only" else "passed"
            )
        except (ContractError, KeyError, TypeError, OSError, json.JSONDecodeError) as failure:
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
        if tests_outcome == "success" else f"NOT PASSED ({tests_outcome})"
    )
    summary = (
        "## Weather delivery: offline coverage only\n\n"
        "| Check | Result |\n|---|---|\n"
        f"| Delivery-code tests | {suite_label} |\n"
        f"| Participant package | {PACKAGE_LABELS[package_status]} |\n"
        "| Live Microsoft Foundry agent tests | NOT RUN |\n"
        "| Deployment | NOT RUN |\n\n"
        f"Checked Git commit: `{commit}`.\n\n"
        "These results do not prove Azure access, runtime identity, tool authentication "
        "or execution, human tool approval, memory isolation or production behavior. "
        "A passing offline report alone is not release approval. If checks pass, "
        "review the PR diff before merging; deployment is a separate manual action.\n"
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
        if error:
            print(f"BLOCKED: {error}", file=sys.stderr)
        return int(
            report["delivery_code_tests"] != "success"
            or report["participant_package"] == "failed"
        )
    except (ContractError, OSError) as error:
        print(f"BLOCKED: offline coverage could not be written: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
