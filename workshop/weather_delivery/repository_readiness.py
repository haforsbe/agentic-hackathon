"""Read-only GitHub setup preflight; never authenticates to Microsoft Foundry."""

import argparse
import json
import re
import subprocess
import sys


REQUIRED_VARIABLES = (
    "WEATHER_AZURE_CLIENT_ID",
    "WEATHER_AZURE_TENANT_ID",
    "WEATHER_AZURE_SUBSCRIPTION_ID",
    "WEATHER_OIDC_SUBJECT",
    "WEATHER_FOUNDRY_PROJECT_ENDPOINT",
)
REQUIRED_WORKFLOWS = (
    ".github/workflows/weather-delivery-check.yml",
    ".github/workflows/weather-delivery-cloud.yml",
)


def _read_api(path, *, paginate=False):
    command = ["gh", "api", path]
    if paginate:
        command.extend(["--paginate", "--slurp"])
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, check=False, timeout=30
        )
    except OSError:
        return "unknown: gh unavailable", None
    except subprocess.TimeoutExpired:
        return "unknown: GitHub request timed out", None
    if result.returncode:
        match = re.search(r"HTTP (\d{3})", result.stderr)
        code = match.group(1) if match else None
        reason = {
            "401": "sign-in required",
            "403": "denied",
            "404": "unavailable or hidden; not evidence of absence",
        }.get(code, "request failed")
        return f"unknown: {reason}", None
    try:
        return "read", json.loads(result.stdout)
    except json.JSONDecodeError:
        return "unknown: invalid API response", None


def inspect_repository(repository, expected_default_branch):
    if (
        re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9_.-]+", repository) is None
        or repository.rsplit("/", 1)[-1] in {".", ".."}
    ):
        raise ValueError("Use an explicit OWNER/REPOSITORY name")
    if not expected_default_branch.strip():
        raise ValueError("Confirm the intended default branch")
    prefix = f"repos/{repository}"
    report = {
        "repository": repository,
        "expected_default_branch": expected_default_branch,
        "scope": "GitHub metadata only; no Azure access, runtime test or deployment",
        "checks": {},
        "cloud_variables": {},
        "live_readiness": "not-verified",
    }
    checks = report["checks"]
    state, metadata = _read_api(prefix)
    if state != "read":
        checks["repository_access"] = state
        report["cloud_variables"] = {"status": "unknown: repository access not verified"}
        return report
    actual_branch = metadata.get("default_branch")
    report["actual_default_branch"] = actual_branch
    checks["default_branch"] = (
        "passed" if actual_branch == expected_default_branch
        else "blocked: default branch differs from intended workshop branch"
    )
    admin = metadata.get("permissions", {}).get("admin")
    checks["administrator_access"] = (
        "passed" if admin is True else
        "blocked: caller is not an administrator" if admin is False else
        "unknown: administrator permission not returned"
    )
    state, permissions = _read_api(f"{prefix}/actions/permissions")
    checks["actions_enabled"] = (
        "passed" if permissions.get("enabled") is True else
        "blocked: Actions disabled" if permissions.get("enabled") is False else
        "unknown: Actions enabled state not returned"
    ) if state == "read" else state
    if state == "read":
        report["actions_policy"] = permissions.get("allowed_actions", "unknown")
    state, pages = _read_api(f"{prefix}/actions/workflows?per_page=100", paginate=True)
    if state == "read":
        workflows = {
            workflow["path"]: workflow.get("state")
            for page in pages for workflow in page["workflows"]
        }
        for path in REQUIRED_WORKFLOWS:
            checks[path] = (
                "passed" if workflows.get(path) == "active" else
                "blocked: workflow absent from successful listing" if path not in workflows else
                f"blocked: workflow state is {workflows[path]}"
            )
    else:
        checks["workflow_availability"] = state
    state, pages = _read_api(f"{prefix}/actions/variables?per_page=100", paginate=True)
    if state == "read":
        names = {variable["name"] for page in pages for variable in page["variables"]}
        missing = sorted(set(REQUIRED_VARIABLES) - names)
        report["cloud_variables"] = {
            "status": "missing" if missing else "configured-not-authenticated",
            "missing_names": missing,
        }
    else:
        report["cloud_variables"] = {"status": state}
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True, help="Participant-owned OWNER/REPOSITORY")
    parser.add_argument("--expected-default-branch", required=True)
    args = parser.parse_args(argv)
    try:
        report = inspect_repository(args.repository, args.expected_default_branch)
    except (ValueError, KeyError, TypeError) as error:
        print(f"BLOCKED: repository preflight could not interpret metadata: {error}", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2, sort_keys=True))
    return int(
        any(value != "passed" for value in report["checks"].values())
        or report["cloud_variables"]["status"] != "configured-not-authenticated"
    )


if __name__ == "__main__":
    raise SystemExit(main())
