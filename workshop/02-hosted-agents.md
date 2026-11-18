# Hosted agents: orchestrate the two prompt specialists

Keep both tested prompt-agent releases. Build a Microsoft Agent Framework
workflow that invokes them, validates their results, and produces a sourced
itinerary. Do not port their MCP tools, memories, skills, or specialist
instructions into the hosted runtime.

Use [TESTS.md](TESTS.md) and [APP-GUIDE.md](APP-GUIDE.md). Use a current official
hosting sample and the installed Microsoft Foundry skill workflow, not an old
console script as a server entry point.
The [shared hosted-workflow asset](assets/hosted-workflow/README.md) contains
the reusable host, confirmed-configuration contract, exact dependency pins and
intended local tests. Its graph is a facilitator reference, not a substitute
for the participant-specific workflow, participant learning or live release
evidence.

**Creation is coach-only.** Workshop Coach writes the code-first workflow and
creates/deploys its hosted agent through the supported SDK/CLI route, after the
required scoped approvals. Participants do not write the workflow themselves
or create this hosted agent directly in the Microsoft Foundry portal. They
review and explain the generated implementation, then inspect and test the
deployed agent. Follow the
[execution ownership rule](COACH.md#hosted-workflow-execution-ownership).

## Participant delivery flow

1. **Create the workflow (15).** Workshop Coach implements coordination and
   contracts using the prepared host and runs the intended local tests.
   Participants review and explain the generated contracts and workflow.
2. **Test in Microsoft Foundry (16).** Workshop Coach deploys the approved
   hosted candidate, then participants test a supported trip in the agent
   Playground, including sourced output and any actual Weather/Cultural tool
   decisions. Do not force permission cards, denials or failure demonstrations.
   Hosting deployment is necessary before this portal test; deployment alone
   is not a pass.
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
API documentation. Neither guidance nor installation proves MCP execution,
human approval, release or CH01/CH02 channel evidence.

## 15: Build and test the Trip Planning Workflow

**Concept:** executable workflow code coordinates released specialists and is
the first place formal machine-readable result contracts are required.

Start with a workflow orientation:

- both prompt agents already work through separate Stable Agent Endpoints;
- each agent owns its tested domain reasoning and permitted MCP tool use;
- workflow code owns request validation, agent invocation, result validation,
  partial-failure policy, aggregation, and correlation;
- the retiring visual Microsoft Foundry Workflow designer and Prompt Flow are
  not used.

Continue the [shared story](MCP-SERVICES.md) with a fictional New York art trip.
Use dates inside the actual weather forecast horizon and museum coverage
returned by travel.art. Each specialist keeps its own MCP connection and
release, plus any configured skill or memory scope. The default route keeps
only `weather_forecast` and `find_museum_guide`; do not add event tools to make
the itinerary broader. Skills and persistent memory are temporarily deferred,
not prerequisites for either specialist or this workflow; follow the
[skills](README.md#temporary-skills-and-multi-tool-deferral) and
[memory](README.md#temporary-memory-deferral) policies.
The coach supplies both existing agent release
details and guides their connection into workflow code; the participant does
not need another MCP server. A travel.art `recommend_art_trip` result alone is
not the final workflow, because it does not invoke our Weather Research Agent.
Confirm the checkpoint 14 handoff includes both tested direct-MCP releases,
their exact bindings, T01/T03 evidence and any configured skill versions.
T02/S01/S02 remain deferred unless those capabilities are configured.
The workflow invokes
the specialists, not their MCP servers; do not give it direct weather or
cultural tool access as a shortcut around specialist execution.

After approval, Workshop Coach uses the reviewed
[shared hosting plumbing](assets/hosted-workflow/README.md) under
`student/hosted-agent/` and builds the participant-specific graph and contracts
incrementally, explaining the generated changes for participant review.
Record the repository revision and dependency versions. If a replacement is
necessary, rehearse the smallest appropriate
[official sample](https://github.com/microsoft-foundry/foundry-samples) before
offering it to participants.

The facilitator rehearses and records the exact suitable sample revision and
dependency set before the cohort, with a runnable validation/failure-fixture
test path and deployment prerequisites. Reuse that recorded source when it
remains supported; do not search the entire sample catalogue or design a new
hosting stack during the lesson. If it is incompatible, timebox the blocker
instead of substituting an unverified scaffold.

The prepared scaffold supplies hosting plumbing, not completed specialists or
itinerary logic. Workshop Coach writes agent invocation, validation and
aggregation. Participants review the entry point and generated logic, explain
the coordination, test the actual workflow and inspect its correlated traces.
No future code is deployed by preparation.

### Prepare the portal-compatible host before teaching

The workflow must work in the Microsoft Foundry portal's agent **Playground**,
not only through a custom API client. A **protocol** is the request/response
contract between that interface and the hosted code. The prepared host must
support the portal's Responses contract, including streamed replies and
human tool decisions whenever requested by the saved policies, while retaining the required Invocations
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
  pending native specialist request. If Weather or Cultural requests permission,
  show its distinct card in sequence; do not invent cards for automatic execution.
  Reject stale, replayed, forged and cross-user decisions;
  never accept an inner tool ID as a replacement for a missing portal card.
- Keep each specialist's instructions consistent with native approval:
  follow its saved policy, pausing only when a native request needs approval.
  After automatic execution or an exact human decision and
  actual tool completion, report the result rather than claiming approval is
  still pending. Do not send synthetic "approved" prose or remove inconvenient
  text from the assembled evidence to manufacture consistency.

Before handing this scaffold to a participant, require the
[intended G/W tests](TESTS.md#hosted-trip-planning-workflow) and the facilitator's
[workflow readiness gate](FACILITATOR.md#hosted-workflow-readiness-before-the-cohort).
Record the reviewed repository revision that actually contains the scaffold,
fully pinned dependency manifest and tests. The shared asset excludes its
private-feed lockfile; its version pins do not prove package availability or
remote-build compatibility. Verify the approved feed and target runtime first.
An author-only implementation, a bundled builder skill or
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
Keep invalid or contradictory results covered by the existing automated
G02/W02 implementation tests, not participant or live failure demonstrations.

Use the pre-release content checklist from 07/14 to avoid discovering missing
source fields for the first time here. That checklist is not a schema pass:
the formal contracts are introduced, implemented and tested now. A genuine
incompatibility still requires an explicitly approved specialist candidate
and its applicable regressions/release; do not hide the resulting time cost.

Workshop Coach implements a code-first Agent Framework workflow:

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

Run the existing automated implementation suite locally, then verify G01/G03
and a supported W01/W03 trip through both specialists'
Stable Agent Endpoints. Inspect workflow, executor, agent-call, validation, and
aggregation spans when supported. Two manual agent calls followed by a manually
written itinerary do not prove the workflow ran.

Group existing deterministic tests in one local build check, without turning
their defensive fixtures into learner demonstrations. Workshop Coach creates
the coordination and contracts; the participant reviews and explains them,
then tests a working trip. Keep live supported
calls and correlated evidence mandatory; fixtures do not prove live specialist
success. Do not inject a failure or ask the participant to demonstrate an outage.

**App practice:** review the workflow plan, contracts, generated entry point, and tests.
**Alternative:** use Plan mode when available, then return to Chat for evidence review.
**Teach-back:** "Why does coordinating two released agents need formal result contracts?"

## 16: Hosted release

**Concept:** deploy the fully passing workflow as a Microsoft Foundry Hosted
Agent and prove its end-to-end behavior through nested traces.

Before deployment, require passing existing local implementation tests and
supported G01/G03 and W01/W03 results, compatible
specialist releases, approved runtime configuration, an identifiable code and
contract revision, and explicit cost/change approval. A known-failing hosted
candidate is not deployed or promoted.

Before a paid hosted test, follow the reference's
[usage and limits guidance](assets/hosted-workflow/README.md#usage-and-limits-before-live-tests)
and obtain the coach's [scoped test approval](COACH.md#scoped-test-approvals).
Explain possible charges and supported execution limits; retain available
response tokens without price lookups or mandatory whole-case calculations.
Four native Responses submissions do not mean four internal inference turns;
requested output limits are not input, memory or billing caps. Missing prices
or a monetary estimate alone do not block tests. Keep all runtime, authorization,
tool-approval and explicitly participant-imposed cost restrictions.

Workshop Coach deploys the approved workflow as a Microsoft Foundry Hosted
Agent. Inspect its running
version, Stable Agent Endpoint, identity, configuration, and nested trace. The
workflow trace should show request validation, both agent invocations, both
contract validations, and aggregation. Correlated specialist traces remain the
detailed proof of `weather_forecast`, `find_museum_guide`, and other approved
MCP tool calls. The hosted workflow must invoke both released specialists
rather than attaching their tools directly or replacing either with model
knowledge. If forecast dates or catalogue coverage are unavailable, preserve
the usable evidence and explicitly report the missing part.

Run a supported W01/W03 trip and P01-P04 remotely. Demonstrate the working
itinerary, both specialist contributions and the implemented traveler
preferences. No deliberate specialist failure, invalid result, timeout or
authorization-denial demonstration is required.

Run W04 through the actual Microsoft Foundry portal on this same candidate
before promotion: one trip with the specialists' saved approval policies.
Handle any actual Weather/Cultural requests separately; respect the
participant's decisions without adding a denial case. Do not change settings
or ask approval-configuration questions to force cards. Follow the
[portal workflow procedure](APP-GUIDE.md#hosted-workflow-portal-test-at-16).
Correlate the final answer with both native tool executions and any actual human
decisions. A plausible answer, two approved-looking cards or an HTTP 200 alone
does not prove execution. Do not claim a successful trip proves denial.
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
agent-to-agent messages. Keep the configured approval behavior, identity isolation,
provenance and explicit failures intact through the channel adapter.
At least one chosen surface must have real CH02 evidence; installation or a
raw endpoint response alone is not enough. An unsupported adapter or approval
flow blocks this milestone; it does not authorize an approval bypass.

**Close the core explicitly:** checkpoint 16 is the final core checkpoint.
Follow the coach's [end-of-core notification](COACH.md#end-of-core-notification)
without waiting for the participant to ask. Announce full completion only when
all core gates pass; otherwise close an agreed stop as partial completion and
name the remaining checks. Explain that 17-19 are an optional capstone, not
additional required core lessons, and do not start them automatically.

**App practice:** send the workflow request in the chosen channel, then compare
the reply with live endpoint/version and nested-trace evidence in the GitHub Copilot app.
**Alternative:** use applicable hosted Canvas controls when available, then return to Chat for validation.
**Teach-back:** "How can you prove that your request from Microsoft Teams or
Microsoft 365 Copilot invoked the workflow and both tested specialist versions?"

The core route is complete only after both endpoint and channel gates pass,
including Weather CH01 and workflow CH02. Proceed to [capstone selection](CAPSTONE.md)
only if the participant chooses the optional follow-on.
