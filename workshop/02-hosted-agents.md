# Hosted agents: orchestrate the two prompt specialists

Keep both tested prompt-agent releases. Build a Microsoft Agent Framework
workflow that invokes them, validates their results, and produces a sourced
itinerary. Do not port their MCP tools, memories, skills, or specialist
instructions into the hosted runtime.

Use [TESTS.md](TESTS.md) and [APP-GUIDE.md](APP-GUIDE.md). Use a current official
hosting sample and the installed Microsoft Foundry skill workflow, not an old
console script as a server entry point.

## Participant delivery flow

1. **Create the workflow (15).** Implement coordination and contracts using
   the prepared host; run the intended local contract and workflow tests.
2. **Test in Microsoft Foundry (16).** Deploy the hosted candidate to
   Microsoft Foundry, then test it in the agent Playground, including separate
   Weather/Cultural decisions, denial and explicit failures. Hosting deployment
   is necessary before this portal test; deployment alone is not a pass.
3. **Connect and test in the destination (16).** Publish that same tested
   workflow to Microsoft Teams, or connect it to Microsoft Copilot Studio.
   Repeat the same applicable behavior tests and inspect the same-run evidence.
   Do not rebuild its orchestration or attach the specialist tools directly.

The destination must meet the same behavioral standard as the Playground:
actual approvals, denial, sourced output and explicit failures must survive
the route. Interface layouts and streaming need not be identical. Follow
[destination test parity](PUBLISHING.md#workflow-destination-test-parity).
Microsoft Copilot Studio integration testing is distinct from publishing to
Microsoft Teams or Microsoft 365 Copilot; a Studio test-pane result alone does
not pass the workshop's CH02 channel-publication milestone.

### Development-time builder skill

Use the repository-scoped
[Python Agent Framework builder skill](../.agents/skills/agent-framework-builder-python/SKILL.md)
when preparing or implementing checkpoints 15-16. It is Microsoft-maintained
guidance for the GitHub Copilot coding assistant, not a runtime skill attached
to either specialist and not an additional participant exercise.

The bundled snapshot is pinned to upstream commit
`1c3264b065ef4b2b9b3614b19394bdd49d98334f`; its source metadata is recorded in
`SKILL.md`. Review changes before intentionally updating that pin. Load its
workflow and hosting references as needed, and check API examples against the
workshop's tested package versions rather than upgrading dependencies to match
upstream guidance automatically.

Use the builder for framework code, session isolation, approval/resume behavior
and deterministic workflow tests. Continue using the Microsoft Foundry skill
for deployment and resource operations, and Microsoft Learn MCP for current
API documentation. Neither guidance nor installation proves Toolbox execution,
human approval, release or CH01/CH02 channel evidence.

## 15: Build and test the Trip Planning Workflow

**Concept:** executable workflow code coordinates released specialists and is
the first place formal machine-readable result contracts are required.

Start with a workflow orientation:

- both prompt agents already work through separate Stable Agent Endpoints;
- each agent owns its tested domain reasoning and skill-guided MCP tool use;
- workflow code owns request validation, agent invocation, result validation,
  partial-failure policy, aggregation, and correlation;
- the retiring visual Microsoft Foundry Workflow designer and Prompt Flow are
  not used.

Continue the [shared story](MCP-SERVICES.md) with a fictional New York art trip.
Use dates inside the actual weather forecast horizon and museum/event coverage
returned by travel.art. Each specialist keeps its own MCP connection, skill,
memory scope, and release. The coach supplies both existing agent release
details and guides their connection into workflow code; the participant does
not need another MCP server. A travel.art `recommend_art_trip` result alone is
not the final workflow, because it does not invoke our Weather Research Agent.
Confirm the checkpoint 14 handoff includes both tested Toolbox-backed releases,
their pinned dependency versions and T01-T03 evidence. The workflow invokes
the specialists, not a combined Toolbox; do not give it direct weather or
cultural tool access as a shortcut around specialist execution.

After approval, scaffold the smallest appropriate
[official sample](https://github.com/microsoft-foundry/foundry-samples) under
`student/hosted-agent/`. Record its source revision and dependency versions.

The facilitator rehearses and records the exact suitable sample revision and
dependency set before the cohort, with a runnable validation/failure-fixture
test path and deployment prerequisites. Reuse that recorded source when it
remains supported; do not search the entire sample catalogue or design a new
hosting stack during the lesson. If it is incompatible, timebox the blocker
instead of substituting an unverified scaffold.

The prepared scaffold supplies hosting plumbing, not completed specialists or
itinerary logic. Participants still review the entry point, implement and
explain agent invocation/validation/aggregation, run the actual workflow and
inspect its correlated traces. No future code is deployed by preparation.

### Prepare the portal-compatible host before teaching

The workflow must work in the Microsoft Foundry portal's agent **Playground**,
not only through a custom API client. A **protocol** is the request/response
contract between that interface and the hosted code. The prepared host must
support the portal's Responses contract, including streamed replies and
separate human tool approvals, while retaining the required Invocations
consumer path. An Invocations-only success is not portal evidence.

Use the reviewed native workflow hosting route for the recorded SDK versions.
Do not invent a transport adapter during the lesson or share mutable workflow
executors between requests. The scaffold must establish these boundaries:

- Treat a valid Responses `include` field as an outer response projection
  (which output details to return), not an execution override. Validate it
  using the tested SDK contract; do not forward it to either specialist.
  Keep caller-supplied instruction, tool, identity and safety overrides rejected.
- Use request-owned workflows/executors, stable checkpoint identities and one
  owner of conversation history. Restore only the current authenticated
  user's conversation and pending approval.
- Preserve the host's outer approval reference and its binding to the exact
  pending native specialist request. Weather and Cultural need distinct
  sequential cards. Reject stale, replayed, forged and cross-user decisions;
  never accept an inner tool ID as a replacement for a missing portal card.
- Keep each specialist's instructions consistent with native approval:
  pause when a tool request needs approval, but after that exact approval and
  actual tool completion, report the result rather than claiming approval is
  still pending. Do not send synthetic "approved" prose or remove inconvenient
  text from the assembled evidence to manufacture consistency.

Before handing this scaffold to a participant, require the
[intended G/W tests](TESTS.md#hosted-trip-planning-workflow) and the facilitator's
[workflow readiness gate](FACILITATOR.md#hosted-workflow-readiness-before-the-cohort).
Record the reviewed repository revision that actually contains the scaffold,
lockfile and tests. An author-only implementation, a bundled builder skill or
a deployed author agent does not supply those files to a participant.
If that handoff is missing, checkpoint 15 is blocked; do not reconstruct it
from an old example or upgrade dependencies opportunistically.
Keep author troubleshooting tests, diagnostic instrumentation, captured
responses and incident records out of the shared scaffold. The implementation
should incorporate the lessons, not make participants repeat the investigation.

Define versioned weather-result and cultural-result contracts based on observed
specialist outputs. Each contract should require the owning agent/version,
destination and relevant constraints, findings, source/tool provenance,
timestamps where applicable, uncertainty, missing information, and explicit
failure status. Contracts validate structure; correlated traces and release
evidence remain the proof of execution.

If a released specialist cannot produce a contract-compatible result, create a
new specialist candidate, fully retest it, and promote it before continuing.
Do not silently reinterpret incompatible output inside the workflow.

Validate semantic consistency as well as schema and provenance. A completed,
approved native tool call does not make every sentence in the specialist's
final answer valid. If that final answer still claims its required approval is
pending, reject it as contradictory evidence and report an explicit
validation failure or documented partial result; do not mark it `ok` or publish
an unqualified completed itinerary. The native approval state remains
authoritative: prose cannot approve a tool or undo an actual decision.
Do not silently strip the contradiction or retry the model to obtain a pass.
Cover invalid or contradictory results with the intended G02/W02 cases.

Use the pre-release content checklist from 07/14 to avoid discovering missing
source fields for the first time here. That checklist is not a schema pass:
the formal contracts are introduced, implemented and tested now. A genuine
incompatibility still requires an explicitly approved specialist candidate
and its applicable regressions/release; do not hide the resulting time cost.

Implement a code-first Agent Framework workflow:

1. normalize and validate the trip request;
2. invoke the released Weather Research Agent;
3. validate the weather result contract;
4. invoke the released Cultural Travel Agent;
5. validate the cultural result contract;
6. aggregate only validated evidence into an itinerary;
7. expose missing, failed, or invalid specialist evidence without fabrication.

The two specialist calls may run independently after request validation when
the participant explains the tradeoff. Bound retries and timeouts. Preserve
correlation identifiers without exposing credentials.

Run G01-G03/W01-W03 locally with synthetic
fixtures, then run the applicable approved live tests through both specialists'
Stable Agent Endpoints. Inspect workflow, executor, agent-call, validation, and
aggregation spans when supported. Two manual agent calls followed by a manually
written itinerary do not prove the workflow ran.

Group deterministic contract/failure fixtures in one local test command.
Keep live happy-path calls and correlated evidence mandatory; do not use
fixtures to claim live specialist success. An isolated injected failure at
the workflow boundary tests the workflow's failure policy, not an outage in
the provider. Record which variant and execution path each case exercised.

**App practice:** review the workflow plan, contracts, generated entry point, and tests.
**Alternative:** use Plan mode when available, then return to Chat for evidence review.
**Teach-back:** "Why do formal contracts appear here rather than in the first skill lesson?"

## 16: Hosted release

**Concept:** deploy the fully passing workflow as a Microsoft Foundry Hosted
Agent and prove its end-to-end behavior through nested traces.

Before deployment, require passing local G01-G03 and W01-W03, compatible
specialist releases, approved runtime configuration, an identifiable code and
contract revision, and explicit cost/change approval. A known-failing hosted
candidate is not deployed or promoted.

Deploy the workflow as a Microsoft Foundry Hosted Agent. Inspect its running
version, Stable Agent Endpoint, identity, configuration, and nested trace. The
workflow trace should show request validation, both agent invocations, both
contract validations, and aggregation. Correlated specialist traces remain the
detailed proof of `weather_forecast`, `find_museum_guide`, and other approved
MCP tool calls. The hosted workflow must invoke both released specialists
rather than attaching their tools directly or replacing either with model
knowledge. If forecast dates or catalogue coverage are unavailable, preserve
the usable evidence and explicitly report the missing part.

Run W01-W03 and P01-P04 remotely. Demonstrate a successful itinerary, each
single-specialist failure, structurally invalid specialist data, timeout or
authorization failure, and no fabricated replacement evidence.

Run W04 through the actual Microsoft Foundry portal on this same candidate
before promotion: one trip with Weather approval followed by Cultural approval,
plus a separately approved denial case. Follow the
[portal workflow procedure](APP-GUIDE.md#hosted-workflow-portal-test-at-16).
Correlate the final answer with both native tool executions and their human
decisions. A plausible answer, two approved-looking cards or an HTTP 200 alone
does not prove execution. A successful trip does not also prove denial.
Contradictory pending-approval text in a completed result is a failed output
assertion, not something the coach should explain away.

If the portal fails, preserve that run and use the bounded recovery procedure;
do not resend automatically, approve an old card again, weaken checkpoint
validation or deploy a speculative fix. A successful fresh conversation
demonstrates that attempt only, not the cause or permanent repair of an earlier
HTTP 400. Keep the affected gate incomplete until the evidence supports it.

Promote only a fully passing hosted candidate. Rollback is an emergency response
for an unforeseen issue discovered after promotion, not a substitute for
pre-release testing. Retain the failed post-release version and traces for
diagnosis while restoring the previous known-good release.

After the final endpoint release/update checks pass, follow
[channel publication at 16](PUBLISHING.md#required-channel-publication-at-07-and-16).
Publish the **hosted workflow's stable endpoint**, not the individual workers,
to the participant's chosen Microsoft Teams and/or Microsoft 365 Copilot
surface. Obtain separate publication and bounded test approvals; do not
rebuild the specialists or replace their endpoints.

If the participant chooses Microsoft Copilot Studio integration, follow its
[connected-agent route](PUBLISHING.md#microsoft-copilot-studio-integration)
and destination parity tests before publication through that agent. Preserve
the workflow endpoint/version and both native approval boundaries; no
Microsoft Copilot Studio orchestration rewrite or approval bypass is allowed.

Run CH02: the participant sends a supported trip request from the chosen
channel and receives the workflow's sourced itinerary. Inspect the same run's
correlated Microsoft Foundry workflow and specialist traces together to show
both agents being invoked, both results validated and the itinerary assembled.
The channel displays the combined reply; do not promise it exposes internal
agent-to-agent messages. Keep per-call approvals, identity isolation,
provenance and explicit failures intact through the channel adapter.
At least one chosen surface must have real CH02 evidence; installation or a
raw endpoint response alone is not enough. An unsupported adapter or approval
flow blocks this milestone; it does not authorize an approval bypass.

**App practice:** send the workflow request in the chosen channel, then compare
the reply with live endpoint/version and nested-trace evidence in the GitHub Copilot app.
**Alternative:** use applicable hosted Canvas controls when available, then return to Chat for validation.
**Teach-back:** "How can you prove that your request from Microsoft Teams or
Microsoft 365 Copilot invoked the workflow and both tested specialist versions?"

The core route is complete only after both endpoint and channel gates pass,
including Weather CH01 and workflow CH02. Proceed to [capstone selection](CAPSTONE.md)
only if the participant chooses the optional follow-on.
