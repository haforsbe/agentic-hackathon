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
continuation, stop: do not auto-approve, switch to direct MCP, or claim a pass.

## Route

1. **Capture** the reviewed Weather configuration and release dependencies
   from service read-back. Record the instructions and model policy; exact
   released-agent/version and Stable Agent Endpoint; Toolbox name, pinned
   version-specific MCP URL, and discovered qualified tool mapping; distinct
   upstream and Toolbox-authentication connection references; skill revision
   and delivery method; and memory configuration hash and separate candidate/
   release scopes. Include no tool credentials, private Conversations,
   transcripts, memory contents, or bearer tokens. Do not construct a URL from
   a display name or substitute the project endpoint for the Stable Agent
   Endpoint.
2. **Review in Git.** Put only the sanitized manifest, agent-definition file,
   instructions source, and synthetic/public test cases in the participant's
   `student/weather-delivery/` folder. The manifest pins the agent-definition
   and instructions file hashes; offline CI checks those hashes against the
   reviewed files. Open a normal GitHub pull request and review the diff. The
   manifest contract rejects unknown fields, missing dependency references,
   shared connections, unverified bindings, and non-pinned Toolbox endpoints;
   it does not silently remove unsupported fields.
3. **Run offline CI.** The
   [Weather delivery check](../../.github/workflows/weather-delivery-check.yml)
   runs standard-library tests with no secrets, Azure login, network calls,
   model usage, MCP invocation, or `id-token` permission. A passing check proves
   only the offline coverage shown in its **job summary and artifact**.
   Delivery-code tests use synthetic fixtures/mocks, not the participant's
   agent. If `student/weather-delivery/manifest.json` is absent, the summary
   says **NOT CHECKED (manifest absent)** and the hash record says
   `contract-suite-only`. A saved agent-definition file alone is not a complete
   package. With a manifest, CI validates its contract and reviewed file hashes;
   malformed manifests, missing referenced files or changed hashes fail CI.
   Neither case proves Microsoft Foundry access or runtime behavior.
   See [Reading green checks](#reading-green-checks) before continuing.
4. **Validate the separate candidate.** After reviewing the exact commit,
   manually dispatch the
   [Weather delivery cloud stages](../../.github/workflows/weather-delivery-cloud.yml)
   from the default workshop branch. `capture` reads one exact saved version;
   review its artifact before adding the sanitized definition to the reviewed
   `student/weather-delivery/` change. `prepare` creates the validation agent
   only if it does not exist; if it already exists, the workflow reuses only
   an identical latest definition and blocks on any difference. Keep its
   Toolbox version, effective allowlist, model policy, skill revision, and
   other dependencies pinned to the reviewed manifest. Verify its identity
   and memory scope independently. Before `prepare`, the operator must
   independently read back the exact Toolbox-authentication connection in
   this project and set `binding_verified=yes`; the workflow has no supported
   connection-discovery operation. Never modify the released agent or its
   dependencies during validation.
5. **Review each tool call before continuing.** `start` creates a fresh
   managed Conversation and stops at one pending Weather MCP approval. The
   run output and artifact contain IDs and hashes, not the raw prompt, reply,
   or tool arguments. Before a separate `continue` dispatch, inspect that
   exact pending request in Microsoft Foundry using its response and
   Conversation IDs, then choose `yes` or `no` for that specific call. The
   continuation re-reads the response and requires the exact approval ID,
   candidate version, Toolbox binding, and same Conversation. Never approve
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
   evidence. A project endpoint or Toolbox MCP URL is not the consumer path.

The standard-library validator can check internal consistency:

```text
python -S -m workshop.weather_delivery.contract check-manifest student/weather-delivery/manifest.json
python -S -m workshop.weather_delivery.contract check-validation student/weather-delivery/manifest.json .workshop/evidence/weather-validation.json --repository OWNER/REPOSITORY --default-branch FY27 --current-commit "$CURRENT_SHA" --latest-sha "$LATEST_DEFAULT_BRANCH_SHA" --latest-attempt "$LATEST_RUN_ATTEMPT"
python -S -m workshop.weather_delivery.contract check-release student/weather-delivery/manifest.json .workshop/evidence/weather-validation.json .workshop/evidence/weather-release.json --repository OWNER/REPOSITORY --default-branch FY27 --current-commit "$CURRENT_SHA" --latest-sha "$LATEST_DEFAULT_BRANCH_SHA" --latest-attempt "$LATEST_RUN_ATTEMPT"
```

Replace `OWNER/REPOSITORY` with the participant-owned copy and confirm its
actual intended default branch; these checks must not bind to upstream CI.
Evidence belongs in ignored `.workshop/evidence/`, not in the Git PR. The
validator checks hashes, pinned dependencies, exact CI run/artifact linkage,
actual evidence-ID presence, and the approval outcome shape; it cannot prove
that a human-reported ID came from Microsoft Foundry. The facilitator must
independently inspect required live evidence. Failed or blocked attempts stay
available for diagnosis and never authorize release. The shell variables in
the examples must come from an independent read of the current commit and
latest default-branch workflow attempt; never fill them from participant-
reported or stale values.

## Reading green checks

Open your owned repository on GitHub, choose **Actions → Weather delivery
offline checks**, select the exact commit/run attempt, then open the
**Delivery-code tests and optional participant-package checks (offline only)**
job summary. Download `weather-delivery-<run-id>-<attempt>` under that run's
artifacts for `coverage.json`, `summary.md` and, when available,
`weather-delivery-check.json`. A failed package still produces a coverage
report, but no passing hash record. If setup failed before reporting, missing
artifacts mean unknown coverage, not a pass.

| Evidence | What it proves | What it does not prove |
|---|---|---|
| Workflow validation (`actionlint`) | Workflow syntax, expression/context availability and structural rules | A successful dispatch, GitHub/Azure permissions or live execution |
| Delivery-code tests | Synthetic contract, progress-state and mocked cloud-code behavior | That any participant agent was invoked |
| Participant-package checks | Manifest contract and reviewed local file hashes; skipped explicitly when absent | That definitions match the service or dependencies work at runtime |
| Live agent tests | **Not run by offline CI** | Identity, MCP approval/denial, memory and telemetry need separate runtime evidence |
| Deployment/release | **Not run by offline CI; not eligible for release** | A stable consumer path or channel milestone |

CI checks all workflows with pinned `actionlint` 1.7.12. This caught the
cloud workflow's invalid job-level `${{ runner.temp }}` reference: the
`runner` context is unavailable at that scope, so GitHub can reject the
workflow before scheduling any jobs. Azure CLI isolation is now initialized
in a step using `$RUNNER_TEMP` and `$GITHUB_ENV`, before OIDC verification or
Azure login. Explicitly quoted `"yes"`/`"no"` choices avoid ambiguous YAML
boolean parsing; quoting alone is not the context-scope fix.

Offline maintainer checks (run from the repository root):

```text
actionlint -shellcheck= .github/workflows/*.yml
python -S -m unittest discover -s workshop/weather_delivery -p "test_*.py" -v
```

Use the reviewed `actionlint` 1.7.12 release, or the same versioned container
command as the offline workflow. Plain YAML parsing is insufficient.

## Read-only GitHub preflight

Complete [owned-repository setup](../START.md#2-choose-your-owned-repository-then-clone-it)
before opening repository Settings. With GitHub CLI (`gh`) already available
and signed in to the intended GitHub account, run this from your workshop
checkout, replacing the example repository:

```text
python -S -m workshop.weather_delivery.repository_readiness --repository OWNER/REPOSITORY --expected-default-branch FY27
```

This only reads GitHub metadata. It does not sign in, modify a repository,
display variable values, grant permissions, contact Azure or dispatch a workflow.
It checks the actual default branch, the caller's administrator access, Actions
enabled state/policy, workflow registration/state, and required variable names.
Selected-action policy is reported, not proven compatible: the owner must
verify that checkout, Python setup, artifact upload and Azure login are allowed.
A listed active workflow is not proof its contents validate; require the
separate structural check.

Successful listing with missing names means **missing configuration**.
Denied requests, hidden/not-found responses, missing `gh` or failed sign-in
mean **unknown**, never "no variables" or permission to create replacements.
The command exits nonzero for missing/unknown requirements. Missing cloud
variables block the optional cloud stages, not core lesson orientation.
All names present means **configured-not-authenticated**, not runtime ready.

| Required repository variable | Purpose (not a credential) |
|---|---|
| `WEATHER_AZURE_CLIENT_ID` | Approved CI workload application's client ID; not the participant identity |
| `WEATHER_AZURE_TENANT_ID` | Tenant for that CI identity |
| `WEATHER_AZURE_SUBSCRIPTION_ID` | Approved subscription for that CI context |
| `WEATHER_OIDC_SUBJECT` | Exact repository/branch subject trusted by the approved federated credential |
| `WEATHER_FOUNDRY_PROJECT_ENDPOINT` | Exact approved Microsoft Foundry Project endpoint |

An owner configures these only under separately approved setup. Do not copy
credentials, auto-grant roles or configure federation during a read-only
preflight. A fork/template does not inherit these settings or identity trust.
CI workload login does not authenticate the participant, portal session,
MCP server or agent runtime. Verify those actual identities and operation
permissions independently at the relevant approved step.

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

The main core path remains blocked on the unverified managed prompt-agent to
Toolbox authentication route described in
[Tools and Toolboxes](../TOOLS-AND-TOOLBOXES.md#prepare-the-supported-route-before-teaching).
The separately proposed direct-MCP alternative in
[PR #7](https://github.com/haforsbe/agentic-hackathon/pull/7) is delivery-lab-only
and is not assumed merged or implemented here. It cannot satisfy the core
Toolbox gate. If that PR is combined later, preserve this coverage reporting,
workflow validation and all independent runtime/approval/memory gates; review
the overlapping workflow, contract, test and guidance edits rather than
replacing one set wholesale.

A later facilitator-approved rehearsal must separately establish:

- the exact GitHub repository/workflow/branch OIDC subject and a short-lived,
  least-privilege CI identity, distinct from the participant/runtime identity;
- the exact existing one-project scope and permitted create/read/invoke
  operations,
  without write-probing, role broadening, or creating another model deployment;
- the Toolbox-authentication connection and agent binding were read back in
  the target project; this workflow does not create or discover connections;
- observed prompt-agent runtime use of the version-pinned Toolbox, exact
  per-call approval/denial and same-Conversation continuation, plus explicit
  memory isolation evidence;
- explicit cost/spend agreement for each model/tool call, private artifact
  retention, a separate human release gate, and read-only consumer-path
  verification; and
- an observed full failure/recovery rehearsal on synthetic/public data.

Current documented Foundry REST operations support the stages in the cloud
workflow, including prompt-agent MCP configuration and approval continuation.
The live Toolbox binding and approval behavior remain unverified. In addition,
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
