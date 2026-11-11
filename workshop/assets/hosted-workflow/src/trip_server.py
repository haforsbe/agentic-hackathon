import asyncio
import base64
import json
import logging
import os
from pathlib import Path
import re

from azure.ai.agentserver.invocations import InvocationAgentServerHost
from azure.ai.agentserver.core import get_request_context
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from agent_framework_foundry_hosting import FoundryRequestScope, ResponsesHostServer
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from trip_workflow import CONFIG, ENDPOINT, NativeInvoker, atomic_json, build, execute_request
from trip_responses import parse_response, prepare_options


logger = logging.getLogger("two-specialist-workflow")


locks: dict[str, asyncio.Lock] = {}
root = Path(os.environ.get("HOME", str(Path.home()))) / "workshop-workflow"
def platform_credential():
    return DefaultAzureCredential(
        exclude_cli_credential=True, exclude_developer_cli_credential=True,
        exclude_powershell_credential=True, exclude_visual_studio_code_credential=True,
        exclude_shared_token_cache_credential=True, exclude_interactive_browser_credential=True,
        exclude_broker_credential=True,
    )


class RuntimeCredential:
    def __init__(self, inner):
        self.inner = inner
        self.identity: dict[str, str] | None = None

    def get_token(self, *scopes, **kwargs):
        token = self.inner.get_token(*scopes, **kwargs)
        encoded = token.token.split(".")[1]
        claims = json.loads(base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4)))
        if (claims.get("tid") != CONFIG.tenant_id
                or claims.get("oid") != CONFIG.runtime_principal_id):
            raise RuntimeError("Unexpected actual hosted request identity")
        self.identity = {"tenant": claims["tid"], "principal_id": claims["oid"]}
        return token

    def close(self):
        self.inner.close()


def response_workflow(request):
    scope_folder = root / "responses" / request.scope.storage_key

    def invoker_for_run(run_id):
        if not re.fullmatch(r"[a-f0-9]{32}", run_id):
            raise ValueError("Invalid stored workflow run identifier")
        folder = scope_folder / run_id
        folder.mkdir(parents=True, exist_ok=True)

        def invoke_native(domain, trip, pending, approved):
            with platform_credential() as underlying:
                runtime = RuntimeCredential(underlying)
                with AIProjectClient(endpoint=ENDPOINT, credential=runtime,
                                     retry_total=0) as client:
                    result = NativeInvoker(client, folder)(domain, trip, pending, approved)
                    atomic_json(folder / "runtime-identity.json", runtime.identity)
                    return result
        return invoke_native

    workflow = build(chat=True, invoker_factory=invoker_for_run)
    return workflow


class WorkflowHost(InvocationAgentServerHost, ResponsesHostServer):
    pass


app = WorkflowHost(workflow=response_workflow, parse_response=parse_response,
                   prepare_options=prepare_options)


@app.invoke_handler
async def invoke(request: Request) -> Response:
    session = request.state.session_id
    if not isinstance(session, str) or not re.fullmatch(r"[a-zA-Z0-9_-]{1,120}", session):
        return JSONResponse({"error": "Unsupported session identifier"}, status_code=400)
    scope = FoundryRequestScope.from_context(app.config, get_request_context(), local_session_id=session)
    folder = root / "invocations" / scope.storage_key / session
    folder.mkdir(parents=True, exist_ok=True)
    lock = locks.setdefault(scope.storage_key, asyncio.Lock())
    if lock.locked():
        return JSONResponse({"error": "A workflow request is already in progress"}, status_code=409)
    async with lock:
        try:
            data = await request.json()
            if not isinstance(data, dict):
                raise ValueError("Request must be a JSON object")
            if data == {"status": True}:
                path = folder / "result.json"
                if not path.exists():
                    return JSONResponse({"error": "No recorded result; reconcile any interrupted request"},
                                        status_code=404)
                return JSONResponse(json.loads(path.read_text()))
            if set(data) not in ({"trip"}, {"approval"}):
                raise ValueError("Supply exactly one trip or one approval")
            with platform_credential() as underlying:
                runtime = RuntimeCredential(underlying)
                with AIProjectClient(endpoint=ENDPOINT, credential=runtime,
                                     retry_total=0) as client:
                    result = await execute_request(folder, data, NativeInvoker(client, folder))
            result["release"] = os.environ.get("WORKFLOW_RELEASE", "unknown")
            result["runtime_identity"] = runtime.identity
            journal_path = folder / "requests.json"
            journal = json.loads(journal_path.read_text()) if journal_path.exists() else {}
            result["response_observations"] = [{
                "response_id": item["body"]["id"], "usage": item["body"].get("usage"),
                "memory_updates": [
                    entry["update_id"] for entry in item["body"]["output"]
                    if entry["type"] == "memory_search_call" and entry.get("update_id")
                ],
            } for item in journal.values() if item.get("body")]
            atomic_json(folder / "result.json", result)
            return JSONResponse(result)
        except (ValueError, ValidationError, json.JSONDecodeError) as error:
            logger.warning("Rejected workflow input or result (%s)", type(error).__name__)
            return JSONResponse({
                "error": "Unsupported trip or invalid native decision; inspect the current pending request",
                "session_id": session,
            }, status_code=400)


if __name__ == "__main__":
    app.run()
