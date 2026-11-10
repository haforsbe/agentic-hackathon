# Hosted agents: orchestrate the two prompt specialists

Keep both tested prompt-agent releases. Build a Microsoft Agent Framework
workflow that invokes them, validates their results, and produces a sourced
itinerary. Do not port their MCP tools, memories, skills, or specialist
instructions into the hosted runtime.

Use [TESTS.md](TESTS.md) and [APP-GUIDE.md](APP-GUIDE.md). Use a current official
hosting sample and the installed Microsoft Foundry skill workflow, not an old
console script as a server entry point.

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

Define versioned weather-result and cultural-result contracts based on observed
specialist outputs. Each contract should require the owning agent/version,
destination and relevant constraints, findings, source/tool provenance,
timestamps where applicable, uncertainty, missing information, and explicit
failure status. Contracts validate structure; correlated traces and release
evidence remain the proof of execution.

If a released specialist cannot produce a contract-compatible result, create a
new specialist candidate, fully retest it, and promote it before continuing.
Do not silently reinterpret incompatible output inside the workflow.

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

Run G01-G03 and W01-W03 locally with recorded fixtures, then with approved live
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
