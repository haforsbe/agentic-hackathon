"""Narrow Microsoft Foundry cloud stages for the optional Weather delivery lab."""

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, quote, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen

from workshop.weather_delivery.contract import (
    ContractError,
    canonical_sha256,
    validate_manifest,
    validate_manifest_files,
    validate_validation_evidence,
)


class StageBlocked(RuntimeError):
    """A cloud stage cannot safely continue with the observed interface or evidence."""

    def __init__(self, message, partial_evidence=None):
        self.partial_evidence = partial_evidence or {}
        super().__init__(message)


class FoundryRequestError(StageBlocked):
    def __init__(self, status):
        self.status = status
        super().__init__(f"Foundry request failed ({status}); no automatic retry")


def _require(condition, message):
    if not condition:
        raise StageBlocked(message)


def _token_claims(token):
    try:
        payload = token.split(".")[1]
        return json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
    except (IndexError, ValueError, json.JSONDecodeError) as error:
        raise StageBlocked("Azure CLI returned a token with unreadable identity claims") from error


def verify_github_oidc(request_url, request_token, expected_subject, opener=urlopen):
    parts = urlsplit(request_url)
    _require(
        parts.scheme == "https"
        and parts.hostname
        and parts.hostname.casefold().endswith(".actions.githubusercontent.com")
        and parts.username is None
        and parts.password is None
        and not parts.fragment,
        "GitHub OIDC request URL must use the GitHub Actions HTTPS host",
    )
    query = [
        (key, value)
        for key, value in parse_qsl(parts.query, keep_blank_values=True)
        if key != "audience"
    ]
    query.append(("audience", "api://AzureADTokenExchange"))
    request = Request(
        urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), "")),
        headers={"Authorization": f"Bearer {request_token}"},
    )
    with opener(request, timeout=30) as response:
        payload = json.load(response)
    _require(isinstance(payload, dict), "GitHub OIDC endpoint returned an invalid response")
    token = payload.get("value")
    _require(isinstance(token, str), "GitHub OIDC endpoint returned no token")
    claims = _token_claims(token)
    audience = claims.get("aud")
    audiences = audience if isinstance(audience, list) else [audience]
    _require(
        claims.get("iss") == "https://token.actions.githubusercontent.com"
        and "api://AzureADTokenExchange" in audiences
        and claims.get("sub") == expected_subject
        and type(claims.get("exp")) in (int, float)
        and claims["exp"] > time.time(),
        "GitHub OIDC token does not match the configured subject, audience and expiry",
    )
    return claims["sub"]


def azure_cli_token(subscription, client_id, tenant_id, command=subprocess.run):
    result = command(
        [
            "az", "account", "get-access-token", "--subscription", subscription,
            "--resource", "https://ai.azure.com", "--query", "accessToken", "--output", "tsv",
        ],
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )
    token = result.stdout.strip()
    claims = _token_claims(token)
    _require(
        claims.get("tid") == tenant_id
        and client_id.casefold() in {
            str(claims.get("appid", "")).casefold(),
            str(claims.get("azp", "")).casefold(),
        },
        "Foundry access token identity differs from the configured CI application",
    )
    return token


class FoundryApi:
    """Small, no-retry client for documented Foundry agent and Responses operations."""

    def __init__(self, project_endpoint, token, opener=urlopen):
        parsed = urlsplit(project_endpoint)
        _require(
            parsed.scheme == "https"
            and parsed.hostname
            and parsed.username is None
            and parsed.password is None
            and parsed.query == ""
            and parsed.fragment == ""
            and parsed.path.startswith("/api/projects/"),
            "Use the exact HTTPS Microsoft Foundry Project Endpoint",
        )
        self.endpoint = project_endpoint.rstrip("/")
        self.token = token
        self.opener = opener

    def request(self, path, body=None, *, method=None, content_type="application/json"):
        request = Request(
            self.endpoint + path,
            data=None if body is None else json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": content_type,
            },
            method=method or ("GET" if body is None else "POST"),
        )
        try:
            with self.opener(request, timeout=60) as response:
                raw = response.read()
                payload = json.loads(raw) if raw else {}
                _require(isinstance(payload, dict), "Foundry returned a non-object response")
                return payload
        except HTTPError as error:
            raise FoundryRequestError(error.code) from error
        except (URLError, TimeoutError, json.JSONDecodeError) as error:
            raise StageBlocked(
                f"Foundry request failed ({type(error).__name__}); no automatic retry"
            ) from error

    def get_existing_agent(self, agent_name):
        try:
            return self.get_agent(agent_name)
        except FoundryRequestError as error:
            if error.status == 404:
                return None
            raise

    def create_agent(self, agent_name, definition):
        return self.request(
            "/agents?api-version=v1",
            {"name": agent_name, "definition": definition},
        )

    def get_version(self, agent_name, version):
        return self.request(
            f"/agents/{quote(agent_name, safe='')}/versions/{quote(str(version), safe='')}?api-version=v1"
        )

    def create_version(self, agent_name, definition):
        return self.request(
            f"/agents/{quote(agent_name, safe='')}/versions?api-version=v1",
            {"definition": definition},
        )

    def get_agent(self, agent_name):
        return self.request(f"/agents/{quote(agent_name, safe='')}?api-version=v1")

    def create_conversation(self):
        return self.request("/openai/v1/conversations", {})

    def response(self, body):
        return self.request("/openai/v1/responses", body)

    def get_response(self, response_id):
        return self.request(f"/openai/v1/responses/{quote(response_id, safe='')}")

    def pin_agent_version(self, agent_name, version):
        rules = [{
            "type": "FixedRatio",
            "agent_version": str(version),
            "traffic_percentage": 100,
        }]
        self.request(
            f"/agents/{quote(agent_name, safe='')}?api-version=v1",
            {"agent_endpoint": {"version_selector": {"version_selection_rules": rules}}},
            method="PATCH",
            content_type="application/merge-patch+json",
        )
        observed = self.get_agent(agent_name)
        actual = (
            observed.get("agent_endpoint", {})
            .get("version_selector", {})
            .get("version_selection_rules")
        )
        _require(actual == rules, "Foundry did not read back the requested stable-version selector")
        return observed

    def invoke_stable_endpoint(self, endpoint, agent_name, body):
        _validate_stable_endpoint_url(self.endpoint, endpoint, agent_name)
        request = Request(
            endpoint,
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with self.opener(request, timeout=60) as response:
                raw = response.read()
                payload = json.loads(raw) if raw else {}
                _require(isinstance(payload, dict), "Stable Agent Endpoint returned a non-object response")
                return payload
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
            status = getattr(error, "code", None)
            raise StageBlocked(
                f"Stable Agent Endpoint request failed ({status or type(error).__name__}); no automatic retry"
            ) from error


def _read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _validate_stable_endpoint_url(project_endpoint, endpoint, agent_name):
    parsed = urlsplit(endpoint)
    project = urlsplit(project_endpoint)
    expected_path = (
        project.path.rstrip("/")
        + f"/agents/{quote(agent_name, safe='')}/endpoint/protocols/openai/responses"
    )
    _require(
        parsed.scheme == "https"
        and parsed.netloc.casefold() == project.netloc.casefold()
        and parsed.username is None
        and parsed.password is None
        and parsed.query == ""
        and parsed.fragment == ""
        and parsed.path == expected_path,
        "Use the service-returned Stable Agent Endpoint, not a project or Toolbox URL",
    )


def _reject_credentials(value):
    sensitive_names = {
        "authorization", "headers", "password", "secret", "token",
        "api_key", "apikey", "credential", "connection_string",
    }
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).casefold().replace("-", "_")
            _require(
                normalized not in sensitive_names
                and not normalized.endswith(("_token", "_secret", "_password", "_api_key")),
                "Agent configuration contains a credential-like field; capture is blocked",
            )
            _reject_credentials(child)
    elif isinstance(value, list):
        for child in value:
            _reject_credentials(child)


def _definition_from_file(path, manifest):
    configuration = _read(path)
    _require(
        isinstance(configuration, dict)
        and set(configuration) == {"schema_version", "definition"}
        and type(configuration["schema_version"]) is int
        and configuration["schema_version"] == 1,
        "Captured agent file has an unsupported schema",
    )
    definition = configuration["definition"]
    _reject_credentials(definition)
    _validate_tool_binding(definition, manifest)
    return definition


def _validate_tool_binding(definition, manifest):
    _require(
        isinstance(definition, dict)
        and definition.get("kind") == "prompt"
        and isinstance(definition.get("instructions"), str)
        and definition.get("model") == manifest["model_policy"]["deployment_ref"],
        "Agent definition differs from the reviewed prompt/model policy",
    )
    tools = definition.get("tools", [])
    _require(isinstance(tools, list) and len(tools) == 1, "Expected exactly one reviewed Weather Toolbox")
    tool = tools[0]
    allowed = {
        "type", "server_label", "server_url", "project_connection_id",
        "allowed_tools", "require_approval",
    }
    _require(
        isinstance(tool, dict)
        and set(tool) == allowed
        and tool["type"] == "mcp"
        and tool["server_url"] == manifest["toolbox"]["mcp_url"]
        and tool["project_connection_id"] == manifest["toolbox"]["toolbox_auth_connection_ref"]
        and tool["require_approval"] == "always"
        and isinstance(tool["allowed_tools"], list)
        and all(isinstance(item, str) for item in tool["allowed_tools"])
        and sorted(tool["allowed_tools"]) == sorted(manifest["toolbox"]["tool_map"].values())
        and isinstance(tool["server_label"], str)
        and bool(tool["server_label"]),
        "Agent Toolbox binding is missing, unverified, or differs from the manifest",
    )
    return tool


def capture_agent(api, agent_name, version, output):
    observed = api.get_version(agent_name, version)
    _require(str(observed.get("version")) == str(version), "Foundry returned a different agent version")
    definition = observed.get("definition")
    _require(isinstance(definition, dict), "Foundry returned no agent definition")
    _reject_credentials(definition)
    config = {"schema_version": 1, "definition": definition}
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(config, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "agent_name": agent_name,
        "agent_version": str(version),
        "configuration_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "captured_path": str(target),
        "review_required": True,
    }


def prepare_candidate(api, manifest, definition_path, *, binding_verified, approved):
    _require(
        binding_verified is True,
        "Verify the current-project Toolbox-authentication connection before candidate creation",
    )
    _require(approved is True, "Validation-agent creation requires explicit current-step approval")
    validate_manifest(manifest)
    definition = _definition_from_file(definition_path, manifest)
    candidate_name = manifest["validation_agent"]["name"]
    released_name = manifest["released_agent"]["name"]
    _require(candidate_name != released_name, "Candidate and released Weather agents must be separate")
    existing = api.get_existing_agent(candidate_name)
    if existing is None:
        created = api.create_agent(candidate_name, definition)
        _require(
            created.get("name") == candidate_name,
            "Foundry returned a different validation agent identity",
        )
        versions = created.get("versions")
        latest = versions.get("latest") if isinstance(versions, dict) else None
        version = created.get("version")
        if version is None and isinstance(latest, dict):
            version = latest.get("version")
    else:
        _require(
            existing.get("name") == candidate_name,
            "Foundry returned a different validation agent identity",
        )
        versions = existing.get("versions")
        latest = versions.get("latest") if isinstance(versions, dict) else None
        _require(
            isinstance(latest, dict)
            and isinstance(latest.get("version"), (str, int))
            and latest.get("definition") == definition,
            "Validation agent already exists with another configuration; inspect it before any update",
        )
        version = latest["version"]
    _require(isinstance(version, (str, int)) and str(version), "Foundry returned no candidate version")
    observed = api.get_version(candidate_name, str(version))
    _require(observed.get("definition") == definition, "Candidate version read-back differs from reviewed configuration")
    return {
        "candidate_agent": candidate_name,
        "candidate_version": str(version),
        "configuration_sha256": manifest["configuration_sha256"],
        "created_agent": existing is None,
    }


def prepare_release_version(api, manifest, definition_path, validation_evidence, *, approved, **provenance):
    _require(approved is True, "Creating a released-agent version requires explicit current-step approval")
    validate_manifest(manifest)
    validate_validation_evidence(manifest, validation_evidence, **provenance)
    definition = _definition_from_file(definition_path, manifest)
    release_name = manifest["released_agent"]["name"]
    _require(
        release_name != manifest["validation_agent"]["name"],
        "Validation and released Weather agents must be separate",
    )
    created = api.create_version(release_name, definition)
    version = created.get("version")
    _require(isinstance(version, (str, int)) and str(version), "Foundry returned no release version")
    observed = api.get_version(release_name, str(version))
    _require(observed.get("definition") == definition, "Release version read-back differs from reviewed configuration")
    return {"released_agent": release_name, "released_version": str(version), "configuration_sha256": manifest["configuration_sha256"]}


def _pending_approval(response, manifest, expected_server_label=None):
    _require(isinstance(response, dict), "Foundry response is not a JSON object")
    _require(
        response.get("status") == "requires_action",
        "Foundry response is not waiting for a human MCP approval",
    )
    output = response.get("output")
    _require(
        isinstance(output, list) and all(isinstance(item, dict) for item in output),
        "Foundry response has no valid output list",
    )
    requests = [item for item in output if item.get("type") == "mcp_approval_request"]
    _require(len(requests) == 1, "Expected exactly one pending human MCP approval request")
    item = requests[0]
    allowed = set(manifest["toolbox"]["tool_map"].values())
    _require(item.get("name") in allowed, "Pending request names a tool outside the reviewed Toolbox allowlist")
    _require(item.get("server_label"), "Pending request has no server label")
    _require(
        isinstance(response.get("id"), str)
        and isinstance(item.get("id"), str)
        and item["id"],
        "Foundry response omitted its response or approval request ID",
    )
    if expected_server_label is not None:
        _require(
            item["server_label"] == expected_server_label,
            "Pending request server label differs from the reviewed agent binding",
        )
    raw_arguments = item.get("arguments")
    arguments = json.loads(raw_arguments) if isinstance(raw_arguments, str) else raw_arguments
    _require(isinstance(arguments, dict), "Pending MCP arguments are not a JSON object")
    conversation = response.get("conversation")
    conversation_id = conversation.get("id") if isinstance(conversation, dict) else conversation
    _require(isinstance(conversation_id, str) and conversation_id, "Foundry response has no managed Conversation ID")
    return {
        "response_id": response.get("id"),
        "conversation_id": conversation_id,
        "approval_request_id": item.get("id"),
        "server_label": item["server_label"],
        "tool_name": item["name"],
        "arguments": arguments,
        "arguments_sha256": canonical_sha256(arguments),
    }


def start_tool_call(api, manifest, candidate_version, decision, *, spend_approved):
    _require(decision in {"approved", "denied"}, "Use the approved or denied public Weather test case")
    candidate = api.get_version(manifest["validation_agent"]["name"], candidate_version)
    _require(
        str(candidate.get("version")) == str(candidate_version)
        and isinstance(candidate.get("definition"), dict),
        "Foundry did not read back the selected validation candidate version",
    )
    binding = _validate_tool_binding(candidate["definition"], manifest)
    _require(spend_approved is True, "Model/tool call requires explicit current-step spend approval")
    conversation = api.create_conversation()
    conversation_id = conversation.get("id")
    _require(isinstance(conversation_id, str) and conversation_id, "Foundry returned no managed Conversation")
    prompt = "Give me the weather forecast for New York, NY for the next available forecast period."
    response = api.response({
        "agent_reference": {
            "type": "agent_reference",
            "name": manifest["validation_agent"]["name"],
            "version": str(candidate_version),
        },
        "input": prompt,
        "store": True,
        "conversation": conversation_id,
        "max_output_tokens": 1024,
    })
    try:
        pending = _pending_approval(response, manifest, binding["server_label"])
    except StageBlocked as error:
        if isinstance(response, dict):
            output = response.get("output")
            error.partial_evidence = {
                "response_id": response.get("id"),
                "conversation_id": conversation_id,
                "response_status": response.get("status"),
                "output_types": (
                    [item.get("type") for item in output if isinstance(item, dict)]
                    if isinstance(output, list)
                    else []
                ),
            }
        raise
    _require(pending["conversation_id"] == conversation_id, "Tool request escaped its managed Conversation")
    pending["decision_case"] = decision
    pending["candidate_agent"] = manifest["validation_agent"]["name"]
    pending["candidate_version"] = str(candidate_version)
    pending["prompt_sha256"] = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    pending["review_the_exact_arguments_before_continuing"] = True
    pending.pop("arguments")
    return pending


def continue_tool_call(
    api,
    manifest,
    candidate_version,
    response_id,
    approval_request_id,
    approve,
    *,
    spend_approved,
):
    _require(type(approve) is bool, "A separate explicit per-call approve/deny decision is required")
    candidate = api.get_version(manifest["validation_agent"]["name"], candidate_version)
    _require(
        str(candidate.get("version")) == str(candidate_version)
        and isinstance(candidate.get("definition"), dict),
        "Foundry did not read back the selected validation candidate version",
    )
    binding = _validate_tool_binding(candidate["definition"], manifest)
    prior = api.get_response(response_id)
    pending = _pending_approval(prior, manifest, binding["server_label"])
    _require(pending["response_id"] == response_id, "Retrieved response ID differs")
    _require(pending["approval_request_id"] == approval_request_id, "Pending approval request ID differs")
    _require(spend_approved is True, "Approval continuation requires explicit current-step spend approval")
    continued = api.response({
        "previous_response_id": response_id,
        "conversation": pending["conversation_id"],
        "store": True,
        "input": [{
            "type": "mcp_approval_response",
            "approval_request_id": approval_request_id,
            "approve": approve,
        }],
    })
    if not isinstance(continued, dict) or continued.get("status") != "completed":
        raise StageBlocked(
            "Approval continuation did not complete; preserve the pending response and inspect read-back",
            partial_evidence={
                "prior_response_id": response_id,
                "approval_request_id": approval_request_id,
                "response_id": continued.get("id") if isinstance(continued, dict) else None,
                "response_status": continued.get("status") if isinstance(continued, dict) else None,
            },
        )
    continued_conversation = continued.get("conversation")
    continued_conversation_id = (
        continued_conversation.get("id") if isinstance(continued_conversation, dict)
        else continued_conversation
    )
    _require(
        continued_conversation_id == pending["conversation_id"],
        "Approval continuation did not stay in the original managed Conversation",
    )
    output = continued.get("output")
    _require(
        isinstance(output, list) and all(isinstance(item, dict) for item in output),
        "Approval continuation returned no valid output list",
    )
    tool_calls = [item for item in output if item.get("type") == "mcp_call"]
    _require(
        bool(tool_calls) == approve,
        "Tool execution evidence does not match the explicit approve/deny decision",
    )
    result = {
        "response_id": continued.get("id"),
        "conversation_id": continued_conversation_id,
        "candidate_agent": manifest["validation_agent"]["name"],
        "candidate_version": str(candidate_version),
        "approval_request_id": approval_request_id,
        "decision": "approved" if approve else "denied",
        "arguments_sha256": pending["arguments_sha256"],
        "tool_name": pending["tool_name"],
    }
    if approve:
        _require(len(tool_calls) == 1, "Expected exactly one approved MCP execution")
        execution_id = tool_calls[0].get("id")
        _require(isinstance(execution_id, str) and execution_id, "Approved call omitted its execution ID")
        result["execution_id"] = execution_id
    else:
        result["execution_id"] = None
    _require(
        isinstance(result["response_id"], str) and result["response_id"],
        "Approval continuation omitted its response ID",
    )
    return result


def pin_release(api, manifest, validation_evidence, release_version, *, repository, default_branch, current_commit, latest_sha, latest_attempt, approved):
    _require(approved is True, "Stable endpoint change requires explicit current-step approval")
    validate_manifest(manifest)
    validate_validation_evidence(
        manifest,
        validation_evidence,
        repository=repository,
        default_branch=default_branch,
        current_commit=current_commit,
        latest_sha=latest_sha,
        latest_attempt=latest_attempt,
    )
    _require(
        validation_evidence["runtime"]["released_agent_name"] == manifest["released_agent"]["name"],
        "Validation evidence is not for the released Weather agent",
    )
    _require(
        isinstance(release_version, str)
        and release_version
        and release_version != manifest["released_agent"]["version"],
        "Pin only a new service-returned version on the released Weather agent",
    )
    release_config = api.get_version(manifest["released_agent"]["name"], release_version)
    _require(
        release_config.get("definition")
        == _definition_from_file(
            manifest["configuration_source_path"],
            manifest,
        ),
        "Released version differs from the reviewed configuration",
    )
    _require(
        isinstance(manifest["released_agent"]["stable_endpoint"], str),
        "The reviewed Stable Agent Endpoint is missing",
    )
    _validate_stable_endpoint_url(
        api.endpoint,
        manifest["released_agent"]["stable_endpoint"],
        manifest["released_agent"]["name"],
    )
    before = api.get_agent(manifest["released_agent"]["name"])
    _require(
        before.get("name") == manifest["released_agent"]["name"],
        "Foundry returned a different released agent identity",
    )
    observed = api.pin_agent_version(manifest["released_agent"]["name"], release_version)
    _require(observed.get("name") == manifest["released_agent"]["name"], "Foundry returned a different released agent")
    return {
        "agent_name": observed["name"],
        "selected_release_version": release_version,
        "endpoint": manifest["released_agent"]["stable_endpoint"],
        "version_selector": observed.get("agent_endpoint", {}).get("version_selector"),
    }


def test_stable_endpoint(api, manifest, expected_version, prompt):
    observed = api.get_agent(manifest["released_agent"]["name"])
    _require(
        observed.get("name") == manifest["released_agent"]["name"],
        "Foundry returned a different released agent identity",
    )
    endpoint = manifest["released_agent"]["stable_endpoint"]
    _validate_stable_endpoint_url(api.endpoint, endpoint, manifest["released_agent"]["name"])
    selector = (
        observed.get("agent_endpoint", {})
        .get("version_selector", {})
        .get("version_selection_rules")
    )
    _require(
        selector == [{
            "type": "FixedRatio",
            "agent_version": str(expected_version),
            "traffic_percentage": 100,
        }],
        "Stable endpoint is not pinned to the validated released version",
    )
    response = api.invoke_stable_endpoint(
        endpoint,
        manifest["released_agent"]["name"],
        {"input": prompt, "store": True, "max_output_tokens": 1024},
    )
    conversation = response.get("conversation")
    conversation_id = conversation.get("id") if isinstance(conversation, dict) else conversation
    _require(
        isinstance(response.get("id"), str)
        and isinstance(conversation_id, str)
        and conversation_id,
        "Stable endpoint response omitted its response or Conversation identifier",
    )
    return {
        "response_id": response["id"],
        "conversation_id": conversation_id,
        "agent_version": str(expected_version),
        "trace_evidence_required": True,
    }


def _add_provenance_arguments(parser):
    parser.add_argument("--repository", required=True)
    parser.add_argument("--default-branch", required=True)
    parser.add_argument("--current-commit", required=True)
    parser.add_argument("--latest-sha", required=True)
    parser.add_argument("--latest-attempt", required=True, type=int)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    oidc = sub.add_parser("verify-oidc")
    oidc.add_argument("--expected-subject", default=None)
    capture = sub.add_parser("capture")
    capture.add_argument("--agent-name", required=True)
    capture.add_argument("--version", required=True)
    capture.add_argument("--output", required=True)
    capture.add_argument("--record", required=True)
    prepare = sub.add_parser("prepare")
    prepare.add_argument("--manifest", required=True)
    prepare.add_argument("--definition", required=True)
    prepare.add_argument("--binding-verified", choices=("yes", "no"), required=True)
    prepare.add_argument("--approved", choices=("yes", "no"), required=True)
    prepare.add_argument("--output", required=True)
    prepare_release = sub.add_parser("prepare-release")
    prepare_release.add_argument("--manifest", required=True)
    prepare_release.add_argument("--definition", required=True)
    prepare_release.add_argument("--validation-evidence", required=True)
    prepare_release.add_argument("--approved", choices=("yes", "no"), required=True)
    prepare_release.add_argument("--output", required=True)
    _add_provenance_arguments(prepare_release)
    start = sub.add_parser("start")
    start.add_argument("--manifest", required=True)
    start.add_argument("--candidate-version", required=True)
    start.add_argument("--decision-case", choices=("approved", "denied"), required=True)
    start.add_argument("--spend-approved", choices=("yes", "no"), required=True)
    start.add_argument("--output", required=True)
    cont = sub.add_parser("continue")
    cont.add_argument("--manifest", required=True)
    cont.add_argument("--candidate-version", required=True)
    cont.add_argument("--response-id", required=True)
    cont.add_argument("--approval-request-id", required=True)
    cont.add_argument("--approve", choices=("yes", "no"), required=True)
    cont.add_argument("--spend-approved", choices=("yes", "no"), required=True)
    cont.add_argument("--output", required=True)
    release = sub.add_parser("pin-release")
    release.add_argument("--manifest", required=True)
    release.add_argument("--release-version", required=True)
    release.add_argument("--validation-evidence", required=True)
    release.add_argument("--approved", choices=("yes", "no"), required=True)
    release.add_argument("--output", required=True)
    _add_provenance_arguments(release)
    consumer = sub.add_parser("consumer-test")
    consumer.add_argument("--manifest", required=True)
    consumer.add_argument("--release-version", required=True)
    consumer.add_argument("--prompt", required=True)
    consumer.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    output_path = getattr(args, "record", None) if args.command == "capture" else getattr(args, "output", None)
    try:
        if args.command == "verify-oidc":
            subject = verify_github_oidc(
                os.environ["ACTIONS_ID_TOKEN_REQUEST_URL"],
                os.environ["ACTIONS_ID_TOKEN_REQUEST_TOKEN"],
                args.expected_subject or os.environ["EXPECTED_OIDC_SUBJECT"],
            )
            print(f"Verified GitHub OIDC subject: {subject}")
            return 0
        subscription = os.environ["AZURE_SUBSCRIPTION_ID"]
        client_id = os.environ["AZURE_CLIENT_ID"]
        tenant_id = os.environ["AZURE_TENANT_ID"]
        verify_github_oidc(
            os.environ["ACTIONS_ID_TOKEN_REQUEST_URL"],
            os.environ["ACTIONS_ID_TOKEN_REQUEST_TOKEN"],
            os.environ["EXPECTED_OIDC_SUBJECT"],
        )
        token = azure_cli_token(subscription, client_id, tenant_id)
        api = FoundryApi(os.environ["FOUNDRY_PROJECT_ENDPOINT"], token)
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        _require(
            not Path(output_path).exists(),
            "Stage evidence already exists; inspect it and service read-back before any repeat",
        )
        stage_inputs = {
            key: value
            for key in (
                "agent_name", "version", "candidate_version", "decision_case",
                "response_id", "approval_request_id", "approve", "release_version",
                "approved", "spend_approved", "binding_verified",
            )
            if (value := getattr(args, key, None)) is not None
        }
        Path(output_path).write_text(
            json.dumps({
                "schema_version": 1,
                "state": "started_do_not_repeat_without_readback",
                "operation": args.command,
                "source_commit": os.environ.get("GITHUB_SHA"),
                "repository": os.environ.get("GITHUB_REPOSITORY"),
                "workflow_run_id": os.environ.get("GITHUB_RUN_ID"),
                "workflow_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
                "stage_inputs": stage_inputs,
            }, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        if args.command == "capture":
            result = capture_agent(api, args.agent_name, args.version, args.output)
        else:
            manifest = _read(args.manifest)
            validate_manifest_files(manifest)
            if args.command == "prepare":
                result = prepare_candidate(
                    api,
                    manifest,
                    args.definition,
                    binding_verified=args.binding_verified == "yes",
                    approved=args.approved == "yes",
                )
            elif args.command == "prepare-release":
                result = prepare_release_version(
                    api,
                    manifest,
                    args.definition,
                    _read(args.validation_evidence),
                    approved=args.approved == "yes",
                    repository=args.repository,
                    default_branch=args.default_branch,
                    current_commit=args.current_commit,
                    latest_sha=args.latest_sha,
                    latest_attempt=args.latest_attempt,
                )
            elif args.command == "start":
                result = start_tool_call(
                    api,
                    manifest,
                    args.candidate_version,
                    args.decision_case,
                    spend_approved=args.spend_approved == "yes",
                )
            elif args.command == "continue":
                result = continue_tool_call(
                    api,
                    manifest,
                    args.candidate_version,
                    args.response_id,
                    args.approval_request_id,
                    args.approve == "yes",
                    spend_approved=args.spend_approved == "yes",
                )
            elif args.command == "pin-release":
                result = pin_release(
                    api,
                    manifest,
                    _read(args.validation_evidence),
                    args.release_version,
                    repository=args.repository,
                    default_branch=args.default_branch,
                    current_commit=args.current_commit,
                    latest_sha=args.latest_sha,
                    latest_attempt=args.latest_attempt,
                    approved=args.approved == "yes",
                )
            else:
                result = test_stable_endpoint(api, manifest, args.release_version, args.prompt)
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        persisted = {
            "schema_version": 1,
            "state": "completed",
            "operation": args.command,
            "source_commit": os.environ.get("GITHUB_SHA"),
            "repository": os.environ.get("GITHUB_REPOSITORY"),
            "workflow_run_id": os.environ.get("GITHUB_RUN_ID"),
            "workflow_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
            **{key: value for key, value in result.items() if key != "arguments"},
        }
        Path(output_path).write_text(json.dumps(persisted, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (ContractError, StageBlocked, KeyError, OSError, subprocess.SubprocessError, json.JSONDecodeError) as error:
        if output_path and Path(output_path).is_file():
            try:
                record = _read(output_path)
                if record.get("state") == "started_do_not_repeat_without_readback":
                    record["state"] = "blocked_readback_required"
                    record["failure"] = str(error)
                    if isinstance(error, StageBlocked) and error.partial_evidence:
                        record["partial_evidence"] = error.partial_evidence
                    Path(output_path).write_text(
                        json.dumps(record, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8",
                    )
            except (OSError, json.JSONDecodeError) as preservation_error:
                print(
                    "PARTIAL EVIDENCE PRESERVATION FAILED: "
                    f"{type(preservation_error).__name__}",
                    file=sys.stderr,
                )
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
