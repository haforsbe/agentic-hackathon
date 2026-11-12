"""Bounded prompt-agent operations; no automatic sign-in, retries, or tool approval."""

import argparse
import base64
import copy
from datetime import datetime, timezone
from fnmatch import fnmatchcase
import importlib.metadata
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from time import perf_counter, time
from urllib.parse import urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[2]
OPERATIONS = {"inspect", "create-version", "run", "retrieve", "new-conversation", "continue"}
VERSIONS = {"azure-ai-projects": "2.6.1", "azure-identity": "1.25.3", "openai": "3.19.2"}
FOUNDRY_USER_DATA_EXCLUSIONS = {
    "Microsoft.CognitiveServices/accounts/AIServices/agents/endpoints/UserIdentityImpersonation/action",
    "Microsoft.CognitiveServices/accounts/OpenAI/fine-tunes-deployments/write",
    "Microsoft.CognitiveServices/accounts/AIServices/fine_tuning_deployments/write",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def now():
    return datetime.now(timezone.utc).isoformat()


def readiness():
    packages = {}
    for package, expected in VERSIONS.items():
        try:
            actual = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            actual = None
        packages[package] = {"expected": expected, "installed": actual, "matches": actual == expected}
    tools = {name: shutil.which(name) is not None for name in ("git", "az", "azd")}
    return {
        "tools": tools,
        "packages": packages,
        "prompt_runner_ready": tools["az"] and all(item["matches"] for item in packages.values()),
        "cloud_access": "unverified; this check makes no network requests",
        "later_capabilities": "Memory, skills, consumer identities and hosted runtime require facilitator rehearsal.",
    }


def local_path(value, folder):
    path = (ROOT / value).resolve()
    require(path.is_relative_to((ROOT / folder).resolve()), f"Path must be inside {folder}")
    return path


def normalized(definition):
    value = copy.deepcopy(definition)
    for tool in value.get("tools", []):
        allowed = tool.get("allowed_tools")
        if isinstance(allowed, dict):
            require(set(allowed) == {"tool_names"}, "Unexpected allowlist fields")
            tool["allowed_tools"] = allowed["tool_names"]
    return value


def load_plan(path):
    plan = json.loads(local_path(path, ".workshop").read_text(encoding="utf-8-sig"))
    require(plan["operation"] in OPERATIONS, "Unsupported operation")
    require(re.fullmatch(r"[a-zA-Z0-9_-]{1,80}", plan["run_id"]), "Invalid run identifier")
    require(plan.get("approval_reference"), "Record the current participant approval reference")
    require(plan.get("public_or_synthetic_data_only") is True, "Only public/synthetic evidence is supported")
    endpoint = urlparse(plan["endpoint"])
    require(
        endpoint.scheme == "https" and endpoint.hostname
        and endpoint.hostname.endswith(".services.ai.azure.com")
        and endpoint.username is None and endpoint.password is None
        and endpoint.port in (None, 443) and not endpoint.query and not endpoint.fragment
        and re.fullmatch(r"/api/projects/[A-Za-z0-9_.-]+", endpoint.path),
        "Use the exact supported public Foundry project endpoint",
    )
    require(Path(plan["azure_config_dir"]).is_absolute(), "Use an absolute isolated CLI profile")
    require(Path(plan["azure_config_dir"]).resolve() != (Path.home() / ".azure").resolve(),
            "Do not use the global Azure CLI profile")
    require(
        not Path(plan["azure_config_dir"]).resolve().is_relative_to(ROOT),
        "Keep the isolated CLI profile outside the repository",
    )
    require(plan.get("required_permissions"), "Supply verified operation-specific permission names")
    for permission in plan["required_permissions"]:
        require(permission["kind"] in ("actions", "dataActions"), "Invalid permission kind")
        require("*" not in permission["operation"], "Specify an exact required permission, not a wildcard")
    for key in ("account", "tenant", "subscription", "project_resource_id", "agent_name"):
        require(isinstance(plan.get(key), str) and plan[key], f"Missing {key}")
    resource_id = plan["project_resource_id"]
    require(
        resource_id.lower().startswith(f"/subscriptions/{plan['subscription']}/".lower())
        and resource_id.lower().endswith(f"/projects/{endpoint.path.rsplit('/', 1)[-1]}".lower()),
        "Project resource ID does not match the confirmed scope",
    )
    if plan["operation"] != "create-version":
        require(isinstance(plan.get("agent_version"), str) and plan["agent_version"], "Pin the agent version")
    config = json.loads(local_path(plan["configuration"], "student").read_text(encoding="utf-8"))
    require(config["name"] == plan["agent_name"], "Configuration names a different agent")
    require(config["definition"]["kind"] == "prompt", "Only ordinary prompt agents are supported")
    for tool in config["definition"].get("tools", []):
        require(
            tool.get("type") == "mcp" and tool.get("require_approval") == "always"
            and tool.get("allowed_tools"),
            "Runner supports only explicit MCP allowlists with approval always",
        )
        require(not any(tool.get(key) for key in ("authorization", "headers", "project_connection_id")),
                "Do not put credentials or authenticated connections in these public-service plans")
        require(tool["server_url"] in ("https://weather.datakoot.com/mcp", "https://mcp.travel.art/"),
                "Only the workshop's selected public MCP services are supported")
    if plan["operation"] in ("run", "continue"):
        require(type(plan.get("max_output_tokens")) is int and 16 <= plan["max_output_tokens"] <= 4096,
                "Set a bounded output limit between 16 and 4096")
    if plan["operation"] == "run":
        require(isinstance(plan.get("cases"), list) and 1 <= len(plan["cases"]) <= 12, "Use 1-12 approved cases")
        require(len({case["id"] for case in plan["cases"]}) == len(plan["cases"]), "Duplicate case identifiers")
        for case in plan["cases"]:
            require(isinstance(case["prompt"], str) and case["prompt"].strip(), "Empty prompt")
            require(case.get("conversation_id") is None or case["conversation_id"].startswith("conv_"),
                    "Use a service-returned Conversation ID")
            require(type(case.get("store", False)) is bool, "store must be a boolean")
            if config["definition"].get("tools"):
                require(case.get("store") is True,
                        "MCP tests need approved response storage for same-run retrieval/approval continuation")
        require(type(plan.get("max_requests")) is int and plan["max_requests"] == len(plan["cases"]),
                "Request budget must equal the displayed case count")
    if plan["operation"] in ("retrieve", "continue"):
        require(plan.get("response_id", "").startswith("resp_"), "Use a response ID, not a conversation/trace ID")
    if plan["operation"] == "continue":
        require("cases" not in plan, "A continuation permits one response, not a batch")
        require(type(plan.get("approve")) is bool, "Explicitly approve or deny this one tool request")
        require(plan.get("approval_request_id", "").startswith("mcpr_"), "Exact approval request ID required")
        require(plan.get("tool_name") and isinstance(plan.get("arguments"), dict), "Exact tool and arguments required")
    authorization_policy(plan)
    return plan, config


def authorization_policy(plan):
    policy = plan.get("authorization_policy", "operation-specific")
    require(policy in ("operation-specific", "foundry-user-data-access"), "Unsupported authorization policy")
    uses_conversation = plan["operation"] == "new-conversation" or (
        plan["operation"] == "run" and any(case.get("conversation_id") for case in plan["cases"])
    )
    require(not uses_conversation or policy == "foundry-user-data-access",
            "Managed Conversations require the documented foundry-user-data-access authorization policy")
    return policy


def cli(*args):
    executable = shutil.which("az")
    require(executable is not None, "Azure CLI unavailable")
    result = subprocess.run([executable, *args, "--output", "json", "--only-show-errors"],
                            capture_output=True, text=True, timeout=60)
    require(result.returncode == 0, "Azure CLI check failed; participant must resolve sign-in/access")
    return json.loads(result.stdout)


def check_cli(plan):
    account = cli("account", "show")
    require(
        account["user"]["name"].casefold() == plan["account"].casefold()
        and account["tenantId"] == plan["tenant"] and account["id"] == plan["subscription"],
        "Signed-in account, tenant or subscription differs; no identity switch performed",
    )


def permitted(grants, permission):
    kind, operation = permission["kind"], permission["operation"].lower()
    excluded = "notActions" if kind == "actions" else "notDataActions"
    return any(
        any(fnmatchcase(operation, pattern.lower()) for pattern in grant.get(kind, []))
        and not any(fnmatchcase(operation, pattern.lower()) for pattern in grant.get(excluded, []))
        for grant in grants
    )


def foundry_user_data_access(grants):
    allowed_exclusions = {operation.lower() for operation in FOUNDRY_USER_DATA_EXCLUSIONS}
    return any(
        any(pattern.lower() in ("*", "microsoft.cognitiveservices/*")
            for pattern in grant.get("dataActions", []))
        and all(pattern.lower() in allowed_exclusions for pattern in grant.get("notDataActions", []))
        for grant in grants
    )


def verify_permissions(plan, credential):
    policy = authorization_policy(plan)
    token = credential.get_token("https://management.azure.com/.default")
    request = Request(
        "https://management.azure.com" + plan["project_resource_id"]
        + "/providers/Microsoft.Authorization/permissions?api-version=2022-04-01",
        headers={"Authorization": "Bearer " + token.token},
    )
    with urlopen(request, timeout=60) as response:
        permissions = json.load(response)
    require(not permissions.get("nextLink"), "Permission pagination needs facilitator review")
    require(all(permitted(permissions["value"], item) for item in plan["required_permissions"]),
            "Required operation permission not verified; no write probe performed")
    verification = {"policy": policy, "required_permissions_verified": True}
    if policy == "foundry-user-data-access":
        require(foundry_user_data_access(permissions["value"]),
                "Documented Foundry User-equivalent data grant not verified; "
                "narrower or additionally restricted grants need facilitator review, not a role change or write probe")
        verification["foundry_user_equivalent_data_grant_verified"] = True
        verification["reference"] = "https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry"
    return verification


def verified_credential(plan):
    from azure.identity import AzureCliCredential

    inner = AzureCliCredential(tenant_id=plan["tenant"], process_timeout=60)

    class VerifiedCredential:
        def __init__(self):
            self.arm_token = None
            self.closed = False

        def get_token(self, *scopes, **kwargs):
            require(not self.closed, "Credential is closed")
            context = (os.getpid(), os.environ.get("AZURE_CONFIG_DIR"),
                       plan["tenant"], plan["account"], plan["subscription"])
            cacheable = scopes == ("https://management.azure.com/.default",) and not kwargs
            cached = self.arm_token
            self.arm_token = None
            if cacheable and cached and cached[2] == context and cached[1] > time() + 300:
                token = cached[0]
            else:
                token = inner.get_token(*scopes, **kwargs)
            payload = token.token.split(".")[1]
            claims = json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
            identities = [claims.get(key, "").casefold() for key in ("upn", "preferred_username", "unique_name")]
            require(claims.get("tid") == plan["tenant"],
                    "Actual request identity differs from participant choice")
            if plan["account"].casefold() not in identities:
                check_cli(plan)
                user_id = cli("ad", "signed-in-user", "show", "--query", "id")
                require(isinstance(user_id, str) and user_id.strip(),
                        "Selected account directory identity could not be verified")
                require(claims.get("oid") == user_id,
                        "Actual request identity differs from participant choice")
            expires_on, expiry = getattr(token, "expires_on", None), claims.get("exp")
            if (
                cacheable
                and claims.get("aud") in ("https://management.azure.com", "https://management.azure.com/")
                and type(expires_on) in (int, float) and type(expiry) in (int, float)
                and min(expires_on, expiry) > time() + 300
            ):
                # AzureCliCredential launches CLI even for repeated token requests.
                self.arm_token = (token, min(expires_on, expiry), context)
            return token

        def close(self):
            self.arm_token = None
            self.closed = True
            inner.close()

    return VerifiedCredential()


def verify_version(project, plan, config):
    observed = project.agents.get_version(agent_name=plan["agent_name"], agent_version=plan["agent_version"])
    require(normalized(observed.definition.as_dict()) == normalized(config["definition"]),
            "Pinned version differs from reviewed configuration")
    return observed


def summarize_response(response, plan):
    body = response.model_dump(mode="json")
    reference = body.get("agent_reference")
    expected = {"type": "agent_reference", "name": plan["agent_name"], "version": plan["agent_version"]}
    require(reference == expected, "Response agent/version linkage differs or is missing; inspect saved evidence")
    return {
        "response_id": response.id, "agent_reference": reference,
        "reply": response.output_text, "status": response.status,
        "conversation": body.get("conversation"), "usage": body.get("usage"),
        "output": body.get("output", []), "error": body.get("error"),
        "judgement": "not graded; coach must review actual evidence",
    }


def execute(project, client, plan, config, record, save):
    operation = plan["operation"]
    if operation == "create-version":
        check_cli(plan)
        from azure.ai.projects.models import MCPTool, PromptAgentDefinition
        definition = config["definition"]
        tools = [MCPTool(**{k: v for k, v in tool.items() if k != "type"})
                 for tool in definition.get("tools", [])]
        candidate = PromptAgentDefinition(model=definition["model"], instructions=definition["instructions"], tools=tools)
        require(normalized(candidate.as_dict()) == normalized(definition), "Unsupported definition fields")
        record["state"] = "creation_started_do_not_repeat"
        save()
        created = project.agents.create_version(agent_name=plan["agent_name"], definition=candidate)
        record["created_version"] = created.version
        save()
        observed = project.agents.get_version(agent_name=plan["agent_name"], agent_version=created.version)
        require(normalized(observed.definition.as_dict()) == normalized(definition), "Created version readback differs")
        record["definition_readback_matches"] = True
        return
    verify_version(project, plan, config)
    if operation == "inspect":
        record["definition_readback_matches"] = True
        return
    if operation == "new-conversation":
        check_cli(plan)
        record["state"] = "conversation_creation_started_do_not_repeat"
        save()
        record["conversation_id"] = client.conversations.create().id
        save()
        return
    if operation == "retrieve":
        response = client.responses.retrieve(plan["response_id"])
        record["raw_response"] = response.model_dump(mode="json")
        save()
        record["results"].append(summarize_response(response, plan))
        return
    cases = [{"id": "tool-continuation"}] if operation == "continue" else plan["cases"]
    for case in cases:
        check_cli(plan)
        kwargs = {
            "max_output_tokens": plan["max_output_tokens"],
            "extra_body": {"agent_reference": {
                "type": "agent_reference", "name": plan["agent_name"], "version": plan["agent_version"],
            }},
        }
        if operation == "continue":
            prior = client.responses.retrieve(plan["response_id"])
            summarize_response(prior, plan)
            requests = [item for item in prior.model_dump(mode="json")["output"]
                        if item["type"] == "mcp_approval_request" and item["id"] == plan["approval_request_id"]]
            require(len(requests) == 1, "Matching pending approval request not found")
            request = requests[0]
            require(request["server_label"] == plan["server_label"] and request["name"] == plan["tool_name"]
                    and json.loads(request["arguments"]) == plan["arguments"], "Tool approval scope differs")
            kwargs.update(
                previous_response_id=plan["response_id"], store=True,
                input=[{"type": "mcp_approval_response", "approval_request_id": plan["approval_request_id"],
                        "approve": plan["approve"]}],
            )
        else:
            kwargs.update(input=case["prompt"], store=case.get("store", False) or bool(case.get("conversation_id")))
            if case.get("conversation_id"):
                kwargs["conversation"] = case["conversation_id"]
        record["state"] = "request_started_do_not_repeat"
        record["requests_started"] += 1
        record["pending_case"] = case["id"]
        save()
        started = perf_counter()
        response = client.responses.create(**kwargs)
        duration = perf_counter() - started
        record["raw_response"] = response.model_dump(mode="json")
        save()
        result = summarize_response(response, plan)
        result["case"] = case
        result["request_seconds"] = round(duration, 3)
        record["results"].append(result)
        save()
        if any(item["type"] == "mcp_approval_request" for item in result["output"]):
            record["state"] = "awaiting_separate_tool_approval"
            return
        require(response.status == "completed", "Response incomplete; stopped without retry")
    record.pop("pending_case", None)


def run(plan, config):
    require(readiness()["prompt_runner_ready"], "Dependency mismatch; run readiness and resolve before execution")
    from azure.ai.projects import AIProjectClient

    os.environ["AZURE_CONFIG_DIR"] = plan["azure_config_dir"]
    folder = ROOT / ".workshop" / "evidence"
    folder.mkdir(parents=True, exist_ok=True)
    evidence = folder / (plan["run_id"] + ".json")
    record = {"started_at": now(), "state": "preflight", "plan": plan,
              "configuration": config, "requests_started": 0, "results": []}
    with evidence.open("x", encoding="utf-8") as handle:
        json.dump(record, handle, indent=2)

    def save():
        temporary = evidence.with_suffix(".tmp")
        temporary.write_text(json.dumps(record, indent=2), encoding="utf-8")
        temporary.replace(evidence)

    credential = None
    started = perf_counter()
    try:
        check_cli(plan)
        credential = verified_credential(plan)
        project_resource = cli("resource", "show", "--ids", plan["project_resource_id"])
        require(project_resource["id"].lower() == plan["project_resource_id"].lower(), "Project resource differs")
        record["authorization"] = verify_permissions(plan, credential)
        save()
        with AIProjectClient(endpoint=plan["endpoint"], credential=credential, retry_total=0) as project:
            # This request establishes access to the exact data-plane project, not just ARM.
            next(project.connections.list().by_page(), None)
            with project.get_openai_client(max_retries=0, timeout=60) as client:
                execute(project, client, plan, config, record, save)
        if record["state"] != "awaiting_separate_tool_approval":
            record["state"] = "operation_completed_not_graded"
        record["finished_at"] = now()
        record["elapsed_seconds"] = round(perf_counter() - started, 3)
        save()
    except Exception as error:
        record["state"] = "stopped_do_not_retry_without_reconciliation"
        record["elapsed_seconds"] = round(perf_counter() - started, 3)
        record["error"] = {"type": type(error).__name__, "status_code": getattr(error, "status_code", None)}
        if isinstance(error, ValueError):
            record["error"]["reason"] = str(error)
        save()
        raise RuntimeError(f"Runner stopped ({type(error).__name__}); inspect {evidence}. Do not repeat uncertain requests.") from None
    finally:
        if credential is not None:
            credential.close()
    return evidence, record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("readiness", "execute"))
    parser.add_argument("--plan")
    args = parser.parse_args()
    if args.command == "readiness":
        print(json.dumps(readiness(), indent=2))
        return
    require(args.plan, "An approved local plan is required")
    plan, config = load_plan(args.plan)
    evidence, record = run(plan, config)
    print(json.dumps({"evidence": str(evidence), "state": record["state"],
                      "requests_started": record["requests_started"], "results": record["results"]}, indent=2))


if __name__ == "__main__":
    main()
