"""Fail-closed, offline checks for sanitized Weather delivery evidence."""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, quote, urlsplit


class ContractError(ValueError):
    """A delivery artifact does not satisfy the reviewed contract."""


def _object(value, keys, label):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ContractError(f"{label} must contain exactly: {', '.join(sorted(keys))}")
    return value


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{label} must be a nonempty string")
    if "://" in value or value.lower().startswith("bearer "):
        raise ContractError(f"{label} must be a reference, not a URL or credential")
    return value


def _sha256(value, label):
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise ContractError(f"{label} must be a lowercase SHA-256 digest")
    return value


def _https_url(value, label):
    if not isinstance(value, str):
        raise ContractError(f"{label} must be an HTTPS URL")
    parts = urlsplit(value)
    if (
        parts.scheme != "https"
        or not parts.hostname
        or parts.username is not None
        or parts.password is not None
        or parts.fragment
    ):
        raise ContractError(f"{label} must be an HTTPS URL without credentials or a fragment")
    return parts


def canonical_sha256(value):
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _reject_credentials(value):
    sensitive_names = {
        "authorization", "headers", "password", "secret", "token",
        "api_key", "apikey", "credential", "connection_string",
    }
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).casefold().replace("-", "_")
            if (
                normalized in sensitive_names
                or normalized.endswith(("_token", "_secret", "_password", "_api_key"))
            ):
                raise ContractError("Agent configuration contains a credential-like field")
            _reject_credentials(child)
    elif isinstance(value, list):
        for child in value:
            _reject_credentials(child)


def validate_capture_package(manifest, definition, *, expected_production_agent=None):
    _object(
        manifest,
        {
            "schema_version", "source_agent_name", "source_agent_version",
            "production_agent_name", "production_stable_endpoint",
            "definition_sha256",
        },
        "capture manifest",
    )
    if type(manifest["schema_version"]) is not int or manifest["schema_version"] != 1:
        raise ContractError("Unsupported capture manifest schema_version")
    source_name = _text(manifest["source_agent_name"], "source_agent_name")
    _text(manifest["source_agent_version"], "source_agent_version")
    production_name = _text(manifest["production_agent_name"], "production_agent_name")
    if source_name == production_name:
        raise ContractError("The Dev source and Prod target must be separate agents")
    _sha256(manifest["definition_sha256"], "definition_sha256")
    endpoint = _https_url(
        manifest["production_stable_endpoint"], "production_stable_endpoint",
    )
    expected_endpoint_path = (
        f"/agents/{quote(production_name, safe='')}/endpoint/protocols/openai/responses"
    )
    if endpoint.query or not endpoint.path.endswith(expected_endpoint_path):
        raise ContractError("Prod stable endpoint must match the configured Prod agent")
    if expected_production_agent is not None and production_name != expected_production_agent:
        raise ContractError("Capture manifest targets a different configured Prod agent")

    _object(definition, {"schema_version", "definition"}, "captured agent definition")
    if type(definition["schema_version"]) is not int or definition["schema_version"] != 1:
        raise ContractError("Unsupported captured agent definition schema_version")
    body = definition["definition"]
    _reject_credentials(body)
    if (
        not isinstance(body, dict)
        or body.get("kind") != "prompt"
        or not isinstance(body.get("model"), str)
        or not body["model"]
        or not isinstance(body.get("instructions"), str)
        or not isinstance(body.get("tools", []), list)
    ):
        raise ContractError("Captured definition must be a prompt agent with model and instructions")
    return manifest


def validate_capture_files(manifest_path, definition_path, *, expected_production_agent=None):
    manifest_file = Path(manifest_path)
    definition_file = Path(definition_path)
    try:
        manifest = _read(manifest_file)
        definition = _read(definition_file)
    except (OSError, json.JSONDecodeError) as error:
        raise ContractError("Capture manifest and agent definition must be readable JSON files") from error
    validate_capture_package(
        manifest, definition, expected_production_agent=expected_production_agent,
    )
    actual_hash = hashlib.sha256(definition_file.read_bytes()).hexdigest()
    if actual_hash != manifest["definition_sha256"]:
        raise ContractError("Captured agent definition hash differs from the manifest")
    return manifest, definition


def validation_cases_sha256():
    cases = json.loads(
        (Path(__file__).with_name("cases.json")).read_text(encoding="utf-8")
    )
    return canonical_sha256(cases)


def validate_manifest(manifest):
    _object(
        manifest,
        {
            "schema_version", "lab", "project_ref", "released_agent",
            "validation_agent", "configuration_source_path",
            "configuration_sha256", "model_policy",
            "instructions", "toolbox", "skill", "memory", "unverified_bindings",
        },
        "manifest",
    )
    if type(manifest["schema_version"]) is not int or manifest["schema_version"] != 1:
        raise ContractError("Unsupported manifest schema_version")

    lab = _object(
        manifest["lab"],
        {"project_count", "classification", "production_isolation"},
        "lab",
    )
    if (
        type(lab["project_count"]) is not int
        or lab["project_count"] != 1
        or lab["classification"] != "training-compromise"
        or lab["production_isolation"] is not False
    ):
        raise ContractError("The lab must explicitly disclose its single-project training compromise")
    project_ref = _text(manifest["project_ref"], "project_ref")

    released = _object(
        manifest["released_agent"],
        {"name", "version", "stable_endpoint", "endpoint_source", "configuration_sha256"},
        "released_agent",
    )
    release_name = _text(released["name"], "released_agent.name")
    _text(released["version"], "released_agent.version")
    _sha256(released["configuration_sha256"], "released_agent.configuration_sha256")
    if released["endpoint_source"] != "service-read-back":
        raise ContractError("The stable agent endpoint must come from service metadata")
    stable_parts = _https_url(released["stable_endpoint"], "released_agent.stable_endpoint")

    candidate = _object(
        manifest["validation_agent"], {"name", "memory_scope_ref"}, "validation_agent",
    )
    candidate_name = _text(candidate["name"], "validation_agent.name")
    candidate_memory = _text(candidate["memory_scope_ref"], "validation_agent.memory_scope_ref")
    if candidate_name == release_name:
        raise ContractError("Validation must use a separate agent from the released Weather agent")
    configuration_path = manifest["configuration_source_path"]
    if (
        not isinstance(configuration_path, str)
        or not configuration_path.startswith("student/")
        or ".." in Path(configuration_path).parts
    ):
        raise ContractError("configuration_source_path must be a safe path under student/")
    _sha256(manifest["configuration_sha256"], "configuration_sha256")

    model = _object(
        manifest["model_policy"], {"deployment_ref", "model", "version", "change_policy"},
        "model_policy",
    )
    for key in ("deployment_ref", "model", "version"):
        _text(model[key], f"model_policy.{key}")
    if model["change_policy"] != "keep-existing":
        raise ContractError("Validation must keep the participant-selected model deployment unchanged")

    instructions = _object(
        manifest["instructions"], {"source_path", "sha256"}, "instructions",
    )
    source_path = instructions["source_path"]
    if (
        not isinstance(source_path, str)
        or not source_path.startswith("student/")
        or ".." in Path(source_path).parts
    ):
        raise ContractError("instructions.source_path must be a safe path under student/")
    _sha256(instructions["sha256"], "instructions.sha256")

    toolbox = _object(
        manifest["toolbox"],
        {
            "name", "version", "mcp_url", "endpoint_source",
            "upstream_connection_ref", "upstream_target", "upstream_auth",
            "toolbox_auth_connection_ref", "toolbox_auth_type",
            "toolbox_auth_evidence_ref", "tool_map", "require_approval",
            "unverified_bindings",
        },
        "toolbox",
    )
    toolbox_name = _text(toolbox["name"], "toolbox.name")
    toolbox_version = _text(toolbox["version"], "toolbox.version")
    if toolbox["endpoint_source"] != "service-read-back":
        raise ContractError("The Toolbox MCP URL must be copied from service read-back")
    toolbox_parts = _https_url(toolbox["mcp_url"], "toolbox.mcp_url")
    expected_path = (
        f"/toolboxes/{quote(toolbox_name, safe='')}/versions/"
        f"{quote(toolbox_version, safe='')}/mcp"
    )
    if (
        not toolbox_parts.path.startswith("/api/projects/")
        or not toolbox_parts.path.endswith(expected_path)
        or parse_qs(toolbox_parts.query) != {"api-version": ["v1"]}
    ):
        raise ContractError("Use the service-returned, version-specific Toolbox MCP endpoint")
    if stable_parts.geturl() == toolbox_parts.geturl():
        raise ContractError("A Toolbox MCP endpoint is not a stable agent consumer endpoint")
    if toolbox["upstream_target"] != "https://weather.datakoot.com/mcp":
        raise ContractError("Use the selected public Weather MCP server")
    if toolbox["upstream_auth"] != "none":
        raise ContractError("The public Weather upstream connection must remain anonymous")
    upstream_ref = _text(toolbox["upstream_connection_ref"], "toolbox.upstream_connection_ref")
    auth_ref = _text(
        toolbox["toolbox_auth_connection_ref"], "toolbox.toolbox_auth_connection_ref",
    )
    if upstream_ref == auth_ref:
        raise ContractError("Upstream and Toolbox-authentication connections must be distinct")
    for key in ("toolbox_auth_type", "toolbox_auth_evidence_ref"):
        _text(toolbox[key], f"toolbox.{key}")
    if toolbox["require_approval"] != "always":
        raise ContractError("Every MCP call must retain per-call approval")
    if toolbox["unverified_bindings"] != []:
        raise ContractError("Unsupported or unverified bindings must block this manifest")
    tool_map = toolbox["tool_map"]
    if (
        not isinstance(tool_map, dict)
        or "weather_forecast" not in tool_map
        or not all(
            isinstance(key, str) and key and isinstance(value, str) and value
            for key, value in tool_map.items()
        )
        or len(set(tool_map.values())) != len(tool_map)
    ):
        raise ContractError("Record a one-to-one mapping for the discovered Weather tool names")

    skill = _object(manifest["skill"], {"revision", "delivery", "sha256"}, "skill")
    for key in ("revision", "delivery"):
        _text(skill[key], f"skill.{key}")
    _sha256(skill["sha256"], "skill.sha256")

    memory = _object(
        manifest["memory"],
        {
            "configuration_sha256", "released_scope_ref", "validation_scope_ref",
            "contents_included",
        },
        "memory",
    )
    _sha256(memory["configuration_sha256"], "memory.configuration_sha256")
    released_memory = _text(memory["released_scope_ref"], "memory.released_scope_ref")
    validation_memory = _text(memory["validation_scope_ref"], "memory.validation_scope_ref")
    if memory["contents_included"] is not False:
        raise ContractError("Memory contents must never be captured")
    if (
        released_memory == validation_memory
        or candidate_memory != validation_memory
        or released_memory == project_ref
        or validation_memory == project_ref
    ):
        raise ContractError("Candidate and release memory scopes must be explicitly distinct")
    if manifest["unverified_bindings"] != []:
        raise ContractError("Unsupported or unverified bindings must block this manifest")
    return manifest


def validate_ci_run(run, manifest, *, repository, default_branch, current_commit, latest_sha, latest_attempt):
    _object(
        run,
        {
            "id", "attempt", "repository", "head_repository", "head_sha",
            "head_branch", "workflow_path", "event", "status", "conclusion",
            "latest_attempt", "artifact", "record",
        },
        "ci_run",
    )
    run_id = run["id"]
    attempt = run["attempt"]
    artifact = _object(run["artifact"], {"name", "run_id", "expired"}, "ci_run.artifact")
    record = _object(
        run["record"],
        {
            "schema_version", "status", "eligible_for_release", "source_commit",
            "manifest_sha256", "cases_sha256",
        },
        "ci_run.record",
    )
    expected_artifact = f"weather-delivery-{run_id}-{attempt}"
    if (
        not isinstance(run_id, str)
        or not run_id.isdigit()
        or type(attempt) is not int
        or type(run["latest_attempt"]) is not int
        or run["latest_attempt"] != attempt
        or latest_attempt != attempt
        or run["repository"] != repository
        or run["head_repository"] != repository
        or run["head_sha"] != current_commit
        or run["head_sha"] != latest_sha
        or run["head_branch"] != default_branch
        or run["workflow_path"] != ".github/workflows/weather-delivery-check.yml"
        or not isinstance(run["event"], str)
        or run["event"] not in {"push", "workflow_dispatch"}
        or run["status"] != "completed"
        or run["conclusion"] != "success"
        or artifact["name"] != expected_artifact
        or artifact["run_id"] != run_id
        or artifact["expired"] is not False
        or type(record["schema_version"]) is not int
        or record["schema_version"] != 1
        or record["status"] != "manifest-contract-passed"
        or record["eligible_for_release"] is not False
        or record["source_commit"] != current_commit
        or record["manifest_sha256"] != canonical_sha256(manifest)
        or record["cases_sha256"] != validation_cases_sha256()
    ):
        raise ContractError(
            "CI evidence must be the successful latest run and artifact for this "
            "repository's default-branch commit"
        )
    return expected_artifact


def _evidence_id(value, label):
    return _text(value, label)


def validate_validation_evidence(
    manifest,
    evidence,
    *,
    repository,
    default_branch,
    current_commit,
    latest_sha,
    latest_attempt,
):
    validate_manifest(manifest)
    _object(
        evidence,
        {
            "schema_version", "status", "source_commit", "manifest_sha256",
            "cases_sha256", "ci_run", "runtime", "checks", "tool_calls",
        },
        "validation evidence",
    )
    if type(evidence["schema_version"]) is not int or evidence["schema_version"] != 1:
        raise ContractError("Unsupported validation evidence schema_version")
    if evidence["status"] != "passed":
        raise ContractError("A failed or blocked attempt cannot authorize release; preserve its evidence")
    if (
        not isinstance(evidence["source_commit"], str)
        or re.fullmatch(r"[0-9a-f]{40}", evidence["source_commit"]) is None
    ):
        raise ContractError("source_commit must be a full Git commit SHA")
    if evidence["source_commit"] != current_commit:
        raise ContractError("Validation evidence is for a different configuration commit")
    if evidence["manifest_sha256"] != canonical_sha256(manifest):
        raise ContractError("Validation evidence does not match the reviewed manifest")
    _sha256(evidence["cases_sha256"], "cases_sha256")
    if evidence["cases_sha256"] != validation_cases_sha256():
        raise ContractError("Validation evidence uses a different reviewed case definition")
    validate_ci_run(
        evidence["ci_run"],
        manifest,
        repository=repository,
        default_branch=default_branch,
        current_commit=current_commit,
        latest_sha=latest_sha,
        latest_attempt=latest_attempt,
    )

    runtime = _object(
        evidence["runtime"],
        {
            "project_ref", "ci_identity_ref", "runtime_identity_ref",
            "validation_agent_name", "validation_agent_version",
            "validation_config_sha256", "validation_memory_scope_ref",
            "released_agent_name", "released_config_sha256",
            "released_agent_version", "released_memory_scope_ref",
            "toolbox_name", "toolbox_version", "toolbox_mcp_url",
            "toolbox_auth_type", "toolbox_auth_evidence_ref",
            "upstream_connection_ref", "toolbox_auth_connection_ref",
            "upstream_target", "upstream_tools", "instructions_sha256",
            "model_deployment_ref", "model_name", "model_version",
            "skill_revision", "skill_delivery", "skill_sha256",
            "memory_configuration_sha256", "effective_tool_names", "unverified_bindings",
        },
        "runtime",
    )
    if (
        runtime["project_ref"] != manifest["project_ref"]
        or runtime["validation_agent_name"] != manifest["validation_agent"]["name"]
        or runtime["validation_config_sha256"] != manifest["configuration_sha256"]
        or runtime["released_agent_name"] != manifest["released_agent"]["name"]
        or runtime["released_config_sha256"] != manifest["released_agent"]["configuration_sha256"]
        or runtime["released_agent_version"] != manifest["released_agent"]["version"]
        or runtime["validation_memory_scope_ref"] != manifest["memory"]["validation_scope_ref"]
        or runtime["released_memory_scope_ref"] != manifest["memory"]["released_scope_ref"]
        or runtime["validation_memory_scope_ref"] == runtime["released_memory_scope_ref"]
        or runtime["memory_configuration_sha256"] != manifest["memory"]["configuration_sha256"]
        or runtime["ci_identity_ref"] == runtime["runtime_identity_ref"]
        or runtime["toolbox_name"] != manifest["toolbox"]["name"]
        or runtime["toolbox_version"] != manifest["toolbox"]["version"]
        or runtime["toolbox_mcp_url"] != manifest["toolbox"]["mcp_url"]
        or runtime["toolbox_auth_type"] != manifest["toolbox"]["toolbox_auth_type"]
        or runtime["toolbox_auth_evidence_ref"] != manifest["toolbox"]["toolbox_auth_evidence_ref"]
        or runtime["upstream_connection_ref"] != manifest["toolbox"]["upstream_connection_ref"]
        or runtime["toolbox_auth_connection_ref"] != manifest["toolbox"]["toolbox_auth_connection_ref"]
        or runtime["upstream_target"] != manifest["toolbox"]["upstream_target"]
        or runtime["upstream_tools"] != sorted(manifest["toolbox"]["tool_map"])
        or runtime["instructions_sha256"] != manifest["instructions"]["sha256"]
        or runtime["model_deployment_ref"] != manifest["model_policy"]["deployment_ref"]
        or runtime["model_name"] != manifest["model_policy"]["model"]
        or runtime["model_version"] != manifest["model_policy"]["version"]
        or runtime["skill_revision"] != manifest["skill"]["revision"]
        or runtime["skill_delivery"] != manifest["skill"]["delivery"]
        or runtime["skill_sha256"] != manifest["skill"]["sha256"]
        or runtime["effective_tool_names"] != sorted(manifest["toolbox"]["tool_map"].values())
        or runtime["unverified_bindings"] != []
    ):
        raise ContractError(
            "Runtime identity, configuration, candidate boundary, or pinned dependencies differ"
        )
    for key in (
        "project_ref", "ci_identity_ref", "runtime_identity_ref",
        "validation_agent_name", "validation_agent_version",
        "validation_memory_scope_ref", "released_agent_name",
        "released_agent_version", "released_memory_scope_ref", "toolbox_name",
        "toolbox_version", "upstream_connection_ref",
        "toolbox_auth_connection_ref", "toolbox_auth_type",
        "toolbox_auth_evidence_ref", "model_deployment_ref", "model_name",
        "model_version", "skill_revision", "skill_delivery",
    ):
        _text(runtime[key], f"runtime.{key}")
    _sha256(runtime["validation_config_sha256"], "runtime.validation_config_sha256")
    _sha256(runtime["released_config_sha256"], "runtime.released_config_sha256")
    _sha256(runtime["memory_configuration_sha256"], "runtime.memory_configuration_sha256")
    _sha256(runtime["instructions_sha256"], "runtime.instructions_sha256")
    _sha256(runtime["skill_sha256"], "runtime.skill_sha256")
    _https_url(runtime["toolbox_mcp_url"], "runtime.toolbox_mcp_url")
    _https_url(runtime["upstream_target"], "runtime.upstream_target")
    if not isinstance(runtime["upstream_tools"], list) or not all(
        isinstance(item, str) and item for item in runtime["upstream_tools"]
    ):
        raise ContractError("upstream_tools must be the observed nonempty allowlist")
    if not isinstance(runtime["effective_tool_names"], list) or not all(
        isinstance(item, str) and item for item in runtime["effective_tool_names"]
    ):
        raise ContractError("effective_tool_names must be the observed nonempty allowlist")

    checks = evidence["checks"]
    required_checks = {"WD02", "WD03", "WD04"}
    if not isinstance(checks, dict) or set(checks) != required_checks:
        raise ContractError("Validation must include WD02, WD03 and WD04")
    for check_id, check in checks.items():
        _object(check, {"status", "evidence_id"}, f"checks.{check_id}")
        if check["status"] != "passed":
            raise ContractError(f"{check_id} did not pass")
        _evidence_id(check["evidence_id"], f"checks.{check_id}.evidence_id")

    tool_calls = evidence["tool_calls"]
    if not isinstance(tool_calls, list) or len(tool_calls) < 2:
        raise ContractError("Record separate approved and denied MCP calls")
    decisions = set()
    approval_ids = set()
    response_ids = set()
    allowed = set(manifest["toolbox"]["tool_map"].values())
    for index, call in enumerate(tool_calls):
        _object(
            call,
            {
                "decision", "tool_name", "arguments_sha256", "response_id",
                "conversation_id", "approval_request_id", "trace_id",
                "continuation_conversation_id", "execution_id", "toolbox_version",
            },
            f"tool_calls[{index}]",
        )
        decision = call["decision"]
        if not isinstance(decision, str) or decision not in {"approved", "denied"}:
            raise ContractError("Record an actual human approval or denial for each tool request")
        if not isinstance(call["tool_name"], str) or call["tool_name"] not in allowed:
            raise ContractError("A tool call is outside the reviewed effective allowlist")
        _sha256(call["arguments_sha256"], f"tool_calls[{index}].arguments_sha256")
        for key in ("tool_name", "response_id", "conversation_id", "approval_request_id", "trace_id"):
            _evidence_id(call[key], f"tool_calls[{index}].{key}")
        if call["continuation_conversation_id"] != call["conversation_id"]:
            raise ContractError("Approval continuation must stay in the same managed Conversation")
        _evidence_id(
            call["continuation_conversation_id"],
            f"tool_calls[{index}].continuation_conversation_id",
        )
        if (
            call["approval_request_id"] in approval_ids
            or call["response_id"] in response_ids
        ):
            raise ContractError("Each approval and response must identify a distinct tool request")
        approval_ids.add(call["approval_request_id"])
        response_ids.add(call["response_id"])
        if call["toolbox_version"] != manifest["toolbox"]["version"]:
            raise ContractError("Tool call used an unpinned Toolbox version")
        if decision == "approved":
            _evidence_id(call["execution_id"], f"tool_calls[{index}].execution_id")
        elif call["execution_id"] is not None:
            raise ContractError("A denied request must not have an execution ID")
        decisions.add(decision)
    if decisions != {"approved", "denied"}:
        raise ContractError("Both an actual approved call and a denied call are required")
    return True


def validate_release_evidence(
    manifest,
    validation,
    release,
    *,
    repository,
    default_branch,
    current_commit,
    latest_sha,
    latest_attempt,
):
    validate_validation_evidence(
        manifest,
        validation,
        repository=repository,
        default_branch=default_branch,
        current_commit=current_commit,
        latest_sha=latest_sha,
        latest_attempt=latest_attempt,
    )
    _object(
        release,
        {
            "schema_version", "status", "source_commit", "manifest_sha256",
            "ci_run_id", "validation_candidate_version", "release_config_sha256",
            "released_agent_name", "released_agent_version",
            "stable_endpoint", "endpoint_source", "consumer_test",
        },
        "release evidence",
    )
    consumer = _object(
        release["consumer_test"],
        {"status", "response_id", "conversation_id", "trace_id", "evidence_id", "agent_version"},
        "consumer_test",
    )
    released_version = release["released_agent_version"]
    if (
        type(release["schema_version"]) is not int
        or release["schema_version"] != 1
        or release["status"] != "passed"
        or release["source_commit"] != validation["source_commit"]
        or release["manifest_sha256"] != validation["manifest_sha256"]
        or release["ci_run_id"] != validation["ci_run"]["id"]
        or release["validation_candidate_version"] != validation["runtime"]["validation_agent_version"]
        or release["released_agent_name"] != manifest["released_agent"]["name"]
        or not isinstance(released_version, str)
        or not released_version
        or released_version == manifest["released_agent"]["version"]
        or release["release_config_sha256"] != manifest["configuration_sha256"]
        or release["stable_endpoint"] != manifest["released_agent"]["stable_endpoint"]
        or release["endpoint_source"] != "service-read-back"
        or release["stable_endpoint"] == manifest["toolbox"]["mcp_url"]
        or consumer["status"] != "passed"
        or consumer["agent_version"] != released_version
    ):
        raise ContractError("Release evidence is not linked to the validated configuration and consumer path")
    for key in ("response_id", "conversation_id", "trace_id", "evidence_id", "agent_version"):
        _evidence_id(consumer[key], f"consumer_test.{key}")
    return True


def _read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_manifest_files(manifest, root="."):
    validate_manifest(manifest)
    root_path = Path(root).resolve()
    student_root = (root_path / "student").resolve()
    for path_key, hash_value, label in (
        (
            "configuration_source_path",
            manifest["configuration_sha256"],
            "configuration",
        ),
        (
            "instructions.source_path",
            manifest["instructions"]["sha256"],
            "instructions",
        ),
    ):
        relative = (
            manifest["instructions"]["source_path"]
            if path_key == "instructions.source_path"
            else manifest[path_key]
        )
        path = (root_path / relative).resolve()
        if not path.is_relative_to(student_root) or not path.is_file():
            raise ContractError(f"{label} file must exist under student/")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != hash_value:
            raise ContractError(f"{label} file hash differs from the reviewed manifest")
    return manifest


def write_ci_record(commit, manifest_path, output_path):
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise ContractError("CI commit must be a full Git SHA")
    manifest_file = Path(manifest_path)
    manifest_hash = None
    status = "contract-suite-only"
    if manifest_file.is_file():
        manifest = _read(manifest_file)
        if isinstance(manifest, dict) and "source_agent_name" in manifest:
            validate_capture_files(
                manifest_file,
                manifest_file.parent / "agent-definition.json",
            )
            status = "capture-package-passed"
        else:
            validate_manifest_files(manifest)
            status = "manifest-contract-passed"
        manifest_hash = canonical_sha256(manifest)
    record = {
        "schema_version": 1,
        "status": status,
        "eligible_for_release": False,
        "source_commit": commit,
        "manifest_sha256": manifest_hash,
        "cases_sha256": validation_cases_sha256(),
    }
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return record


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    capture_parser = subparsers.add_parser("check-capture")
    capture_parser.add_argument("manifest")
    capture_parser.add_argument("definition")
    capture_parser.add_argument("--production-agent")
    manifest_parser = subparsers.add_parser("check-manifest")
    manifest_parser.add_argument("manifest")
    record_parser = subparsers.add_parser("write-ci-record")
    record_parser.add_argument("--commit", required=True)
    record_parser.add_argument("--manifest", required=True)
    record_parser.add_argument("--output", required=True)
    validation_parser = subparsers.add_parser("check-validation")
    validation_parser.add_argument("manifest")
    validation_parser.add_argument("evidence")
    release_parser = subparsers.add_parser("check-release")
    release_parser.add_argument("manifest")
    release_parser.add_argument("validation")
    release_parser.add_argument("release")
    for parser_with_context in (validation_parser, release_parser):
        parser_with_context.add_argument("--repository", required=True)
        parser_with_context.add_argument("--default-branch", required=True)
        parser_with_context.add_argument("--current-commit", required=True)
        parser_with_context.add_argument("--latest-sha", required=True)
        parser_with_context.add_argument("--latest-attempt", required=True, type=int)
    args = parser.parse_args(argv)
    try:
        manifest = (
            _read(args.manifest)
            if args.command in {"check-validation", "check-release", "check-manifest"}
            else None
        )
        if args.command == "check-capture":
            validate_capture_files(
                args.manifest, args.definition,
                expected_production_agent=args.production_agent,
            )
            print("Captured Dev configuration and Prod target passed offline checks.")
        elif args.command == "check-manifest":
            manifest = _read(args.manifest)
            validate_manifest_files(manifest)
            print(f"Manifest structure passed; SHA-256 {canonical_sha256(manifest)}")
        elif args.command == "write-ci-record":
            record = write_ci_record(args.commit, args.manifest, args.output)
            print(f"Offline CI record written with status {record['status']}.")
        elif args.command == "check-validation":
            evidence = _read(args.evidence)
            ci = evidence["ci_run"]
            validate_manifest_files(manifest)
            validate_validation_evidence(
                manifest,
                evidence,
                repository=args.repository,
                default_branch=args.default_branch,
                current_commit=args.current_commit,
                latest_sha=args.latest_sha,
                latest_attempt=args.latest_attempt,
            )
            print("Validation evidence is internally consistent; live evidence still needs review.")
        else:
            validation = _read(args.validation)
            release = _read(args.release)
            ci = validation["ci_run"]
            validate_manifest_files(manifest)
            validate_release_evidence(
                manifest,
                validation,
                release,
                repository=args.repository,
                default_branch=args.default_branch,
                current_commit=args.current_commit,
                latest_sha=args.latest_sha,
                latest_attempt=args.latest_attempt,
            )
            print("Release evidence is internally consistent; stable-path behavior still needs review.")
        return 0
    except (ContractError, KeyError, OSError, json.JSONDecodeError) as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
