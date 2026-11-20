# Prompt agents: build two complementary specialists

Build two independently publishable Microsoft Foundry Prompt Agents. The
**Weather Research Agent** owns weather evidence. The **Cultural Travel Agent**
owns published art-tourism, museum, and cultural-trip evidence, including only
the accessibility information its sources actually supply.
Each follows the same numbered progression with independent evidence; skills
and memory at 05/06 and 12/13 are temporarily deferred under the
[skills](README.md#temporary-skills-and-multi-tool-deferral) and
[memory](README.md#temporary-memory-deferral) policies. Keep one tool per
specialist and continue 04 -> 07 and 11 -> 14.
Teach the method with the first agent, then apply that understanding with the
second. Explain domain-specific differences and their rationale; do not
automatically replace the second agent's teaching with shorter instructions.

Use the [whole-workshop teaching standard](COACH.md#explain-what-and-why-before-every-step).
The teaching explanations below are the foundation for each practical task,
not optional reading for participants who ask why. Expand them with the
participant's actual configuration and observed results. Give a short
[learning summary](COACH.md#close-each-meaningful-learning-step) after each
meaningful step within the lesson as well as at its close.
Summary examples are conditional on actual evidence, never assumed passes;
adapt them when a step is configured only, participant-reported or blocked.
Retained deferred sections are taught only after explicit reintroduction.

Keep reproducible definitions and test clients under `student/prompt-agents/`.
Use current supported APIs and isolated dependencies, not the old root pins.
The coach checks evidence after each change and understanding once per
checkpoint, using an explanation already given when sufficient. Do not add a
quiz after every action or test reply.
Be friendly and ready to explain when someone gets stuck. Accept clear
confirmation of routine manual work under
[participant trust](COACH.md#supportive-coaching-and-participant-trust), rather
than requesting screenshots, full copied replies or duplicate checks by default.
Use [TESTS.md](TESTS.md) and introduce the related
[app technique](APP-GUIDE.md) at each checkpoint.
All acceptance IDs in this lesson are internal coach references, not student
instructions. Follow [the learner-instruction rule](COACH.md#explain-what-and-why-before-every-step):
translate each case into the actual prompt/action, purpose, location/context
and expected result before addressing the participant.
Use the [execution matrix](TESTS.md#checkpoint-execution-matrix) and
[shared helper](runner/README.md) for supported operations instead of creating
new clients during teaching. Keep student definitions under `student/`;
the helper is workshop plumbing, not a finished specialist implementation.

Use the [mixed test plan](APP-GUIDE.md#where-tests-and-exploration-happen)
throughout both specialists, aiming for 50/50 coach-sent and participant-sent
test prompts across each specialist's lessons: the coach demonstrates from the Copilot app, then
the participant copies a prompt into the exact agent's Foundry Playground,
sends it once, and reports the observed result. A short confirmation is enough
for routine learning steps; request specific evidence only when needed.
Allocate remaining
required tests between the routes, tracking the running split rather than
adding duplicate calls. Explain and record capability or participant-preference
exceptions to the target. Keep
identity/scope verification and supported consumer-endpoint checks on a supported client
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
approval boundaries, and test coverage; reuse understood background on agent 2.
Coach-side checks may be grouped within the approved current-step test budget.
Do not add optional exploration or backend debugging to every checkpoint.

## 01: Create the Weather Research Agent

**Concept:** a Microsoft Foundry Model Deployment plus instructions creates a
Microsoft Foundry Prompt Agent.

**Teach before practice:** a callable model supplies language and reasoning
capabilities. An agent adds instructions describing its role, boundaries and
expected answers, plus any configured capabilities. Creating a prompt agent
does not train a new model. The same model can support agents with different
responsibilities because their instructions and available tools differ.

Compare the two agent approaches used in this workshop. A **Prompt Agent**
uses a model, saved instructions and supported capabilities with managed
execution; we do not need to implement its own serving application. A
**Hosted Agent** runs custom application code deployed to Microsoft Foundry,
which gives us explicit coordination logic but adds code, dependency and
hosting responsibilities. We start with Prompt Agents to learn model,
instruction and evidence boundaries before introducing that extra complexity.

Start without tools so the participant can identify what the model already
provides. A useful explanation of clouds can come from trained knowledge;
a current forecast requires an external source. Instructions can require
honesty about that boundary, but cannot create missing weather observations.
Explain why the Playground is useful: it lets the participant interact with
the selected agent/version before publishing it to other users. A good
Playground answer is not yet a released endpoint or channel result.

Create a minimal Weather Research Agent without tools, persistent memory, or a
skill. It can explain stable weather concepts from trained model knowledge, but
it must not claim current weather without an external source. Ask when location
or time context is missing and do not claim access the agent does not have.

After approval, create a uniquely named agent using the installed skill or the
[current quickstart](https://learn.microsoft.com/en-us/azure/foundry/agents/quickstarts/prompt-agent).
Record its actual name/version. For a new run, use these concrete exchanges;
on resume, retain the exact inputs already used rather than repeating them
just to adopt the examples below.

**Coach demonstration:** explain that the first question checks general weather
knowledge. Send the actual Weather agent:

```text
What is the difference between weather and climate?
```

Discuss the reply: weather describes short-term conditions, while climate
describes long-term patterns. The agent should identify this as general
knowledge rather than claim it retrieved a current forecast.

**Participant practice:** give the documented route to the exact agent's
Playground and selected version. Ask the participant to start a new empty
Conversation and send:

```text
How do clouds form?
```

Explain the purpose before sending: this checks another useful general-weather
explanation that the tool-free agent can provide. Ask the participant to
report what it explained in the GitHub Copilot app.
Accept a clear description of the answer;
request the actual reply only when needed for review or a specific assertion.

**Internal coach validation:** B01-B02, two supported general-knowledge answers.

**Learning summary:** "Now we have seen our tool-free agent explain general
weather concepts. Its model supplied the knowledge and its instructions
guided the response; we have not demonstrated current forecast access.
Next we will change the instructions and compare what that changes."

**App practice:** ask "Explain, don't edit," then separately request the change.
**Alternative:** ask for a proposed definition diff before implementation.
**Teach-back:** "What defines this agent, and what has not been added yet?"

## 02: Refine Weather instructions

**Concept:** improve one measurable behavior while holding the model and
capabilities constant.

**Teach before practice:** instructions are written guidance supplied to the
model when the agent responds. They can influence its role, structure,
questions and treatment of uncertainty. They are not fine-tuning, new facts,
an external data connection or an enforced authorization policy. Asking for
a Source section cannot make an invented citation genuine.

Distinguish an agent's instructions from the user's message: instructions
describe the saved role and standing guidance; the user supplies the current
task. A clearer user question and a revised agent definition are different
changes, so do not change both while trying to learn which caused an effect.

Compare changing instructions with changing the model or adding a tool:
each affects a different part of the system. Here the problem is how the
agent communicates its answer, so change only instructions. Saving a new
candidate version preserves the earlier configuration for comparison rather
than silently replacing it. Repeating the same question with equivalent fresh
context helps attribute a visible change to the instructions, not a different
input, tool or conversation history; it does not guarantee every future reply.

Add headings such as `Answer`, `Source`, and `Uncertainty`. Require general
knowledge to be labeled accurately and prohibit invented sources, current
weather claims, or unsupported capabilities. Create a candidate version rather
than silently changing the tested version.

Repeat the same two supported general-weather questions on the revised
agent and compare its replies with the saved earlier ones. Explain that this
checks whether the new sections improve clarity while the answers remain
accurate and honest. Inspect the actual
version metadata and responses. Do not change the Microsoft Foundry Model
Deployment or add tools at the same time.
Let the participant send at least one matched before/after prompt pair, with
the same input and fresh context on both versions; use the coach route for the
remaining comparisons. Reuse the saved baseline input/reply as each before
side; do not generate another before-run merely for the comparison.

**Internal coach validation:** I01, using the exact saved baseline inputs.

**Learning summary:** connect the actual before/after answers to the changed
instruction: "Now we have seen how the new instructions affect the answer's
structure and treatment of evidence. We changed its behavior, not its model
knowledge or access to live data. Next we will examine how earlier messages
affect a follow-up."

**App practice:** review the focused instruction diff before creating the version.
**Alternative:** request an instruction proposal without applying it.
**Teach-back:** "Which behavior changed, and what evidence ties it to the instructions?"

## 03: Test Weather managed Conversations

**Concept:** Microsoft Foundry automatically maintains history within one
Conversation identifier. Persistent memory is a separate capability.

**Teach before practice:** an isolated prompt contains only the information
made available for that request. A managed Conversation keeps a related
message history, so a later question can refer to a destination or interest
given earlier. The Conversation identifier selects that history; a Response
identifier names one reply, and a Trace identifier links execution evidence.
These objects answer different questions and are not interchangeable.

Compare a follow-up within one Conversation with the same follow-up in
another Conversation containing a different destination. The words of the
follow-up can stay the same while its context changes. This demonstrates
why history matters when testing or comparing versions: context can influence
the answer even when instructions do not change. It is not persistent memory,
proof of cross-user authorization or the GitHub Copilot app's coaching history.

**Before the tests:** verify the
[portal trace prerequisite](SETUP.md#portal-trace-prerequisite), including the
project's Application Insights connection and the participant's telemetry-read
access. Conversation history does not depend on this portal trace setup.
If tracing is unavailable, explain the blocker; preserve any completed
Conversation tests and inspect their service-returned evidence without claiming
the portal exercise passed. Do not connect resources or repeat paid tests
without separate approval.

In one Conversation, provide a destination and weather interest, then ask a
follow-up that relies on that context. Then create a new Conversation, supply
a different destination and interest, and ask the same follow-up. Test each
Conversation's own context rather than an intentionally context-free question.
Follow the [rehearsed navigation](APP-GUIDE.md#foundry-navigation-rehearsed-before-the-workshop):
**Build → Agents → the exact agent → Traces**. Use **Trace view** to find
a response and inspect its relevant span's **Metadata**, and **Conversation
view** to locate a saved Conversation (`conv_`). Explain that the Response
ID (`resp_`) identifies one reply, not the conversation, and the Trace ID
identifies its execution record. Fields vary by span; use a supported client
to verify identifier linkage when it is not exposed. Do not infer linkage
from a similar-looking reply or adjacent table row.
Do not build a custom history store or manually replay messages.

Run D01-D02 with weather-appropriate prompts. Explain the observed difference:
each Conversation retains the destination and interest supplied to it, with
distinct service-returned identifiers. A GitHub Copilot app session is not a runtime Conversation.
For coach-sent tests, the workshop runner supplies the Conversation identifier;
for participant-sent tests, the Microsoft Foundry Playground manages the test
interaction. Keep user/session mapping implementation details out of this
introductory explanation. When that boundary matters for a later consumer test,
name the actual backend or channel integration responsible for the mapping.
Prefer participant-run messages for the complete sequence when the Playground
supports the required Conversation behavior and identifier evidence; otherwise
demonstrate with the supported client without claiming a UI feature exists.

**Learning summary:** "We have now seen each Conversation use its own supplied
trip context. The latest message was not the agent's only input: the related
history mattered too. Next we will add an external evidence source rather
than relying only on model knowledge and messages."

**App practice:** contrast the coaching session with both runtime Conversations.
**Alternative:** discuss when a separate app session helps isolate another task.
**Teach-back:** "How did the agent's reply differ between the same Conversation and a new one?"

## 04: Connect the first Weather MCP tool

**Concept:** connect one remote evidence tool, prove its execution, and learn
the difference between a plausible answer and observed runtime evidence.

**Teach before practice:** tools extend what an agent can do beyond generating
an answer from the information already available to its model. Depending on
the tool, it can retrieve external information, perform calculations or ask
another system to take an action. The model requests an operation; the runtime
applies the supported authorization and approval rules, executes the permitted
request and returns the result for use in the answer. Instructions guide the
model; a tool supplies a concrete operation.

Explain the relevant configuration choices, without adding their setup:

- **Project connections** hold reusable connectivity/authentication
  configuration where required by a service. A saved connection does not
  automatically attach a tool to every agent or authorize every caller.
- **Toolboxes** are centrally managed, named and versioned tool collections
  exposed through an MCP-compatible endpoint. They can support shared
  configuration and governance across consumers, at the cost of another
  resource and lifecycle to manage.
- **Direct agent tools** configure the capability on the particular agent.
  This makes our single-purpose binding easy to inspect. Both direct tools
  and Toolboxes may use project connections where authentication requires one;
  these concepts are not three mutually exclusive permission levels.

We use a direct MCP binding because this exercise needs one public read-only
weather operation, not a shared enterprise tool catalogue. MCP, the
**Model Context Protocol**, lets a service describe its callable operations
and their input schemas. A server may expose many tools, but our allowlist
exposes only `weather_forecast` to this agent. Explain Toolboxes as an
architectural alternative, not a required resource or another exercise.
See the current [Toolbox overview](https://learn.microsoft.com/azure/foundry/agents/concepts/toolbox-overview)
for the comparison; do not imply every tool type supports every route.

Explain approval as a separate design choice. **Never require approval**
allows the permitted MCP operation to run without a per-call human prompt;
**Always require approval** pauses for a decision on each requested call.
Supported per-tool filtering can combine policies for different operations.
The runtime must enforce the policy; writing "ask first" in the instructions
is not an equivalent control. Read-only lookups can justify automatic
execution after reviewing their source and data scope; writes or sensitive
data need a separate risk assessment. Approval is not a substitute for
authentication, an allowlist or source validation.

For this new Weather binding, explain the existing creation choice:
**MCP, directly on this agent, Never require approval**
(`require_approval: "never"`), with only `weather_forecast` allowed.
That removes its per-call prompt, not current-step configuration approval,
paid-call approval or required decisions actually emitted by another path.
Preserve existing saved policies rather than editing them to match the example.

The coach provides the public **Weather MCP server** endpoint
`https://weather.datakoot.com/mcp` and the documented tool inputs.
Explain that this is a free public online service used for workshop learning
and testing: US locations, forecasts within the returned horizon, potentially
cached results, and changeable availability, terms and limits. Use public
locations; Microsoft Foundry execution and telemetry can still incur charges.
Keep this short reminder when using or revisiting the service.
Explain `weather_forecast` and its required numeric `lat` and
`lon` inputs; optional `hourly=false` selects daily periods. Use the first-tool
configuration and coverage guidance in [MCP-SERVICES.md](MCP-SERVICES.md).
Before opening the agent's tool picker, explain the direct route **agent ->
Weather MCP server -> `weather_forecast`**. Follow
[Direct MCP connections](MCP-CONNECTIONS.md) and the
[participant inspection steps](APP-GUIDE.md#before-adding-a-direct-mcp-tool).
There is no Toolbox, upstream credential or separate authentication connection
to configure for this public service.

After scoped approval, attach the direct first-tool fragment to a new Weather
candidate. Keep `server_url: "https://weather.datakoot.com/mcp"`, the explicit
one-tool allowlist; for a new coach-created tool set always allow
(`require_approval: "never"`), or encourage the participant to choose always
allow at creation. Keep existing tools as configured and do not ask about their
approval setting again. Omit
`project_connection_id` and credentials. Use the supported skill/API route
and shared runner where applicable, then independently read back the
definition and inspect the exact candidate. Keep the chosen model,
instructions and other agents unchanged. Saving a binding does not run or
authorize its tools. Require T01 and the supported C01 result.
Do not ask the participant to supply server details or host a service.
Verify Foundry-side execution rather than assuming local discovery proves it.

Offer both execution choices for the copy-ready New York forecast prompt from
MCP-SERVICES.md on this exact candidate. For participant execution, use the
[first-use Playground flow](APP-GUIDE.md#first-tool-use-in-the-playground).
If a tool-permission prompt
appears, briefly explain Approve, Deny and Auto approve, then have the
participant consider optional **Auto approve** for the displayed permitted Weather-tool
scope, especially for later Microsoft Teams use. Keep the existing setting if
preferred; automatic execution without a prompt is valid. Continue directly
to the returned forecast and its evidence. Do not
add a standalone connectivity check or a separate approval/denial drill;
record the actual choice and do not assume it applies outside the Playground.

For Workshop Coach execution, use the
[native-request decision flow](APP-GUIDE.md#first-tool-use-when-workshop-coach-sends)
and wait for the participant's exact decision before each matching runner
continuation. Keep the participant's configuration inspection and guided
trace exercise; record the route rather than claiming portal permission
controls were used. Do not send a duplicate demonstration prompt.

Use this same supported exchange for C01 and T01; do not add unsupported-input
or injected-failure exercises. For this first successful
MCP call, teach tracing before the navigation. A trace is the execution
timeline; a span records an operation within it, such as a tool call. Linking
the tool's arguments, status and result to this response helps distinguish
"a tool is configured" from "this request actually used it." Compare the final
answer with the returned source as well: successful execution does not
guarantee the model represented its result faithfully.

Then guide the participant through Microsoft Foundry trace inspection. Locate the forecast
tool span and inspect its arguments, status, timing, returned source/timestamp,
and relationship to the final response. The agent must report failure rather
than invent weather.

Registering an MCP server for the GitHub Copilot app does not attach it to the
Microsoft Foundry agent. Never disable approvals globally to make a test pass.

**Learning summaries:** after saving and inspecting the binding, explain
that the agent is configured to request a forecast, but retrieval has not
yet been demonstrated. After the supported request and trace inspection:
"We have now followed the request from the agent's tool arguments to the
weather service's result and the final answer. The model composed the reply;
the service supplied the forecast evidence." Include the observed source,
date coverage and cache/freshness limits rather than promising real-time data.

**App practice:** inspect the direct server URL and one-tool allowlist; compare the agent binding with the GitHub Copilot app's separate MCP registration without another approval-setting question.
**Alternative:** inspect a sanitized direct MCP response before the agent call.
**Teach-back:** "Which trace evidence proves the forecast tool supplied the result?"

## 05: Guide multiple Weather tools with a skill

**Temporarily deferred.** Skip this checkpoint and memory 06 on the default
route; continue from 04 to 07 with only `weather_forecast`. Retain the material
below for later explicit reintroduction under the
[skills deferral policy](README.md#temporary-skills-and-multi-tool-deferral).
Do not apply a draft skill, expand the allowlist, create a skill-only candidate
or run T02/S01 on this route.

**Concept:** a skill can guide how an agent selects and sequences already
available tools; it does not connect tools or grant authorization.

**Teach before practice, only when reintroduced:** adding more tools increases
the number of possible operations, not the agent's knowledge of the right
research process. A skill supplies a reusable procedure for deciding which
operation to request, in what order and when to stop. Compare an allowlist,
which limits available operations, with a skill, which guides how already
permitted operations are used. Neither replaces runtime authorization.
Explain the actual supported delivery mechanism rather than implying that a
local skill file is automatically loaded by a deployed agent.

Review the selected server's documented tools and resolve any required schema
details during configuration. Repeat the brief free-service and coverage
reminder from 04. Separately approve expansion
from `weather_forecast` to these four Weather MCP tools:

- `geocode` for supplied US addresses or city names;
- `weather_forecast` for future weather within the returned forecast horizon;
- `weather_current` for current station observations; and
- `weather_alerts` for relevant official US state alerts.

Keep checkpoint 04's direct server URL and label. Create a new Weather
candidate expanding only its allowlist to the four approved tools; verify
their actual upstream names and retain the configured approval policy. Do not
register a project connection or alter another consumer. Require T02 and S01.
Cultural applies the same direct-connection pattern independently at 11/12.

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
Run S01 with supported tool-backed and general-knowledge requests.
Inspect traces to verify the chosen tool sequence, but checkpoint
04 remains the full trace-navigation lesson.
Do not inject a partial failure or add a participant denial exercise.

Formal machine-readable result contracts are intentionally deferred until
checkpoint 15, when workflow code needs to validate two agent results.

**Learning summary:** relate the observed selected sequence to the procedure
and distinguish it from the separately configured tool permissions.

**App practice:** review the skill diff, exact version, delivery strategy, and allowlist change.
**Alternative:** validate the procedure against recorded fixtures before a paid call.
**Teach-back:** "How can a skill guide tool use without granting access?"

## 06: Add and test Weather memory

**Temporarily deferred.** Do not execute this checkpoint on the default route;
continue from 04 to 07 while skills 05 is also deferred. The material below is retained for later reintroduction
under the [memory deferral policy](README.md#temporary-memory-deferral).
Do not create memory resources or run memory tests merely to complete this slot.

**Concept:** managed Conversation history and persistent memory solve different
problems.

**Teach before practice, only when reintroduced:** Conversation history answers
"what was said in this exchange?" Persistent memory can retain selected
information for a later exchange, such as a consented temperature-unit
preference. That convenience introduces a storage and privacy lifecycle:
what is retained, whose scope it belongs to, how it is corrected and how it
is deleted. Compare retaining a useful preference with retaining an entire
conversation or an unnecessary reason for the preference. Memory personalizes
presentation; it does not supply current weather or grant tool access.

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

Re-run one MCP response, and skill-guided behavior only if a skill is configured,
to prove memory personalizes presentation without changing tool authorization,
provenance or factual data. Reintroducing memory alone does not require adding a skill.

**Learning summary:** distinguish what was recalled from what the weather
source supplied, and describe only the storage, correction and deletion
behavior actually verified.

**App practice:** save and resume workshop progress; identify where it is stored.
**Alternative:** discuss progress import into another worktree without confusing it with agent memory.
**Teach-back:** "What came from memory, and what still had to come from the Weather MCP server?"

## 07: Release the Weather Research Agent

**Concept:** release selects a fully tested candidate behind a Stable Agent
Endpoint. A known-failing candidate is never promoted as the stable release.

**Teach before practice:** creating a candidate lets us inspect and test a
configuration without declaring it ready for consumers. Release selects
which tested version the Stable Agent Endpoint serves. A stable address
therefore does not mean "whatever version was edited most recently."
Explain the selected version using service metadata, not the model's claim
about its own identity.

Compare testing a candidate in the Playground, invoking the released
endpoint as a consumer and publishing to Microsoft Teams or Microsoft 365
Copilot. They exercise different paths and identities. A successful answer
in one does not prove access or correct routing in another. Publishing
connects the tested agent to its user-facing destination; it does not create
a second weather implementation. Keeping the same release matters because
the later workflow must also invoke this independently working specialist.

The candidate already connects directly to the Weather MCP server introduced
at 04, with only `weather_forecast` on the default skills-deferred route. Follow
[Direct MCP connections](MCP-CONNECTIONS.md): verify its exact agent version,
server URL, effective restrictions and actual permission behavior on the release
path. Require T03-at-07. Do not add a Toolbox or authentication connection as
a release task. Finalize any separately approved correction before the suite
below, so the checks cover the actual release path once.

Follow [PUBLISHING.md](PUBLISHING.md). Run the complete Weather Agent regression
suite, verify its exact agent version, any configured skill revision, tool allowlist, and
Microsoft Foundry Model Deployment, then run P01-P03 through
the Stable Agent Endpoint.
For the default skills-and-memory-deferred route, omit T02/S01, M01-M03 and
post-memory variants; skills and memory are not release prerequisites.
Verify the single allowed tool with a supported request; no injected failure is required.
If skills, expanded tools or memory are already configured, retain their
applicable checks rather than silently disabling or removing them.

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

**Learning summaries:** after endpoint verification, name the exact tested
version now selected and explain why release differs from candidate creation.
After the actual channel exchange, explain what that request demonstrated
about the published route. If publishing is blocked, preserve the endpoint
result and say explicitly that channel use remains unverified.

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
runtime checks remain independent of successful configuration delivery.
The CI identity, participant/runtime identity,
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

**Teach before practice:** reuse the distinction between model, instructions
and tools, then explain the new design decision: one large agent could be
given both domains, but separate specialists make responsibilities, evidence
sources and changes easier to inspect independently. This agent owns cultural
guidance, not weather. Sharing a model deployment does not require sharing
instructions, Conversations or tool bindings.

Apply the participant's earlier understanding to the cultural baseline:
general museum-planning advice is different from verified opening hours or
ticket availability. Explain why a separate tool-free baseline is useful
before adding travel.art: it shows what this specialist contributes and what
still requires an external source. Reuse familiar navigation, but teach
domain-specific choices rather than assuming that remembering clicks proves
understanding. Apply this transfer approach through checkpoint 14.

Require the Weather endpoint release and CH01 channel milestone at 07 first.
Weather remains available in its chosen channel while Cultural is built.
The Cultural lessons and independent release are unchanged; there is no
additional required Cultural channel publication.

Create a separate Cultural Travel Agent without tools, memory, or copied Weather
Agent state. It may answer stable, general cultural questions while labeling
them as general knowledge. It must not claim current opening hours,
accessibility conditions, event schedules, prices, or weather without evidence.
**Coach demonstration:** briefly explain that this checks general cultural
knowledge, then send the Cultural Travel agent:

```text
How does an art museum differ from an art fair?
```

Discuss whether it gives a useful general explanation and labels its source
honestly.

**Participant practice:** guide the participant to a new empty Conversation
with this agent's selected version and give the actual prompt:

```text
How can I pace a day of museum visits?
```

Explain that this checks useful general planning guidance without claiming
current venue details. Ask what practical guidance the agent gives.
Accept a clear confirmation for routine observations; ask for an excerpt
only when it helps the participant or a specific assertion needs it.
For returning participants, reuse their saved cultural baseline inputs.

**Internal coach validation:** B01-B02, two supported general-knowledge answers.

**Learning summary:** "Now we have a second agent with its own responsibility
and baseline behavior. We reused the build method, not Weather's conversation
state or evidence. Next we will refine how this specialist separates guidance
from unsupported venue-specific claims."

**App practice:** compare the two minimal agent definitions.
**Alternative:** request a proposed definition before implementation.
**Teach-back:** "What is independent about agent 2, and what has not been added?"

## 09: Refine Cultural instructions

**Concept:** improve the second specialist through the same controlled
instruction-version comparison.

**Participant-facing opening:** adapt this explanation to the actual baseline,
not a compressed list of headings or configuration requirements.

Your agent already gives general cultural advice. Now we'll change its
**instructions - the written rules guiding its answers** - so you can
distinguish the advice from its evidence and limitations.

Each answer will have three sections:

- **Guidance:** the practical advice, such as how to pace museum visits.
- **Source:** what the answer is based on - general model knowledge or
  information you supplied.
- **Uncertainty:** missing trip details or venue-specific information that
  hasn't been verified, such as current opening hours.

We'll also instruct it to avoid cultural stereotypes and ask for important
missing details rather than guessing.

We'll **save the changed instructions as a new version**, inspect them in
Microsoft Foundry, then repeat the same two questions you already tested.
You'll compare the earlier and new answers to see whether these instructions
actually make the advice clearer and easier to assess.

**We're changing how the agent explains its answers - not adding live museum
information or changing its model.**

Connect this to the mechanism learned with Weather: instructions are context
for the model, not retraining or an authorization boundary. Compare the same
saved questions with equivalent fresh context so the participant can identify
the effect of this instruction change. Explain why source labels and
uncertainty matter especially for venue information that can become outdated.

**Coach execution:** obtain scoped approval before the version update or tests.
Change only the instructions, including respectful language, stereotype
avoidance, missing-context questions and the distinction between general
knowledge and current venue-specific evidence. Keep the Microsoft Foundry Model
Deployment and capabilities unchanged. Reuse the exact saved baseline inputs
on their original execution routes with equivalent fresh context.

**Internal coach validation:** I01, using the exact saved baseline inputs.

**Learning summary:** point to the actual changed guidance, attribution or
uncertainty in the matched replies. Explain that clearer source labeling
improves assessability, but does not itself verify current museum facts.

**App practice:** review the focused instruction diff and matched tests.
**Alternative:** keep the change proposal-only until expectations are clear.
**Teach-back:** "What can this tool-free version explain, and what can it not verify?"

## 10: Test Cultural managed Conversations

**Concept:** repeat Conversation continuity and isolation for the second agent.

**Teach before practice:** apply the earlier context model to a cultural trip.
A follow-up about a destination or museum interest should use the history
of its selected Conversation, not a different test's messages. The important
choice is which history accompanies the request, not simply which agent name
appears on screen. Compare two supplied contexts to make that distinction
observable again for this independent specialist.

Explain why this matters before collaboration: having two useful agents does
not automatically pass context between them. Later workflow code will supply
the relevant trip inputs explicitly. Separate test Conversations demonstrate
their own history behavior, not the authorization of every possible caller.

Recheck the [portal trace prerequisite](SETUP.md#portal-trace-prerequisite) for
this project's current connection and inspection identity before the tests.
The Weather Agent's successful tracing exercise is not proof of trace access
for another project or identity.

Within one Conversation, state a destination and interest, then ask a follow-up.
Create a new Conversation with a different destination and interest, then
verify that its follow-up uses that supplied context. Run D01-D02 with
supported cultural-travel prompts.

The Cultural Travel Agent has its own authorized Conversation mapping. It
cannot read the Weather Research Agent's Conversation history.

**Learning summary:** relate each observed follow-up to its own earlier
destination and interest, then explain which context the later workflow will
need to supply instead of assuming the specialists share a conversation.

**App practice:** keep one coaching session while testing separate runtime Conversations.
**Alternative:** use a separate app session only for a genuinely separate task.
**Teach-back:** "How did each Conversation keep track of its own destination?"

## 11: Connect the first Cultural Travel MCP tool

**Concept:** independently connect the second agent directly to one curated
cultural-evidence tool before introducing multi-tool routing.

**Teach before practice:** reuse the model -> permitted tool request ->
external result -> answer mechanism from Weather, then explain the source
difference. A museum guide is published reference material, not necessarily
an official venue's current record. `guideUrl` gives attribution;
`lastVerified`, when returned, describes catalogue freshness rather than
proving today's opening hours or available tickets.

The direct one-tool binding keeps this specialist's evidence responsibility
visible and separate from Weather's. Explain why the same connection pattern
does not imply the same data guarantees: a weather forecast and a published
museum guide have different coverage and freshness limits. Reuse understood
approval concepts and the existing creation policy without adding another
configuration-choice question or requiring a permission card to appear.

Repeat the checkpoint 04 coaching behavior for agent 2. The coach provides
the public **travel.art MCP server** endpoint `https://mcp.travel.art/`,
supplies the documented tool inputs, and explains
`find_museum_guide` and its optional `query`, `city`, and `country` filters.
Use [MCP-SERVICES.md](MCP-SERVICES.md), including the exact first-tool definition
and copy-ready New York museum prompt. Do not ask the participant to find an
endpoint, obtain a key, register a Cloudflare account, or deploy a server.

Follow [Direct MCP connections](MCP-CONNECTIONS.md): attach the public
`https://mcp.travel.art/` URL directly to this agent's new candidate, with
only `find_museum_guide` allowlisted. Use always allow
(`require_approval: "never"`) for a new coach-created tool; encourage the same
when the participant creates it. Keep existing settings without later questions
or approval-setting edits.
Omit `project_connection_id` and credentials. Reuse 04's supported
configuration and inspection route with a short reminder, not another full
navigation tour. Approve current-step changes explicitly, independently read
back the candidate, and verify the actual permission choice and execution.
Require T01 and the supported C02 result. Do not change the released Weather Agent
or attach its tools to Cultural Travel. No Toolbox or authentication
connection is required for this public upstream service.
The source is travel.art's published museum guides, not live ticket inventory
or an official venue verification service.

Offer both execution choices for the copy-ready museum-guide prompt. For
participant execution, use
[the first-use Playground flow](APP-GUIDE.md#first-tool-use-in-the-playground).
Give a short reminder of Approve,
Deny and Auto approve when the first tool request appears, then let the
participant consider optional **Auto approve** for the displayed permitted Cultural-tool
scope, especially for later channel use. Automatic execution without a prompt
is valid; continue to the guidance and source evidence. Do not repeat a
connectivity exercise or run a separate denial drill.
For Workshop Coach execution, use the
[native-request decision flow](APP-GUIDE.md#first-tool-use-when-workshop-coach-sends);
the participant still decides every exact pending tool request. Preserve portal
inspection and trace practice without claiming Playground controls were used
or sending a duplicate request.
Use the same supported exchange for C02 and T01 without an additional
unsupported-input or controlled-failure exercise.
Inspect the MCP Server Endpoint, tool schema, arguments, result, `guideUrl`,
available `lastVerified` metadata, attribution, and grounded response. Do not
require an invented dataset version. Reuse the trace-inspection knowledge
from checkpoint 04: verify the tool span and result without repeating the full
navigation lesson unless the participant needs it.

**Learning summaries:** distinguish saving the museum-tool binding from
observing it execute. After the supported result, connect the actual guide
and its metadata to the response: the tool supplied attributable cultural
evidence, but did not establish live booking availability or weather.

**App practice:** inspect the direct server URL and agent version; verify the one-tool effective allowlist without another approval-setting question.
**Alternative:** inspect a sanitized direct MCP response before the agent call.
**Teach-back:** "What proves the museum-guide tool supplied the attributed facts?"

## 12: Guide multiple Cultural tools with a skill

**Temporarily deferred.** Skip this checkpoint and memory 13 on the default
route; continue from 11 to 14 with only `find_museum_guide`. Retain the material
below for later explicit reintroduction under the
[skills deferral policy](README.md#temporary-skills-and-multi-tool-deferral).
Do not add skills or tools, create a skill-only candidate or run T02/S02
on this route.

**Concept:** repeat skill-guided tool routing in a new evidence domain.

**Teach before practice, only when reintroduced:** explain why several
operations need selection and restraint rather than calling everything.
A museum lookup, event lookup and itinerary catalogue query serve different
questions. The cultural skill guides their use and treatment of missing
information; the allowlist and saved approval policy still control access.
An upstream itinerary result is not coordination of our two released agents.

The coach supplies the live schemas and separately requests approval to expand
to the four selected travel.art tools: `find_museum_guide`, `find_art_events`,
`find_layover_itinerary`, and `recommend_art_trip`. See MCP-SERVICES.md for
their exact filters, date formats, catalogue limits, and source fields.
There is no standalone accessibility or etiquette tool.
Keep the same direct server URL and label in a new Cultural candidate.
Expand only its allowlist, read back the agent version, check actual upstream
names against the skill, and retain the configured approval policy. Require T02
and S02. Do not change Weather's binding or expose Weather tools.

Create a versioned cultural-research skill that guides which tool to use, in
what order, when not to call one, how to preserve guide attribution/freshness,
and how to expose partial failures. A provider-supplied cultural itinerary is
not our hosted workflow and contains no Weather Agent execution evidence.

The skill must distinguish missing accessibility information from proof that a
venue is accessible or inaccessible. If museum retrieval succeeds while an
event lookup fails, preserve the grounded museum guidance and report the event
failure. If accessibility information is absent from the returned guides,
state that it is unavailable; do not invent a separate retrieval.

Run S02 across supported museum lookup, art events, covered layovers and
cultural trip recommendations. Report any genuinely missing information
honestly, without manufacturing a failure or denial exercise. Use separate
requests to exercise tool roles rather than calling all four for every question.

**Learning summary:** use the observed request to explain why its selected
operation matched the question and which unrequested tools were unnecessary.

**App practice:** review the skill and allowlist diffs separately.
**Alternative:** validate recorded tool results before live agent calls.
**Teach-back:** "How did the skill choose only the tools needed for this request?"

## 13: Add and test Cultural memory

**Temporarily deferred.** Do not execute this checkpoint on the default route;
continue from 11 to 14 while skills 12 is also deferred. The material below is retained for later reintroduction
under the [memory deferral policy](README.md#temporary-memory-deferral).
Do not create memory resources or run memory tests merely to complete this slot.

**Concept:** repeat the persistent-memory lifecycle with an independent,
low-risk cultural preference.

**Teach before practice, only when reintroduced:** apply the distinction
between current Conversation context, a retained preference and external
cultural evidence. A museum preference might help later personalization,
but a reason for that preference may be sensitive and unnecessary to store.
Explain whose scope owns the fact and how the participant can inspect,
correct and delete it; useful recall alone is not the whole lifecycle.

Use a preference such as museums over nightlife. Obtain consent, store the
minimum fact, inspect its scope, verify retrieval in a new Conversation, correct
it, delete it, and prove the deleted value is no longer applied. Run M01-M03
against the Cultural Agent's separately approved memory scope.

Memory supplies the preference; travel.art MCP tools supply the published
museum, event, or cultural-trip facts. Do not store an unnecessary reason that
could reveal sensitive information.

**Learning summary:** identify the actual preference behavior and verified
lifecycle outcomes separately from the facts returned by travel.art.

**App practice:** pause, resume, and recheck the exact agent and memory scope.
**Alternative:** explain why a stateless design would be safer when memory adds no value.
**Teach-back:** "Which evidence came from memory, and which came from the MCP tools?"

## 14: Release the Cultural Travel Agent

**Concept:** the second specialist must independently pass the same release
discipline before orchestration begins.

**Teach before practice:** reuse candidate-versus-release terminology, then
explain why collaboration needs two independently dependable interfaces.
The workflow will call each specialist's stable endpoint; it should not need
to know how to configure that specialist's MCP tools or copy its instructions.
That separation allows a specialist to evolve behind its own tested release
while preserving the information its consumer needs.

Compare verifying unchanged Weather metadata with rerunning every earlier
Weather lesson. We need evidence that its release and dependencies still
match, not another demonstration of unchanged behavior. Cultural still needs
its own complete release evidence. Examine real outputs for the trip details,
provenance and uncertainty that orchestration will later validate formally;
releasing two agents does not yet execute a workflow.

Weather's release from 07 already uses direct MCP. Check its current
release/version and recorded dependencies read-only, and reuse its valid
unchanged-path evidence. Do not migrate Weather or run another full Weather
suite just for this handoff. If a real configuration, dependency or caller
scope change invalidates evidence, explain it and approve the affected
regressions separately. Keep the two direct domain bindings independent.

Run the complete Cultural Agent regression suite. Verify its exact version,
any configured skill revision, travel.art tool allowlist, source
attribution, and freshness caveats. Promote only a fully passing candidate to
its own Stable Agent Endpoint and run P01-P03.
Apply the same skills-and-memory-deferred release rules as at 07, keeping only
`find_museum_guide` and testing its supported result without injecting a failure.

Apply the same pre-release handoff checklist to actual Cultural results:
owning agent/version, destination/constraints, findings, guide/source
provenance and available verification dates, uncertainty, missing information
and explicit failure status. Preserve its cultural-only evidence boundary.
Formal schemas and workflow validation remain at 15.
Runtime agent/version identity comes from service metadata, not a model guess.

Invoke both stable specialists independently for the same destination. The
Weather Research Agent must not claim cultural retrieval; the Cultural Travel
Agent must not claim weather retrieval. Record both names, versions, endpoints,
identities, tool connections, any configured skill revisions or memory scopes, and release
evidence.
Include each direct server URL/label, effective tool selection and native
approval policy. Require T03-at-14. Verify neither agent is configured with
or can invoke the other domain's tools; do not mistake a shared instruction
for an enforced allowlist.

**Learning summary:** "Now both specialists have independently tested releases
with different evidence responsibilities. We can identify the inputs and
evidence each contributes, but have not yet demonstrated coordination.
Next we will build the workflow that invokes and validates both."

**App practice:** request a two-agent handoff table backed by live metadata.
**Alternative:** inspect sanitized raw responses from both endpoints.
**Teach-back:** "Why must both agents pass independently before workflow code is added?"
