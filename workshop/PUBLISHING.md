# Release and publish to Microsoft Teams or Microsoft 365 Copilot

Use this guide at **07 for the Weather Research Agent**, **14 for the Cultural
Travel Agent**, **16 for the hosted Trip Planning Workflow**, and **19 for the
chosen capstone**. Keep separate names and endpoints so students can compare
both specialists and the orchestrator without overwriting evidence.
Tests and evidence requirements are in [TESTS.md](TESTS.md).

The core has two required channel milestones: publish and use Weather at
**07, before starting Cultural at 08**, then publish and use the hosted workflow
at **16, before core completion**. Participants choose **Microsoft Teams,
Microsoft 365 Copilot, or both**; at least one must pass at each milestone.
Cultural's independent endpoint release at 14 remains unchanged; a separate
Cultural channel app is not required. Keep checkpoint numbering and order.
The GitHub Copilot app is the coaching application, not this distribution target.

## Tool dependencies are part of the release

Follow [Tools and Toolboxes](TOOLS-AND-TOOLBOXES.md). Record the reusable
connection ID/target, Toolbox version-specific endpoint, actual exposed
tool names and effective allowlist alongside the agent/skill versions.
At 07 verify the Weather Toolbox introduced at 04 and expanded at 05 before
running the already-required full final-path regressions and P01-P03. Record
both the upstream connection and Toolbox-authentication connection. Its first release is
Toolbox-backed; do not release direct MCP first and migrate later. At 14
Cultural has its own Toolbox and independent final-path tests; verify Weather's
unchanged release/dependencies and reuse valid evidence rather than repeating
its full suite. Real changes still require affected regressions.
No shared mixed Toolbox or direct-MCP bypass is left in the final candidates.

Verify the **agent runtime identity**, not just the developer, can invoke its
Toolbox and only the permitted upstream tools. Keep human approval observable
for the actual tool/arguments. Do not copy documentation examples that disable
approval. If access or approval propagation cannot be verified, block release.

Pin tested dependency versions rather than consuming an unreviewed Toolbox
default. Agent-version rollback cannot undo a separately mutated connection
or default Toolbox. Retain the tested versions/bindings, review affected
consumers before dependency changes, and obtain separate approval for any
promotion or role change.

## Current model versus legacy publishing

The [current Foundry model](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/migrate-agent-applications)
gives a newly created agent its own identity and stable endpoint. There is no
separate Agent Application creation step to obtain that endpoint. A version
selector controls the version consumers invoke.

In this workshop, **release** means selecting a tested version, configuring
consumer access, and proving invocation through the stable endpoint.
**Publishing** distributes that endpoint to Microsoft Teams or Microsoft 365
Copilot. Endpoint release and channel publication are separate outcomes, with
separate approvals and evidence; publishing is required at 07 and 16.

Inspect actual agent metadata and available tooling to determine which model
the student's environment supports. Do not guess an endpoint URL, assume the
latest-created version is selected, or treat a project endpoint as the stable
agent endpoint.

## Release one fully tested version

1. **Review the candidate.** Run every required pre-release test. Record agent name/version, instructions, model,
   tools/allowlist, memory store/scoping, skill version/delivery strategy, and
   the passing test evidence. For a hosted update, identify the current
   known-good running deployment and the separately tested candidate source/
   configuration revision.
   A known-failing candidate is not promoted to stable routing and a known-failing
   hosted candidate is not deployed.
   Use TESTS.md's stage-aware execution matrix: C01R/C02R preserve live
   forecast/museum assertions with the final allowlist; post-memory D tests
   use a verified clean synthetic referent scope. Do not remove capabilities
   to recreate an earlier lesson's configuration.
2. **Inspect endpoint metadata.** Read the service-returned stable endpoint,
   protocol configuration, version selector, and agent identity. Use current
   official APIs or the installed Foundry workflow. Resolve unsupported API
   versions rather than constructing likely-looking requests.
3. **Confirm the release action.** Explain the exact version routing change,
   consumer access, cost, and rollback target. Obtain approval before making
   changes. If the endpoint already selects the tested version, verify it
   rather than creating duplicate release resources.
4. **Configure least-privilege access.** Confirm the consumer identity can
   invoke the endpoint and the agent identity can access downstream tools,
   memory, and skills. Developer credentials succeeding locally do not prove
   the deployed identity has permission. Use current role/permission guidance;
   do not substitute an owner role for diagnosis.
5. **Invoke as a consumer.** Use a separate client configured for the returned
   endpoint and supported protocol. Verify the SDK's base-URL semantics so
   `/responses` is not appended twice. Do not print or persist bearer tokens.
   Run P01-P03 and inspect actual results.
6. **Save the release record.** Store the endpoint, selected version, identity/
   access configuration, test evidence, and rollback target in local progress.
   Never copy access tokens into a shareable handoff.

Use one approved consumer-path regression batch where supported. The same
exact final-version/path exchange can satisfy feature and P03 assertions;
record those assertions separately, not duplicate model calls. Project-path
results are not consumer-path passes. Keep model usage/cost and unavailable
usage clearly labeled. Helpers do not approve operations or grade results.

For the Weather Research Agent, verify its managed conversation behavior,
memory, Weather MCP server and forecast tool connection, instructions,
evidence-aware weather output and skill-guided tool behavior through the released
endpoint. It does not rely on a
local custom-function executor or client-side workflow.

At 07 continue to the channel milestone below and pass CH01 before starting 08.
Preserve the prompt release, channel publication and pinned Toolbox dependencies
while Cultural is developed. Checkpoint 14 does not plan a Weather migration,
routing change or repeat publication.

At checkpoint 14, release the Cultural Travel Agent through its own stable
endpoint. Verify its instructions, conversation isolation, selected travel.art MCP,
skill-guided multi-tool behavior, and memory. Record both specialist versions
and prove neither claims the other's
tools or evidence domain.

## Hosted update and rollback

At checkpoint 16, first pass the same release checks for the hosted workflow.
Then make one small visible instruction change as a separate candidate version,
run the relevant regressions, and perform P04 after approval.

Route the existing endpoint to the tested new version. Inspect metadata and
invoke it; do not infer selection from creation order or an unverified answer.
Verify that the previous known-good code, configuration, contract, and
specialist versions remain available as the documented recovery target. Do not
route traffic back merely as a demonstration. Execute rollback only when an
unforeseen problem is discovered after promotion, then inspect metadata and
invoke the restored version.

At 19, repeat release and P04 for the capstone workflow. Preserve
both prompt-agent releases and the hosted workflow release; do not make the
capstone silently replace them.

**App practice:** compare the proposed routing change, the resulting metadata,
and an actual invocation. Discuss a raw-response inspection as an alternative
to a summary, or applicable hosted Canvas controls if available. A commit,
visual handoff, or successful deployment command alone does not prove behavior.

**Teach-back:** "What stays stable for the consumer, and which identities need
permission to call the agent and its tools?"

## Legacy Agent Applications: explicit compatibility route only

[Agent Applications](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/agent-applications)
are the previous model: an application wraps a deployment referencing an agent
version. Existing applications continue to work, but they are not the default
new-course target.

If the environment only supports that model, mark the current-model release
checkpoint blocked. Ask the facilitator to approve a legacy/partial route or
provide a compatible environment; do not silently change the learning outcome.
Record `publishing_model` as `legacy` for any approved compatibility exercise.

Key differences to teach:

- Application creation and deployment are separate resources/operations.
- Prompt deployments use the managed type; hosted deployments use the hosted
  type and require a running hosted version.
- Publication introduces a different agent identity. Downstream permissions
  do not transfer automatically.
- Legacy application Responses endpoints support stateless requests; do not
  assume project `/conversations` behavior works there. Client-managed history
  is not a substitute for the separate memory-store lesson.
- Invocation permissions differ from current agent-endpoint permissions.
  Verify the correct role and scope rather than copying a newer role name.
- Migrating to a new-model agent changes the endpoint and identity. Do not
  promise that a legacy-to-new migration preserves the old consumer URL.

## Required channel publication at 07 and 16

Use the current official
[portal publishing guide](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/publish-copilot)
and [REST, networking and limitations reference](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/publish-copilot-virtual-network).
The route below is documentation-checked on **2026-10-30**, not a claim of a
live tenant rehearsal. Recheck support and controls before delivery. The
shared prompt runner does not implement channel publishing or channel tests.
Do not invent an API, paste an endpoint into a channel and call it published,
or create another agent/workflow to simulate the integration.

### Readiness and bounded approval

Explain a **channel** as the application through which someone talks to the
same released agent. The **Azure Bot Service** resource relays messages;
the **Activity Protocol** is the message format used by the channel.
Publication can create that resource, enable the activity protocol and change
channel authorization. It does not replace the tested specialist or workflow.

Before any publishing write, verify the selected Azure CLI sign-in and actual
request identity, project access and current operation permissions as usual.
Also confirm the participant's signed-in channel account and tenant separately.
Check these prerequisites without creating a throwaway resource:

- The exact tested agent/version, returned stable endpoint, existing publication
  and resource ownership. Pin the tested active version; do not use **Always use
  latest**. Reuse an existing valid publication rather than duplicating it.
- The target resource group's `Microsoft.BotService/botServices/write` and
  `Microsoft.BotService/botServices/channels/write` permissions and registered
  `Microsoft.BotService` provider, alongside project agent publishing permission.
  The official guide names **Foundry User** and **Azure Bot Service Contributor
  Role** at their respective scopes; project access alone is insufficient.
  Provider registration and role changes are separate approved operations.
- Access/licensing for the chosen Microsoft Teams and/or Microsoft 365 Copilot
  surface, tenant app policies, allowed installation/distribution, supported
  region/runtime and the actual channel-to-runtime protocol. For the hosted
  workflow, rehearse the compatible hosted adapter and channel approvals, not
  just the prompt-agent publishing screen.
- Consumer authorization, trusted user/Conversation/memory mapping, downstream
  runtime access and effective per-call tool approval/denial through this path.
  Do not disable approvals or share one user's memory to make the channel work.
  If the channel/runtime cannot support these requirements, block the milestone.
- Network and data-governance requirements. Publishing sends metadata and
  messages through Microsoft 365 services with their own processing, storage
  and residency commitments. Use public/synthetic data only. The portal route
  is not supported with public network access disabled; the documented REST
  exception is not permission to relax networking during the lesson. Arrange
  an explicitly approved, rehearsed compatible route or record a blocker.

Ask for the surface(s), then obtain approval for the exact target, display
metadata, app package version, resource group, Bot Service creation/reuse,
audience, data flow and possible Azure/channel costs. Explain that the app
package's `major.minor.patch` version is not the Microsoft Foundry agent version.
Prefer **Just you** for workshop testing. **People in your organization**
changes discoverability and invocation scope and needs separate explicit
approval plus Microsoft 365 administrator approval. Never choose that broader
scope merely to bypass a failed permission check. Confirm actual policies;
personal scope needing no publication admin approval is not a guarantee of
tenant access, licensing or installation.

### Publish, open and use the released target

1. In the **Microsoft Foundry portal** at https://ai.azure.com/, open the
   confirmed project, then **Build > Agents > the exact released agent**.
   At 07 this is Weather; at 16 this is the hosted Trip Planning Workflow,
   not either worker. Confirm endpoint metadata and the pinned active version.
   Select **Publish > Teams and Microsoft Copilot**. The expected dialog is
   **Publish to Teams and Microsoft 365**. These are documented product labels;
   if the actual screen differs, ask what is visible rather than invent controls.
2. Review the shown Azure Bot Service resource and complete **Name**, **Publish
   version**, **Short description**, **Description** and **Developer** with the
   approved public metadata. Select **Next: Publish options > Direct publish**,
   review **Choose who can use this agent**, and only then perform the approved
   **Publish**. A success dialog or pending admin request is not a runtime pass.
   The documented **Download & customize** route is a separately agreed
   fallback only if custom app upload is permitted, not a policy bypass.
3. Use the returned launch link in the chosen **Microsoft Teams** application
   (web entry https://teams.microsoft.com/) or **Microsoft 365 Copilot**
   (https://m365.cloud.microsoft/). Confirm the channel identity/tenant and exact
   published app, not general chat or Workshop Coach. In the documented agent
   store route, personal publication appears under **Your agents**; approved
   organization publication appears under **Built by your org**. Use the
   actual available open/add control; stop on a mismatch. Do not construct
   guessed deep links or promise identical controls across the two products.
4. After separate bounded model-test approval, the participant sends the
   agreed public/synthetic prompt **once from the chosen channel**, handles
   each tool approval at its actual supported location, and brings the real
   reply back to the GitHub Copilot app. The coach must not send a duplicate
   request from the project client or Playground. If both surfaces are chosen,
   approve and record a test in each; one surface's pass does not prove the other.
5. Inspect the same run in Microsoft Foundry through the established trace
   route. Record channel/app, audience, returned app/Bot Service identifiers,
   stable endpoint, selected version, actual input/reply, time and available
   response/Conversation/correlation identifiers. Corroborate runtime linkage
   with service evidence; do not infer it from the agent's self-description,
   a nearby trace or an installation screenshot. Missing linkage stays unverified.

At **07, CH01** proves a grounded weather reply from the released Weather agent
through the chosen channel, retaining provenance, uncertainty, user isolation,
tool restrictions and actual approval/denial behavior.

At **16, CH02** proves the participant's channel message reaches the released
hosted workflow, which invokes **both** released specialists and assembles the
sourced itinerary. Guide the participant through that same run's correlated
workflow and specialist traces: request, Weather call, Cultural call,
validation, aggregation and returned reply. Microsoft Teams/Microsoft 365
Copilot need not display an agent-to-agent conversation; the reply plus
correlated execution evidence demonstrates collaboration. Two separately
published bots, manual worker calls or a plausible itinerary do not pass.

The current publishing reference lists streaming and citations as unsupported
in published channels. Do not promise native citation cards or streaming.
Rehearse readable textual source attribution/URLs and uncertainty in the
channel reply, and retain detailed provenance in the correlated evidence.
If required attribution or approval behavior cannot survive the path, leave
the channel gate blocked rather than silently lowering the evidence standard.

Record CH01/CH02 separately from P01-P04. A raw endpoint pass, app installation
or admin approval alone cannot satisfy them. Save sanitized publication and
test references under `channel_publications` in local progress; unknown usage
stays unknown. Changed audience, identity, protocol, routing or dependencies
requires affected rechecks. Preserve direct-client protocols and authorization
when configuring channels; the documented REST update can replace those
collections. Weather must remain independently callable by the later workflow.

Complete endpoint P04 before the workflow channel milestone, so CH02 tests the
final selected workflow version. Later version-selector updates keep the
stable channel target; metadata changes use the documented update flow.
Never republish solely because a candidate version was created.

If publication or execution is unavailable, name the failed layer, preserve
the endpoint release evidence and apply the coaching troubleshooting timebox.
Checkpoint 07 or 16 remains blocked; an explicitly agreed partial route is
incomplete, not a core pass. Never silently skip to Cultural or claim core
completion. At both checkpoints use one combined release/channel teach-back,
not an extra vocabulary quiz.

## End of workshop

Show the two prompt-agent endpoints, hosted workflow endpoint, and any chosen
capstone endpoint, their verified versions, Weather/workflow channel links and
CH01/CH02 evidence, evidence locations, and every workshop-owned
resource still running.
Ask before stopping or deleting specific
resources. Keep shared projects/models and other students' resources untouched.
Include saved tool connections and Toolbox versions in the owned-resource
inventory, including published apps and Azure Bot Service resources. Channel
unpublishing/removal is separate from stopping a hosted runtime or deleting an
endpoint; review each exact owned target and its consumers before approval.
Check remaining consumers before proposing deletion; removing a
connection can break more than one retained binding or recovery version.
If cleanup removes an endpoint, label it retired in the release record rather
than continuing to claim it is callable.
