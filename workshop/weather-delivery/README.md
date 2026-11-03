# Optional Weather-agent GitHub delivery lab

This is an optional lab **after Weather checkpoint 07 and before Cultural
checkpoint 08**. It is not a numbered core checkpoint. Skipping it or
completing it returns directly to checkpoint 08; the core stays 00-16 and
remains planned for 5-6 hours.
Checkpoint 07 must include the required CH01 channel publication and use
before this optional lab is offered. The lab does not replace CH01 or CH02.

## What this lab does—and does not do

The lab practices a reviewed Git configuration change, offline CI checks, and
bounded Microsoft Foundry cloud stages for the Weather Research Agent only.
The manually dispatched cloud workflow supports configuration capture,
creation/read-back of the separate validation candidate, a managed
Conversation request, and explicit per-call MCP approval or denial
continuation. Its API calls have offline mock coverage, but have **not** been
rehearsed against a live project. The separate release helpers remain gated;
the workflow does not claim end-to-end release automation.

This uses **one Microsoft Foundry Project as a training compromise**, not as a
production pattern or best practice. The validation candidate and released
Weather agent must be separate resources with explicitly separate memory
scopes. This reduces accidental changes to the released agent; it does not
isolate quotas, permissions, project-wide resources, audit scope, or blast
radius. Never infer memory isolation from using separate Conversations.

GitHub CI's short-lived workload identity, the participant/runtime identity,
and any agent identity are different principals. A GitHub Environment approval
or a successful CI run is **not** per-call MCP approval. Keep the actual
`weather_forecast` request visible and require a human to approve or deny that
specific call in the supported Microsoft Foundry prompt-agent runtime. If the
runtime cannot surface the exact request and preserve its Conversation for
continuation, stop: do not auto-approve, silently switch bindings, or claim a pass.

### Explicit direct-MCP alternative

The lab supports two reviewed binding contracts: the existing **schema 1
Toolbox** manifest and an explicit **schema 2 direct-MCP** manifest. Direct MCP
means the Microsoft Foundry prompt agent calls the public Weather MCP server
without a Toolbox intermediary; it does not mean calling the server from a
separate client to manufacture agent evidence. Choose this alternative
explicitly when managed-agent-to-Toolbox authentication is blocked. It changes
only this optional delivery lab, not T01-T03, CH01/CH02, checkpoint order or
existing participant progress. It awards no workshop pass.

For schema 2, retain every common schema 1 manifest field (model policy,
instructions, skill revision/delivery/hash, separate agents/memory scopes,
configuration file hash and release metadata), **remove `toolbox` entirely**,
set `schema_version` to `2`, and add:

```json
{
  "definition_sha256": "<canonical SHA-256 of the complete reviewed definition>",
  "direct_mcp": {
    "server_label": "weather_intelligence",
    "server_url": "https://weather.datakoot.com/mcp",
    "allowed_tools": ["geocode", "weather_forecast", "weather_current", "weather_alerts"],
    "require_approval": "always",
    "endpoint_source": "service-read-back",
    "unverified_bindings": []
  }
}
```

This is a fragment, not a ready-to-run participant manifest. Copy the actual
server label and explicit tools from the saved version's service read-back.
Only the four listed Weather tools are permitted; a nonempty subset must
include `weather_forecast`. No wildcard, duplicate tool, alternate endpoint,
Toolbox reference, `project_connection_id`, credential or relaxed approval
setting is accepted. The captured definition must contain exactly one MCP
tool with `type=mcp` and the four binding fields shown above (excluding
`endpoint_source` and `unverified_bindings`). Keep static skill/instruction
composition in the complete reviewed definition; changing any part requires
new hashes and review.

Use `workshop.weather_delivery.contract.canonical_sha256(definition)` for the
definition digest (sorted JSON keys, compact separators, UTF-8 and
`ensure_ascii=False`). `configuration_sha256` remains the SHA-256 of the
captured **file bytes**, including its schema wrapper and formatting.
Offline CI verifies both hashes and the direct binding. `prepare`, `start`
and `continue` require exact complete-definition read-back for schema 2,
not just a matching tool URL. Before `prepare`, `binding_verified=yes` means
independent read-back of that exact direct definition/binding in the target
project, not an invented Toolbox-authentication connection. It is still not
proof of runtime execution or permission to invoke a model.

For direct validation evidence, replace the seven Toolbox-specific runtime
fields (`toolbox_name`, `toolbox_version`, `toolbox_mcp_url`,
`toolbox_auth_type`, `toolbox_auth_evidence_ref`, `upstream_connection_ref`,
`toolbox_auth_connection_ref`) with `direct_mcp` (the exact reviewed object)
and `definition_sha256`. Retain all common identity, model, instructions,
skill, memory, release and CI evidence; `upstream_target` is the selected
Weather URL and both tool lists contain the sorted reviewed direct names.
For each approval/denial trace, replace `toolbox_version` with `server_label`
and `binding_sha256` (the canonical digest of the reviewed `direct_mcp`
object). Do not fabricate connection references. Actual per-call human
approval/denial, same-Conversation continuation, memory isolation and
consumer-path evidence remain mandatory. Neither direct-MCP support nor
offline mocks assert that memory, live testing or release is ready.

## Route

1. **Capture** the reviewed Weather configuration and release dependencies
   from service read-back. Record the instructions and model policy; exact
   released-agent/version and Stable Agent Endpoint; for schema 1, Toolbox name, pinned
   version-specific MCP URL, and discovered qualified tool mapping; distinct
   upstream and Toolbox-authentication connection references; skill revision
   and delivery method; and memory configuration hash and separate candidate/
   release scopes. For schema 2, record the direct binding and complete
   definition digest described above instead of Toolbox dependencies.
   Include no tool credentials, private Conversations,
   transcripts, memory contents, or bearer tokens. Do not construct a URL from
   a display name or substitute the project endpoint for the Stable Agent
   Endpoint.
2. **Review in Git.** Put only the sanitized manifest, agent-definition file,
   instructions source, and synthetic/public test cases in the participant's
   `student/weather-delivery/` folder. The manifest pins the agent-definition
   and instructions file hashes; offline CI checks those hashes against the
   reviewed files. Open a normal GitHub pull request and review the diff. The
   manifest contract rejects unknown fields, missing dependency references,
   shared connections, unverified bindings, non-pinned Toolbox endpoints and
   direct-MCP endpoints/tools outside the explicit reviewed contract;
   it does not silently remove unsupported fields.
3. **Run offline CI.** The
   [Weather delivery check](../../.github/workflows/weather-delivery-check.yml)
   runs standard-library tests with no secrets, Azure login, network calls,
   model usage, MCP invocation, or `id-token` permission. A passing check proves
   only that the local contract and progress-state tests passed. It does not
   prove Foundry access or runtime behavior.
4. **Validate the separate candidate.** After reviewing the exact commit,
   manually dispatch the
   [Weather delivery cloud stages](../../.github/workflows/weather-delivery-cloud.yml)
   from the default workshop branch. `capture` reads one exact saved version;
   review its artifact before adding the sanitized definition to the reviewed
   `student/weather-delivery/` change. `prepare` creates the validation agent
   only if it does not exist; if it already exists, the workflow reuses only
   an identical latest definition and blocks on any difference. Keep its
   selected binding (pinned Toolbox or explicit direct MCP), effective allowlist, model policy, skill revision, and
   other dependencies pinned to the reviewed manifest. Verify its identity
   and memory scope independently. Before `prepare`, the operator must
   independently read back the exact Toolbox-authentication connection or
   selected direct definition/binding in this project and set
   `binding_verified=yes`; the workflow has no supported
   connection-discovery operation. Never modify the released agent or its
   dependencies during validation.
5. **Review each tool call before continuing.** `start` creates a fresh
   managed Conversation and stops at one pending Weather MCP approval. The
   run output and artifact contain IDs and hashes, not the raw prompt, reply,
   or tool arguments. Before a separate `continue` dispatch, inspect that
   exact pending request in Microsoft Foundry using its response and
   Conversation IDs, then choose `yes` or `no` for that specific call. The
   continuation re-reads the response and requires the exact approval ID,
   candidate version, reviewed MCP binding, and same Conversation. Never approve
   from a GitHub Environment approval alone or from an uninspected request.
   Each `start` and `continue` dispatch also requires a separate
   current-step cost/spend confirmation; approval to run offline checks,
   capture, or create a candidate does not grant that spend agreement.
   Capture only returned evidence IDs and hashes, including one actual
   approved call and a separate denied call. Do not save raw arguments,
   prompts, replies, or memory content in shared files.
6. **Gate and release manually.** Creating a version on the released agent
   can affect its active traffic when the current selector follows the latest
   version, so `prepare-release` requires its own explicit current-step
   approval before the write. `pin-release` requires a separate approval to
   change version routing. Do not release until the same reviewed
   configuration commit and manifest hash match the passing offline CI run,
   candidate version, dependency references, explicit approval/denial traces,
   and isolated memory evidence. Use the supported Foundry release action only
   after a separate current-step approval. Read back the service-returned
   version/Stable Agent Endpoint, then test through that consumer path and
   retain its evidence IDs. If any identity, dependency version, permission,
   approval, or endpoint differs, block release and preserve the failed
   evidence. A project endpoint, Toolbox MCP URL or public Weather MCP URL is
   not the consumer path.

The standard-library validator can check internal consistency:

```text
python -S -m workshop.weather_delivery.contract check-manifest student/weather-delivery/manifest.json
python -S -m workshop.weather_delivery.contract check-validation student/weather-delivery/manifest.json .workshop/evidence/weather-validation.json --repository haforsbe/agentic-hackathon --default-branch FY27 --current-commit "$CURRENT_SHA" --latest-sha "$LATEST_DEFAULT_BRANCH_SHA" --latest-attempt "$LATEST_RUN_ATTEMPT"
python -S -m workshop.weather_delivery.contract check-release student/weather-delivery/manifest.json .workshop/evidence/weather-validation.json .workshop/evidence/weather-release.json --repository haforsbe/agentic-hackathon --default-branch FY27 --current-commit "$CURRENT_SHA" --latest-sha "$LATEST_DEFAULT_BRANCH_SHA" --latest-attempt "$LATEST_RUN_ATTEMPT"
```

Evidence belongs in ignored `.workshop/evidence/`, not in the Git PR. The
validator checks hashes, pinned dependencies, exact CI run/artifact linkage,
actual evidence-ID presence, and the approval outcome shape; it cannot prove
that a human-reported ID came from Microsoft Foundry. The facilitator must
independently inspect required live evidence. Failed or blocked attempts stay
available for diagnosis and never authorize release. The shell variables in
the examples must come from an independent read of the current commit and
latest default-branch workflow attempt; never fill them from participant-
reported or stale values.

## Before any live rehearsal

The cloud workflow is source-only until a separately approved facilitator
configures its required repository variables:
`WEATHER_AZURE_CLIENT_ID`, `WEATHER_AZURE_TENANT_ID`,
`WEATHER_AZURE_SUBSCRIPTION_ID`, `WEATHER_OIDC_SUBJECT`, and
`WEATHER_FOUNDRY_PROJECT_ENDPOINT`. None are configured by this PR, and the
workflow has not been dispatched. It requires the GitHub OIDC subject to match
the federated credential exactly and the short-lived Azure CLI token to match
the configured tenant and client ID. Do not add a credential, broaden access,
or run a live stage as part of this offline work.

A later facilitator-approved rehearsal must separately establish:

- the exact GitHub repository/workflow/branch OIDC subject and a short-lived,
  least-privilege CI identity, distinct from the participant/runtime identity;
- the exact existing one-project scope and permitted create/read/invoke
  operations,
  without write-probing, role broadening, or creating another model deployment;
- the selected Toolbox-authentication connection and agent binding, or explicit
  direct-MCP definition/binding, were read back in the target project; this
  workflow does not create or discover connections;
- observed prompt-agent runtime use of the reviewed binding, exact
  per-call approval/denial and same-Conversation continuation, plus explicit
  memory isolation evidence;
- explicit cost/spend agreement for each model/tool call, private artifact
  retention, a separate human release gate, and read-only consumer-path
  verification; and
- an observed full failure/recovery rehearsal on synthetic/public data.

Current documented Foundry REST operations support the stages in the cloud
workflow, including prompt-agent MCP configuration and approval continuation.
Live binding and approval behavior for either lab route remain unverified. In addition,
the documented `GET /agents/{name}` response provides endpoint configuration,
not the Stable Agent Endpoint URL. Capture that exact URL from the participant's
Foundry read-back into the reviewed manifest; never derive it from a display
name. The release helpers validate that reviewed URL against the documented
agent endpoint path and read back version routing before use. The cloud
workflow does not yet accept validation evidence because independently
verified trace, memory-isolation, and approval evidence must first be assembled
and reviewed through a provenance-verified path. The release CLI helpers are
fail-closed, but are not exposed as workflow choices until that evidence
collection is implemented. Until those gates are met, **cloud capture and
candidate validation are implemented but live-unverified; release remains
manual and fail-closed**. Never treat mock tests as live runtime evidence.

The optional lab is not included in the core time estimate. Do not reduce or
skip any 00-16 approval, evidence, test, or teach-back gate to fit it in.

## Official references

- [Build with agents, Conversations, and Responses](https://learn.microsoft.com/azure/foundry/agents/concepts/runtime-components)
- [Configure and share a Microsoft Foundry agent](https://learn.microsoft.com/azure/foundry/agents/how-to/configure-agent)
- [Connect agents to MCP server endpoints](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)
- [Create and manage a Toolbox](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/toolbox)
- [GitHub OIDC in Azure](https://docs.github.com/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-azure)
- [GitHub OIDC subject claims](https://docs.github.com/actions/reference/security/oidc#immutable-subject-claims)
