# 00: Connect the Copilot app to the workshop environment

**Outcome:** verify or help the participant create their dedicated Microsoft Foundry Project,
reuse a suitable existing Model Deployment or create one after explicit
approval, know where the coach and agents run, and inventory which
capabilities can actually be used. Do not create an agent at this step.

## Student experience

Follow the [participant start guide](START.md): in the GitHub Copilot app's
repository project, type **`/agent`** in the message box, select
**Workshop Coach**, then say **"Start the workshop."** The documented agent
picker inside the prompt box is an alternative if visible. Use normal
repository Chat only if neither selection route is available.
The coach welcomes you before asking for setup information, checks
saved progress, and helps with one missing value at a time. There is no VS Code
extension setup in the core path.

The facilitator confirms organizational access and any managed-install policy.
Use the official links below rather than copied installers or guessed commands.
Verify that the app can read the repository and use its execution environment.

Every participant uses one dedicated Microsoft Foundry Project. They may create
it before the workshop or create it themselves at checkpoint 00 with coach
guidance after confirming the target and possible costs. The facilitator does
not assign the project name or endpoint. Follow this opening order: welcome and
explain the workshop, ask the two quick product-specific experience questions
from COACH.md, then begin setup by confirming which Microsoft account the
participant wants to use and immediately asking for the actual Project
Endpoint. Save experience preferences locally and reuse them; no second start
command or proficiency test is needed. If they do not know the endpoint
or do not yet have a project, help them safely locate or create their own
project. The coach does not create it on their behalf or switch projects
silently. The shared story creates and enhances the Weather Research Agent,
repeats the evidence loop for the Cultural Travel Agent, then introduces hosted
workflow code. Capstone choice comes later.

The core MCP services are already selected in [MCP-SERVICES.md](MCP-SERVICES.md).
The coach supplies their URLs and tool information at the relevant lessons.
Participants need no MCP service account, API key, Cloudflare account, or MCP
hosting setup. This does not replace Foundry authentication or remove Azure
costs.

**App practice:** ask the coach to explain repository context without making
changes, then compare that read-only request with asking it to perform a
specific change. Starting the workshop does not grant blanket permission to
change Azure resources. Selecting Workshop Coach chooses the coaching profile;
it does not create a Foundry agent or grant Azure permissions.

## Minimum environment, then just-in-time additions

| When | Needed | What the coach verifies |
|------|--------|------------------------|
| Start | Copilot app access, Git, repository workspace | Repo instructions load; branch/worktree is the student's |
| Participant project | Participant chooses the signed-in Microsoft account to use; coach execution identity can access the exact project and has the required permission for the current approved step; participant can create a dedicated project if one is not already available | Confirm the identity actually used by the Foundry request matches the participant's choice, then directly verify project identity and operation-specific permission; no shared or silently substituted project |
| Workshop model | Microsoft Foundry Model Catalog access, usable project quota, and model-deployment permissions | Inspect existing deployments first; participant chooses whether to reuse a suitable one or independently selects a compatible model and explicitly approves a new named deployment and possible cost |
| SDK fallback | Python and isolated environment | Use the current prompt quickstart's package versions in the student implementation |
| First successful project connection at checkpoint 00; recheck before checkpoint 03 tests and portal trace inspection | Application Insights connected to the participant's Foundry Project, with telemetry-read access | Check connection metadata and telemetry-read access read-only; record readiness or the specific blocker; obtain separate approval for any connection, new resource, or new test |
| Weather MCP | Selected public endpoint `https://weather.datakoot.com/mcp`; no authentication | Current Streamable HTTP schemas; `weather_forecast` first, approved four-tool expansion later; US coverage, upstream provenance, and Foundry runtime evidence |
| Cultural Travel MCP | Selected public endpoint `https://mcp.travel.art/`; no authentication | Current Streamable HTTP schemas; `find_museum_guide` first, approved four-tool expansion later; actual catalogue coverage, guide attribution/freshness, and Foundry runtime evidence |
| Foundry reusable tools (04/05) | Supported upstream connection registration and reuse inside a domain Toolbox | Exact schema/reference semantics, management permissions, read-back and same-ID reuse; anonymous upstream needs no secret; a separate authenticated connection targets the Foundry Toolbox |
| Toolboxes (04/05, 11/12; verification at 07/14) | Supported Toolbox API/client and prompt-agent consumption in the project's region | Weather starts with one tool at 04, expands at 05, and verifies its binding at release; Cultural deepens the pattern; caller/runtime access, pinned endpoints, retained routing URL, verified connection names and actual discovered tool names, effective restrictions and approval/denial; see TOOLS-AND-TOOLBOXES.md |
| Memory | Chat and embedding deployments, memory capability | Store permissions, identity scope, retention, update behavior |
| Skills | Skills API and compatible client/provider | Upload/version/retrieve support; MCP resources support is distinct from tools |
| Hosted workflow | Azure Developer CLI (`azd`), Agent Framework, supported Foundry extensions/runtime, and tracing | Reviewed scaffold revision and exact dependency lock, Responses portal approval flow plus required Invocations path, host transport regressions, both downstream endpoints/contracts, deployment support and quota/cost boundary; require the [pre-cohort workflow readiness gate](FACILITATOR.md#hosted-workflow-readiness-before-the-cohort) |
| Consumer access | Approved test caller identities | Endpoint invocation permission and a caller without permission for the negative test |
| Microsoft Teams/Microsoft 365 Copilot (07, 16) | At least one chosen surface, licensed/allowed tenant access, project publishing and Bot Service resource/channel write permissions, registered Microsoft.BotService provider | Rehearsed Weather and hosted-workflow publication/installation, compatible activity adapter, channel identity and trusted user/state mapping, downstream runtime access, actual tool approval/denial and correlated traces; separate audience/data/cost approval; see PUBLISHING.md |

Use the installed `microsoft-foundry` skill, including its dependency check and
workflow instructions, when available. Otherwise follow the official references
below using available tools. Do not claim an integration exists just because
this repository mentions it.

Read-only checks can include current CLI versions, signed-in account summary,
project metadata, available catalog models, and quota. Students
complete interactive sign-in themselves. Do not dump credential-bearing
environment variables or tokens. The participant chooses independently from the
Microsoft Foundry Model Catalog. The coach may recommend considering a
compatible mini-class model to reduce cost and quota use, but must not make the
choice or imply that the facilitator provides the model.

Before creating a project, confirm the participant's intended target and
acknowledgment that the operation may incur cost. At the start of checkpoint
00, after the welcome and workshop overview, ask which signed-in Microsoft
account the participant wants to use for Foundry. Offer the currently signed-in
account if it can be identified safely, an approved sign-in flow for a different
account, and freeform input. Do not request credentials. After account
confirmation, ask for the exact Project Endpoint; do not ask whether the
participant already has a project first. Verify the identity used by the actual
Foundry request matches the participant's selection; `az account show` does not
prove which identity Foundry MCP uses.

With multiple signed-in accounts, use a separate workshop CLI profile through
a process-scoped `AZURE_CONFIG_DIR` outside the repository. Have the participant
sign in interactively and confirm the exact account, tenant, and subscription;
tenant selection alone does not select a user. Run the read-only SDK check
with explicit `AzureCliCredential` in that same profile, not an automatic
credential chain. Do not change global profile settings or sign out unrelated
accounts. An already-running MCP server does not automatically inherit these
settings; verify its authentication source separately and distinguish its
results from the selected-account SDK check.

Before each Foundry resource inspection or operation, check Azure CLI
availability and `az login` status in the execution context that will perform
it. `az account show` confirms account context only, not access to the Foundry
Project or permission to create resources. Immediately after receiving the
project endpoint, make a direct authenticated request to that exact project and
confirm its identity. Then verify the operation-specific permission required
for the current step; read-only access alone is insufficient to create
resources. On this first successful project connection, also perform the
[read-only portal tracing readiness check](#portal-trace-prerequisite) and
report the result before moving to model selection. Never probe write access
by creating a throwaway resource, print or
request credentials, broaden permissions, or switch identities without
approval. Use the existing authenticated context for read-only discovery and
approved operations. If sign-in, direct project access, or required permission
is unavailable, state which check failed and pause before recommending or
performing the operation.

Once the project is confirmed and directly readable, inspect its existing
model deployments in Microsoft Foundry before asking for a model name/version
or proposing reuse or a new deployment.
If a suitable deployment exists, show its directly verified deployment name,
model/version, status, and project, then ask whether the participant wants to
reuse it. A project endpoint is not a resource ID; use supported discovery
rather than reconstructing an ID. Do not ask the participant to inspect the
portal in place of the coach's lookup or treat their report as independent
verification.

If no suitable deployment is selected, the participant independently chooses a
compatible model from the Microsoft Foundry Model Catalog. After the selection,
check once more for an existing deployment matching that model name/version
before asking for a new deployment name. Before creating a new deployment,
confirm the participant's project, model name/version, deployment name, and
acknowledgment that creation may incur cost. Before reuse, confirm the exact
target and the participant's explicit choice; explain that model usage may
still incur cost. Before the reuse choice or new-deployment creation approval,
follow COACH.md's model-selection pricing display: explain tokens and show
verified input, cached-input (if supported), and output prices per token and per
million tokens for the actual model, deployment type, region, and currency.
Before the first prices or paid-call approval, explain that these counts and
estimates cover the agents built and tested in Foundry and their model setup
tests, not the Workshop Coach conversation in the Copilot app. Copilot usage
and billing are separate and excluded; do not imply the coach is free.
Label subsequent summaries **Microsoft Foundry agent/model usage**.
Follow [checkpoint usage summaries](COACH.md#checkpoint-usage-summaries):
capture usage locally per operation, but report checkpoint and updated workshop
totals once per checkpoint, not after every call. Pre-action cost disclosures
and approvals remain required.
Include the source and date, distinguish estimated retail cost from the final
bill, and state explicitly when pricing cannot be verified. Do not hardcode
example prices or force token rates onto a different billing model.
Save the verified pricing basis locally for later usage estimates.
Detailed capacity, quota, and pricing comparisons beyond those rates are not
required unless the selection or an error makes them necessary.
Create only the participant's dedicated project and only an
explicitly approved new deployment inside it, then inspect the result.

## Official installation links

Install tools just in time, not all at workshop startup. On organization-managed
devices, follow the facilitator's software-distribution policy even when an
official public installer exists.

| Tool or service | Needed | Official link |
|-----------------|--------|---------------|
| GitHub Copilot app | Before checkpoint 00 | [App download page](https://github.com/features/ai/github-app) and [getting-started guide](https://docs.github.com/en/copilot/get-started/quickstart-copilot-app) |
| Git | Before checkpoint 00 | [Git downloads](https://git-scm.com/install/) |
| Microsoft Foundry portal | Checkpoint 00 onward | [Open Microsoft Foundry](https://ai.azure.com/) |
| Python | Only when a lesson needs the SDK or the hosted scaffold | [Python downloads](https://www.python.org/downloads/) |
| Foundry development tooling | Before SDK-based Foundry work | [Prepare the Foundry development environment](https://learn.microsoft.com/azure/foundry/how-to/develop/install-cli-sdk) |
| Azure CLI | Required before the first Foundry check: the coach verifies CLI availability and sign-in in the actual execution process | [Install Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) |
| Azure Developer CLI (`azd`) | Before hosted checkpoint 15 | [Install Azure Developer CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd) |

Do not install VS Code for the core workshop. Do not use direct installer URLs
copied into the curriculum; the official pages select the current supported
package and include operating-system-specific instructions.

### Optional advance readiness, same live approval boundaries

Offer a facilitator-assisted preparation slot before the workshop. Run
`python workshop\runner\workshop_runner.py readiness` in the coach's actual
execution environment. This offline inventory checks tools and package
versions without installing, authenticating, reading Azure resources or
generating model usage. See [runner scope and setup](runner/README.md).

Arrange tools in an isolated environment before the cohort when possible;
otherwise install only when a prerequisite check identifies a missing tool.
Then, with participant-confirmed account/project and agreed read-only scope,
verify direct access, telemetry readiness and later memory/skill, consumer
identity and hosted-runtime prerequisites. Mark each available, unavailable
or unverified; metadata alone does not demonstrate runtime behavior.
No project/model creation, memory-store write, deployment, paid test or role
change is authorized by advance readiness. The live coach still confirms the
account, immediately collects the endpoint and revalidates the actual context.

Include channel readiness for the required publication/use at 07 and 16:
chosen Microsoft Teams/Microsoft 365 Copilot surface(s), tenant app policies,
licensing/access, Bot Service permissions/provider registration and compatible
hosted protocol/approval handling. Readiness is not authorization to register
a provider, create a bot, publish an app or send a channel test. Do not prepare
participants' publication passes for them.

The shared helper is deliberately narrow: creation/readback, bounded prompt
tests, managed Conversation creation, exact tool approval/denial continuation,
and response retrieval. It does not replace the installed skill, current
permission guidance, memory/release helpers, or the hosted scaffold.

## Choose the actual resource boundary

Use only the participant's own dedicated project, whether prepared before the
workshop or created by the participant at checkpoint 00. Record the confirmed
subscription, project endpoint, ownership, participant-created model deployment,
and a unique student prefix in `.workshop/progress.json`. Also record exact
resource IDs when resources are created later, with `owned_by_student` and
`cleanup_approved` flags.

An existing project endpoint is not an ARM resource ID. Resolve resource IDs
through supported discovery; do not reconstruct them from guessed names.
Do not create new infrastructure or change IAM to bypass missing access.

The facilitator must preflight all later capabilities. At checkpoint 00, mark
each capability `available`, `unavailable`, or `unverified`, with evidence.
Initial prompt access must work to pass 00. Later capabilities can be unverified
at this point, but their own checkpoints cannot pass until verified.

### Portal trace prerequisite

**Application Insights** is Azure's telemetry service for storing execution
records such as agent traces. A **trace** records the calls and steps of an
execution. Foundry-managed Conversation history and portal trace visibility
are separate capabilities: a successful model reply or saved Conversation does
not prove tracing is configured.

Check portal tracing at the first successful authenticated project connection
in checkpoint 00, before model selection; do not wait until checkpoint 03 to
discover a missing prerequisite. Repeat the check before checkpoint 03's tests
and required portal inspection, and when the project or inspection identity
changes. Use read-only metadata to identify the Application Insights resource
connected to the exact Foundry Project, then verify telemetry-read access using
a supported read-only request under the inspection identity. Do not request
connection secrets, generate agent traffic, or create resources as a probe.
If the coach cannot verify the participant's portal identity's access, record
that access as unverified rather than inferring it from the coach's identity.
Project or model access alone is not proof of telemetry access. Follow the current
[Foundry tracing prerequisites and setup](https://learn.microsoft.com/azure/foundry/observability/how-to/trace-agent-setup).

Save the result in `capabilities.portal_tracing` in local progress: readiness
`status` (`available`, `unavailable`, or `unverified`), connection status,
discovered Application Insights resource ID, telemetry-read access,
trace visibility, check time, and sanitized evidence naming the checked
identity and any blocker. A confirmed missing connection or denied read is
unavailable; an unsupported or inconclusive check is unverified. Report the
result in plain language immediately. A configured connection and confirmed
read access establish readiness, not proof that a particular trace was
ingested; leave trace visibility unverified until an actual trace is observed.
Missing tracing does not invalidate a successful project connection or model
test, but must remain an explicit blocker for the required trace exercises.

If the connection or access is missing, explain the specific blocker before
directing the participant to search for a trace. Connecting an existing
Application Insights resource is a project change; creating one is an
additional resource change. Confirm the exact targets, permissions, possible
ingestion/storage/retention costs, and data captured before either action.
Do not create resources or change permissions without separate approval.
Telemetry charges are not included in model-token cost estimates.

Preserve successful Conversation tests and service-returned identifiers if
tracing is blocked, but leave the required portal exercise incomplete.
Do not assume enabling tracing backfills earlier executions. If a new
invocation is needed after setup, obtain explicit approval for that bounded
test and its model cost; do not automatically repeat previous tests.

## Student workspace

The coach creates only files needed for the current lesson:

```text
student/
  prompt-agents/      Both agent definitions, tests, isolated dependencies
  skills/            Student-authored SKILL.md packages
  hosted-agent/      Trip Planning Workflow and result contracts, added at checkpoint 15
  capstone/          Chosen final project, added at checkpoint 17
.workshop/
  progress.json      Local progress, never committed
  evidence/          Sanitized test observations, never committed
```

Source artifacts under `student/` can be reviewed and committed by the student.
Keep secrets in an appropriate secret store or ignored environment files.
Do not commit local transcripts or endpoint response dumps under `student/`.

Create a separate dependency environment and dependency manifest for each
implementation under `student/`. The current prompt quickstart
requires Azure AI Projects 2.x (currently `>=2.3.0`). Verify current requirements
at execution time and record the versions actually used. Confirm the Python
version required by the selected hosted runtime before installation.

## Approval and costs

Model tokens, embedding calls, memory, built-in tools, hosted compute, supporting
services, and telemetry can incur charges. Before creating/changing resources,
agree on the target, scope, and cost boundary. Reusing a project does not make
operations free. Pausing a lesson does not stop hosted compute.

For specified low-cost tests on confirmed resources, the participant may approve
a bounded batch or allowance using
[COACH.md's test-spend agreement](COACH.md#bounded-test-spend-agreements).
Explain costs and exclusions once, track conservative cumulative estimates
locally, and do not repeatedly seek negligible-price approval for unchanged
covered tests. Stop before exceeding the remaining allowance or when costs
cannot reasonably be bounded. No universal dollar amount or billing hard cap
is implied; changed scope/resources and further spend require a new decision.
Resource writes, identity/permission changes, deployments and every human MCP
tool approval remain separate.

For private projects, use the organization's supported network path. Do not
relax network restrictions to get through a workshop.

## Checkpoint

**Pass evidence:** repository access; participant project identity and ownership;
direct connection to the exact Microsoft Foundry Project; verified permission
for the current approved operation (including deployment creation if needed);
participant-confirmed choice to reuse a suitable existing deployment or
explicit approval for a new Model Deployment observed in the project; recorded
capability inventory; confirmed distinction between facilitator-provided and
participant-owned resources.

**Teach-back:** "Which agent is coaching you, which will run in Azure, and how
can you request an explanation without authorizing a change?"

## Current references

Use these before generating version-sensitive API calls or CLI syntax. Preview
features and publishing terminology can change; verify commands against these
references before use.

- [Foundry prompt-agent quickstart](https://learn.microsoft.com/en-us/azure/foundry/agents/quickstarts/prompt-agent)
- [Hosted agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents?view=foundry)
- [Official Foundry samples](https://github.com/microsoft-foundry/foundry-samples)
- [MCP tools](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/model-context-protocol)
- [Selected workshop MCP services, configuration, and story](MCP-SERVICES.md)
- [Reusable Foundry tools and Toolboxes](TOOLS-AND-TOOLBOXES.md)
- [Weather MCP provider](https://datakoot.com/weather-geo)
- [travel.art MCP provider](https://mcp.travel.art/)
- [Memory stores](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/memory-usage)
- [Skills](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/skills)
- [Current agent model and stable endpoints](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/migrate-agent-applications)
- [Publish to Microsoft Teams and Microsoft 365 Copilot](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/publish-copilot)
- [Publication API, networking and channel limitations](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/publish-copilot-virtual-network)
- [Legacy Agent Applications](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/agent-applications)
- [Custom-agent configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
