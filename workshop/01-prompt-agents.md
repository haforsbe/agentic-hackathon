# Prompt agents: build two complementary specialists

Build two independently publishable Microsoft Foundry Prompt Agents. The
**Weather Research Agent** owns weather evidence. The **Cultural Travel Agent**
owns published art-tourism, museum, and cultural-trip evidence, including only
the accessibility information its sources actually supply.
Each follows the same seven-step learning progression with independent
evidence. Teach the method with the first agent, then use shorter reminders
and focus on differences with the second; do not repeat introductory lectures.

Keep reproducible definitions and test clients under `student/prompt-agents/`.
Use current supported APIs and isolated dependencies, not the old root pins.
The coach checks evidence after each change and understanding once per
checkpoint, using an explanation already given when sufficient. Do not add a
quiz after every action or test reply.
Use [TESTS.md](TESTS.md) and introduce the related
[app technique](APP-GUIDE.md) at each checkpoint.
Use the [execution matrix](TESTS.md#checkpoint-execution-matrix) and
[shared helper](runner/README.md) for supported operations instead of creating
new clients during teaching. Keep student definitions under `student/`;
the helper is workshop plumbing, not a finished specialist implementation.

Use the [mixed test plan](APP-GUIDE.md#where-tests-and-exploration-happen)
throughout both specialists, aiming for 50/50 coach-sent and participant-sent
test prompts across each specialist's lessons: the coach demonstrates from the Copilot app, then
the participant copies a prompt into the exact agent's Foundry Playground,
sends it once, and brings the actual result back for review. Allocate remaining
required tests between the routes, tracking the running split rather than
adding duplicate calls. Explain and record capability or participant-preference
exceptions to the target. Keep
controlled identity, failure, and consumer-endpoint checks on a supported client
when the Playground cannot supply the required evidence. Agree on each handoff,
its context, cost, and tool approvals before sending.

For both specialists, the coach supplies the selected server URL, actual tool
schemas, and configuration plan from [MCP-SERVICES.md](MCP-SERVICES.md).
Participants do not research endpoints, supply keys, or deploy MCP servers.
Use the same explain, approve, configure, test, inspect, and teach-back loop
for each. The shared New York trip develops into the two-agent workflow only
after both agents pass independently; do not jump ahead to orchestration.

Use the [five-to-six-hour core agenda](FACILITATOR.md#five-to-six-hour-core-agenda):
about 110 minutes for Weather and 70 for Cultural Travel. Same support,
approval boundaries, and test coverage; less repeated explanation on agent 2.
Coach-side checks may be grouped within the approved current-step test budget.
Do not add optional exploration or backend debugging to every checkpoint.

## 01: Create the Weather Research Agent

**Concept:** a Microsoft Foundry Model Deployment plus instructions creates a
Microsoft Foundry Prompt Agent.

Create a minimal Weather Research Agent without tools, persistent memory, or a
skill. It can explain stable weather concepts from trained model knowledge, but
it must not claim current weather without an external source. Ask when location
or time context is missing and do not claim access the agent does not have.

After approval, create a uniquely named agent using the installed skill or the
[current quickstart](https://learn.microsoft.com/en-us/azure/foundry/agents/quickstarts/prompt-agent).
Record its actual name/version and run B01-B03 with weather-appropriate inputs.
Have the coach demonstrate B01, then guide the participant to send B02 and B03
in separate fresh Conversations and copy each reply back to the Copilot app.

**App practice:** ask "Explain, don't edit," then separately request the change.
**Alternative:** ask for a proposed definition diff before implementation.
**Teach-back:** "What defines this agent, and what has not been added yet?"

## 02: Refine Weather instructions

**Concept:** improve one measurable behavior while holding the model and
capabilities constant.

Add headings such as `Answer`, `Source`, and `Uncertainty`. Require general
knowledge to be labeled accurately and prohibit invented sources, current
weather claims, or unsupported capabilities. Create a candidate version rather
than silently changing the tested version.

Run I01 with the same inputs before and after the change. Inspect the actual
version metadata and responses. Do not change the Microsoft Foundry Model
Deployment or add tools at the same time.
Let the participant send at least one matched before/after prompt pair, with
the same input and fresh context on both versions; use the coach route for the
remaining comparisons. Reuse the saved baseline input/reply as each before
side; do not generate another before-run merely for the comparison.

**App practice:** review the focused instruction diff before creating the version.
**Alternative:** request an instruction proposal without applying it.
**Teach-back:** "Which behavior changed, and what evidence ties it to the instructions?"

## 03: Test Weather managed Conversations

**Concept:** Microsoft Foundry automatically maintains history within one
Conversation identifier. Persistent memory is a separate capability.

**Before the tests:** verify the
[portal trace prerequisite](SETUP.md#portal-trace-prerequisite), including the
project's Application Insights connection and the participant's telemetry-read
access. Conversation history does not depend on this portal trace setup.
If tracing is unavailable, explain the blocker; preserve any completed
Conversation tests and inspect their service-returned evidence without claiming
the portal exercise passed. Do not connect resources or repeat paid tests
without separate approval.

In one Conversation, provide a destination and weather interest, then ask a
follow-up that relies on that context. In a new Conversation, ask the follow-up
again. Follow the [rehearsed navigation](APP-GUIDE.md#foundry-navigation-rehearsed-before-the-workshop):
**Build → Agents → the exact agent → Traces**. Use **Trace view** to find
a response and inspect its relevant span's **Metadata**, and **Conversation
view** to locate a saved Conversation (`conv_`). Explain that the Response
ID (`resp_`) identifies one reply, not the conversation, and the Trace ID
identifies its execution record. Fields vary by span; use a supported client
to verify identifier linkage when it is not exposed. Do not infer linkage
from a similar-looking reply or adjacent table row.
Do not build a custom history store or manually replay messages.

Run D01-D02 with weather-appropriate prompts. The application remains
responsible for mapping an authorized user/session to the correct Conversation
identifier. A GitHub Copilot app session is not a runtime Conversation.
Prefer participant-run messages for the complete sequence when the Playground
supports the required Conversation behavior and identifier evidence; otherwise
demonstrate with the supported client without claiming a UI feature exists.

**App practice:** contrast the coaching session with both runtime Conversations.
**Alternative:** discuss when a separate app session helps isolate another task.
**Teach-back:** "What did Microsoft Foundry manage, and what remains the client's responsibility?"

## 04: Connect the first Weather MCP tool

**Concept:** connect one remote evidence tool, prove its execution, and learn
the difference between a plausible answer and observed runtime evidence.

The coach provides the public **Weather MCP server** endpoint
`https://weather.datakoot.com/mcp` and discovers its current schemas without
credentials. Explain `weather_forecast` and its required numeric `lat` and
`lon` inputs; optional `hourly=false` selects daily periods. Use the first-tool
configuration and coverage guidance in [MCP-SERVICES.md](MCP-SERVICES.md).
Before opening the agent's tool picker, explain the route **agent -> pinned
Microsoft Foundry Toolbox -> Weather MCP server -> `weather_forecast`**.
The Toolbox attachment can itself appear as an MCP tool: its saved Microsoft
Foundry Toolbox URL and separate authentication reference distinguish it from
a direct public-server attachment. Do not promise a Toolbox option under
**Add**; if only direct tools are available, explain the rehearsed
coach-executed SDK/API alternative before requesting its separate approval.
Follow the [advance explanation and picker guidance](TOOLS-AND-TOOLBOXES.md#explain-the-attachment-before-opening-the-picker)
and [participant inspection steps](APP-GUIDE.md#before-adding-a-toolbox-backed-tool).
Do not create a direct candidate as an intermediate experiment.

After scoped approval, first register the server as a reusable Microsoft
Foundry project tool connection.
Create a Weather-only Toolbox referencing that connection and selecting only
`weather_forecast`, then authenticate and attach its verified version-specific
endpoint to a new Weather candidate, following
[Tools and Toolboxes](TOOLS-AND-TOOLBOXES.md).
Keep tool-call approval required and independently read back the definition.
Use the separately approved Toolbox-authentication connection, not the
anonymous upstream connection, on the agent binding. Keep `server_url`;
a connection reference does not replace it. Discover the exposed tool name,
update the candidate's allowlist and name references, and verify runtime
identity access separately. Saving either object does not run or authorize
its tools. Inspect both connections, the Toolbox and agent binding;
require T01/T03-at-04 as well as C01/C03.
Do not ask the participant to supply server details or host a service.
Verify Foundry-side execution rather than assuming local discovery proves it.

Run C01 with a supported location and C03a/C03b with unsupported input and an
isolated controlled MCP failure (for example approval denial, not a claimed
provider outage). For the first successful MCP call in the workshop, guide the
participant through Microsoft Foundry trace inspection. Locate the forecast
tool span and inspect its arguments, status, timing, returned source/timestamp,
and relationship to the final response. The agent must report failure rather
than invent weather.

Registering an MCP server for the GitHub Copilot app does not attach it to the
Microsoft Foundry agent. Never disable approvals globally to make a test pass.

**App practice:** inspect the reusable upstream connection, Weather Toolbox, separate authentication connection and agent binding; compare these with Copilot's separate MCP registration.
**Alternative:** inspect a sanitized direct MCP response before the agent call.
**Teach-back:** "Which trace evidence proves the forecast tool supplied the result?"

## 05: Guide multiple Weather tools with a skill

**Concept:** a skill can guide how an agent selects and sequences already
available tools; it does not connect tools or grant authorization.

Recheck the selected server's current schemas. Separately approve expansion
from `weather_forecast` to these four Weather MCP tools:

- `geocode` for supplied US addresses or city names;
- `weather_forecast` for future weather within the returned forecast horizon;
- `weather_current` for current station observations; and
- `weather_alerts` for relevant official US state alerts.

Reuse checkpoint 04's saved connection; do not register another Weather server.
Create a new Weather-only Toolbox version selecting the four approved tools,
verify their actual exposed names, and update this candidate's pinned endpoint,
authentication connection and allowlist. Do not change every consumer of
the upstream connection. Cultural deepens the same Toolbox pattern at 11.

The coach supplies the verified inputs from MCP-SERVICES.md and guides the
allowlist change; other discovered tools remain excluded. Do not invent
coordinates or claim non-US weather coverage.

Author a versioned weather-research skill under `student/skills/`. It should
guide input validation, tool selection, ordering, restraint, provenance,
partial failures, and stopping when prerequisite evidence is missing. For
example, resolve an ambiguous location before requesting its forecast, but do
not call every weather tool for every question.

Use the supported prompt-agent skill-delivery mechanism. If the environment
requires reviewed static composition, label it accurately; do not claim dynamic
loading. Preserve the governing instructions when composing the procedure:
Answer, Source and Uncertainty still apply to acknowledgements, clarifications
and refusals. Check the Weather service's US-only coverage before proposing
any of its tools, including `geocode`; retained Conversation context does not
grant unsupported coverage. A successful tool call alone does not pass these
instruction and routing assertions.
Run S01 across targeted, ambiguous, general-knowledge, and controlled
failure cases. Inspect traces to verify the chosen tool sequence, but checkpoint
04 remains the full trace-navigation lesson.

Formal machine-readable result contracts are intentionally deferred until
checkpoint 15, when workflow code needs to validate two agent results.

**App practice:** review the skill diff, exact version, delivery strategy, and allowlist change.
**Alternative:** validate the procedure against recorded fixtures before a paid call.
**Teach-back:** "How can a skill guide tool use without granting access?"

## 06: Add and test Weather memory

**Concept:** managed Conversation history and persistent memory solve different
problems.

Add a student-owned persistent-memory capability using the
[current memory guide](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/memory-usage).
Use a low-risk, explicitly consented preference such as Celsius temperature
units. Store only the minimum useful fact, map scope from trusted identity, and
support inspection, correction, and deletion.

Inspect every fact retained by automatic memory processing, not just the
requested preference. Extraction instructions such as `user_profile_details`
are not proof of an enforced storage allowlist. Include response-linked
background updates and their usage in the evidence; a completed reply does
not prove that memory processing has finished. If an out-of-scope fact is
stored, preserve the failure, obtain approval for its exact cleanup and stop
further tests until the correction is reviewed. Correct recall alone does not
pass data minimization.

Do not silently replace automatic memory with an API-managed harness or
disable extraction to obtain a pass. Such alternatives change the candidate,
trusted identity/data boundary and consumer behavior, so they require separate
design/operation approval and matched correction, isolation, deletion and
consumer-path evidence. A project-client injection of a preference does not
prove memory works through the Stable Agent Endpoint or a published channel.

Run M01-M03 with weather-appropriate preferences. In a new Conversation, memory
may supply the preferred unit while Weather MCP tools still supply current
weather evidence. A retrieval failure must not become a false claim that the
preference was remembered.

Re-run one MCP and skill-guided response to prove memory personalizes
presentation without changing tool authorization, provenance, or factual data.

**App practice:** save and resume workshop progress; identify where it is stored.
**Alternative:** discuss progress import into another worktree without confusing it with agent memory.
**Teach-back:** "What came from memory, and what still had to come from the Weather MCP server?"

## 07: Release the Weather Research Agent

**Concept:** release selects a fully tested candidate behind a Stable Agent
Endpoint. A known-failing candidate is never promoted as the stable release.

The candidate already uses the Weather-only Toolbox introduced at 04 and
expanded at 05. Follow [Tools and Toolboxes](TOOLS-AND-TOOLBOXES.md):
verify its pinned version-specific endpoint, both connection records, runtime
identity access, four-tool effective restrictions and actual approval/denial.
Require T03-at-07. Do not create another Toolbox or migrate a direct candidate
as a planned release task. Finalize any separately approved correction before
the suite below, so the checks cover the actual release path once.

Follow [PUBLISHING.md](PUBLISHING.md). Run the complete Weather Agent regression
suite, verify its exact agent version, skill revision, tool allowlist, memory
configuration, and Microsoft Foundry Model Deployment, then run P01-P03 through
the Stable Agent Endpoint.

Before moving to checkpoint 08, follow
[channel publication at 07](PUBLISHING.md#required-channel-publication-at-07-and-16).
The participant chooses Microsoft Teams, Microsoft 365 Copilot, or both,
approves the publication scope separately, publishes this released Weather
agent and uses it from at least one chosen surface. Run CH01 with real
channel input/reply and correlated Microsoft Foundry execution evidence.
Retain tool approvals, provenance and user isolation; a successful publish
dialog or Playground reply is not a channel pass. Keep the stable endpoint's
direct-client access for the later workflow. If blocked, preserve release
evidence but do not pass 07 or silently start the second agent.

The released agent returns a consistent evidence-aware weather briefing with
destination, dates, findings, tool/source provenance, timestamps, uncertainty,
and missing information. It does not provide cultural recommendations or a
complete itinerary.

Before release, check this briefing against the facilitator-rehearsed workflow
handoff checklist: owning agent/version, destination/constraints, findings,
provenance and available timestamps, uncertainty, missing information and
explicit failure status. Check content with real outputs now; formal schemas
and executable validation are still taught at 15. Do not promise that arbitrary
prose will automatically satisfy the later contract.
Use service-returned release metadata for runtime agent/version fields; never
ask the model to invent its version or treat a self-reported version as proof.

Retain failed candidate test evidence for diagnosis, but keep that candidate
out of stable routing. Rollback is reserved for an unforeseen issue discovered
after a fully passing version was promoted.

**App practice:** distinguish endpoint release from channel publication; send
the Weather test in the chosen channel and review its evidence in the GitHub Copilot app.
**Alternative:** inspect sanitized raw responses instead of a narrative summary.
**Teach-back:** "How do you know the Weather reply in Microsoft Teams or
Microsoft 365 Copilot came from your tested release, and why is publishing
different from creating the agent?"

### Optional lab after Weather 07: GitHub delivery

After checkpoint 07 passes, including CH01, offer the separate
[Weather-agent GitHub delivery lab](weather-delivery/README.md) before
checkpoint 08. It practices a reviewed configuration PR, offline CI, and a
GitHub-Actions promotion from a manually edited Dev Weather agent to a
separate Prod Weather agent. It is not a new numbered checkpoint, does not
alter the 00-16 core or its 5-6-hour estimate, and does not add work for
Cultural Travel or the hosted workflow.

Explain the tradeoff first: Dev and Prod are separate agent resources in one
Microsoft Foundry Project, an educational compromise, **not production best
practice**. Project dependencies, permissions, quotas, and audit boundary are
shared. GitHub Actions captures the selected saved Dev version, opens a PR
that shows the tracked configuration being replaced, runs automated offline
checks, and lets the participant manually deploy a created or reused version
to the existing Prod agent after merge, confirming the full reviewed commit
and deployment intent.
No GitHub Environment is required. If GitHub requires workflow-run approval,
review the workflow and use its displayed approval control if authorized, or
involve the owner; do not bypass the policy. That approval is not deployment
or tool approval. PR checks are automated
contract tests, not an AI review; the participant reviews and merges the diff.

The deployment copies the captured agent definition, not project resources,
credentials, Conversations, transcripts, memory contents, or external skill
files. Shared Foundry dependencies remain in the project. Offline checks prove
package consistency only; deployment read-back proves a version was created
or reused and selected, not that MCP authentication or tool execution works. Those
runtime checks remain independent and may be blocked by the Toolbox
authentication investigation. The CI identity, participant/runtime identity,
and agent runtime identity are distinct. Neither merge approval nor a GitHub
manual deployment confirmation substitutes for per-call MCP approval. Live workflows
remain unavailable until the facilitator configures and rehearses repository
variables, branch-based OIDC trust, required permissions, and manual deployment.
Finish with read-back and the lab guide's separately approved manual
basic-response test on the exact deployed Prod version. Record the observed
scope: a portal answer is not proof of the stable endpoint or Weather tools.
Automated runtime verification is optional until its corrected endpoint route
is successfully live-rehearsed; a blocked test remains explicitly unverified.
On skip or completion, resume directly at Cultural checkpoint 08; never
renumber or mark any core checkpoint passed.

**Teach-back:** "What does merging the capture PR approve, and what does the
separate commit-confirmed manual deployment allow GitHub Actions to do?"

## 08: Create the Cultural Travel Agent

**Concept:** the second specialist repeats the same lifecycle with a different
evidence responsibility.

Start with a short reminder: "We'll use the method you learned with Weather,
but this agent owns museum and art-trip evidence." Supply its new target and
MCP information when needed. Reuse familiar navigation and explain only
differences; the repeated tests prove independence, not a need to repeat the
full introduction. Apply this pacing through checkpoint 14.

Require the Weather endpoint release and CH01 channel milestone at 07 first.
Weather remains available in its chosen channel while Cultural is built.
The Cultural lessons and independent release are unchanged; there is no
additional required Cultural channel publication.

Create a separate Cultural Travel Agent without tools, memory, or copied Weather
Agent state. It may answer stable, general cultural questions while labeling
them as general knowledge. It must not claim current opening hours,
accessibility conditions, event schedules, prices, or weather without evidence.
Run B01-B03 with cultural-travel inputs.
Repeat the demonstration/practice split: coach sends B01; participant sends B02
and B03 and brings each reply back, rather than making agent 2 coach-only.

**App practice:** compare the two minimal agent definitions.
**Alternative:** request a proposed definition before implementation.
**Teach-back:** "What is independent about agent 2, and what has not been added?"

## 09: Refine Cultural instructions

**Concept:** improve the second specialist through the same controlled
instruction-version comparison.

Add `Guidance`, `Source`, and `Uncertainty` headings. Require respectful language,
stereotype avoidance, missing-context questions, and clear separation between
general knowledge and current venue-specific evidence. Keep the Microsoft
Foundry Model Deployment and capabilities unchanged. Run I01.

**App practice:** review the focused instruction diff and matched tests.
**Alternative:** keep the change proposal-only until expectations are clear.
**Teach-back:** "What can this tool-free version explain, and what can it not verify?"

## 10: Test Cultural managed Conversations

**Concept:** repeat Conversation continuity and isolation for the second agent.

Recheck the [portal trace prerequisite](SETUP.md#portal-trace-prerequisite) for
this project's current connection and inspection identity before the tests.
The Weather Agent's successful tracing exercise is not proof of trace access
for another project or identity.

Within one Conversation, state a destination and interest, then ask a follow-up.
In a new Conversation, verify that the destination is not imported
automatically. Run D01-D02 with cultural-travel prompts.

The Cultural Travel Agent has its own authorized Conversation mapping. It
cannot read the Weather Research Agent's Conversation history.

**App practice:** keep one coaching session while testing separate runtime Conversations.
**Alternative:** use a separate app session only for a genuinely separate task.
**Teach-back:** "Why does a new Cultural Agent Conversation ask for context again?"

## 11: Connect the first Cultural Travel MCP tool

**Concept:** use a Foundry Toolbox to manage access to one curated
cultural-evidence tool before introducing multi-tool routing.

Repeat the checkpoint 04 coaching behavior for agent 2. The coach provides
the public **travel.art MCP server** endpoint `https://mcp.travel.art/`,
discovers its current schemas without credentials, and explains
`find_museum_guide` and its optional `query`, `city`, and `country` filters.
Use [MCP-SERVICES.md](MCP-SERVICES.md), including the exact first-tool definition
and copy-ready New York museum prompt. Do not ask the participant to find an
endpoint, obtain a key, register a Cloudflare account, or deploy a server.

Follow [Tools and Toolboxes](TOOLS-AND-TOOLBOXES.md): register the reusable
travel.art project tool connection, create a Cultural-only Toolbox version
exposing only `find_museum_guide`, and attach the returned version-specific
Toolbox endpoint to this agent's new candidate. Explain the new boundary:
the connection saves the upstream settings; the Toolbox manages a reusable
collection; the agent consumes its endpoint. Approve current-step changes
explicitly and independently read them back. Verify the runtime identity can
invoke Toolbox and approval still covers each actual upstream operation.
Require T01/T02 as well as C02/C03. Do not change the released Weather Agent
or attach its tools to Cultural Travel. Missing Toolbox support blocks this
gate; direct integration is not a Toolbox pass.
Before opening the picker, briefly remind the participant that this Toolbox
also appears as an MCP attachment: verify its Microsoft Foundry Toolbox URL
and separate authentication reference, not its display name. Reuse 04's
supported route if the picker only offers direct tools; do not restart a UI
search or attach the public travel.art URL as a substitute.
The source is travel.art's published museum guides, not live ticket inventory
or an official venue verification service.

Run C02 for a supported destination and C03a/C03b for unsupported/malformed
input and an isolated controlled MCP failure, labeled by its actual cause.
Inspect the MCP Server Endpoint, tool schema, arguments, result, `guideUrl`,
available `lastVerified` metadata, attribution, and grounded response. Do not
require an invented dataset version. Reuse the trace-inspection knowledge
from checkpoint 04: verify the tool span and result without repeating the full
navigation lesson unless the participant needs it.

**App practice:** inspect the saved tool, Toolbox version and agent binding; verify the one-tool effective allowlist.
**Alternative:** inspect a sanitized direct MCP response before the agent call.
**Teach-back:** "What proves the museum-guide tool supplied the attributed facts?"

## 12: Guide multiple Cultural tools with a skill

**Concept:** repeat skill-guided tool routing in a new evidence domain.

The coach supplies the live schemas and separately requests approval to expand
to the four selected travel.art tools: `find_museum_guide`, `find_art_events`,
`find_layover_itinerary`, and `recommend_art_trip`. See MCP-SERVICES.md for
their exact filters, date formats, catalogue limits, and source fields.
There is no standalone accessibility or etiquette tool.
Reuse the saved connection in a new Cultural-only Toolbox version; pin the
candidate to its returned version-specific endpoint. Read back the Toolbox
and agent, check actual exposed names against the skill, and retain per-call
approval. Do not expand a shared default or expose Weather tools.

Create a versioned cultural-research skill that guides which tool to use, in
what order, when not to call one, how to preserve guide attribution/freshness,
and how to expose partial failures. A provider-supplied cultural itinerary is
not our hosted workflow and contains no Weather Agent execution evidence.

The skill must distinguish missing accessibility information from proof that a
venue is accessible or inaccessible. If museum retrieval succeeds while an
event lookup fails, preserve the grounded museum guidance and report the event
failure. If accessibility information is absent from the returned guides,
state that it is unavailable; do not invent a separate retrieval.

Run S02 across museum lookup, art events, covered layovers, cultural trip
recommendations, missing accessibility information, unrelated-tool restraint,
and partial-failure cases. Use separate requests to exercise tool roles rather
than calling all four for every question.

**App practice:** review the skill and allowlist diffs separately.
**Alternative:** validate recorded tool results before live agent calls.
**Teach-back:** "How did the skill choose only the tools needed for this request?"

## 13: Add and test Cultural memory

**Concept:** repeat the persistent-memory lifecycle with an independent,
low-risk cultural preference.

Use a preference such as museums over nightlife. Obtain consent, store the
minimum fact, inspect its scope, verify retrieval in a new Conversation, correct
it, delete it, and prove the deleted value is no longer applied. Run M01-M03
against the Cultural Agent's separately approved memory scope.

Memory supplies the preference; travel.art MCP tools supply the published
museum, event, or cultural-trip facts. Do not store an unnecessary reason that
could reveal sensitive information.

**App practice:** pause, resume, and recheck the exact agent and memory scope.
**Alternative:** explain why a stateless design would be safer when memory adds no value.
**Teach-back:** "Which evidence came from memory, and which came from the MCP tools?"

## 14: Release the Cultural Travel Agent

**Concept:** the second specialist must independently pass the same release
discipline before orchestration begins.

Weather's release from 07 is already Toolbox-backed. Check its current
release/version and pinned dependencies read-only, and reuse its valid
unchanged-path evidence. Do not migrate Weather or run another full Weather
suite just for this handoff. If a real configuration, dependency or caller
scope change invalidates evidence, explain it and approve the affected
regressions separately. Keep the two domain Toolboxes independent.

Run the complete Cultural Agent regression suite. Verify its exact version,
skill revision, travel.art tool allowlist, memory configuration, source
attribution, and freshness caveats. Promote only a fully passing candidate to
its own Stable Agent Endpoint and run P01-P03.

Apply the same pre-release handoff checklist to actual Cultural results:
owning agent/version, destination/constraints, findings, guide/source
provenance and available verification dates, uncertainty, missing information
and explicit failure status. Preserve its cultural-only evidence boundary.
Formal schemas and workflow validation remain at 15.
Runtime agent/version identity comes from service metadata, not a model guess.

Invoke both stable specialists independently for the same destination. The
Weather Research Agent must not claim cultural retrieval; the Cultural Travel
Agent must not claim weather retrieval. Record both names, versions, endpoints,
identities, tool connections, skill revisions, memory scopes, and release
evidence.
Include each reusable connection ID, Toolbox version/endpoint and effective
tool selection. Verify neither agent can discover or invoke the other domain's
tools, including through any Toolbox dispatch/search facility.

**App practice:** request a two-agent handoff table backed by live metadata.
**Alternative:** inspect sanitized raw responses from both endpoints.
**Teach-back:** "Why must both agents pass independently before workflow code is added?"
