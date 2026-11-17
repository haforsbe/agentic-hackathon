# Learn the Copilot app while building agents

This is a companion to every lesson, not a separate product tour. Practice one
app technique when it becomes useful. The coach should show a primary approach,
briefly compare an alternative, and let the student choose. Do not introduce
several new UI concepts while also debugging an agent.

Use the [core workshop time budget](FACILITATOR.md#five-to-six-hour-core-agenda).
Demonstrate an app technique when first introduced, then use it naturally
while building agent 2 rather than repeating the full tour. Keep the 50/50
test-prompt mix and required hands-on evidence. Ask for deeper exploration only
at a natural checkpoint when time allows or the participant requests it; do
not add two optional prompts after every result.

App features depend on build, policy, and available tools. Inspect what is
actually exposed. Never invent buttons, keyboard shortcuts, slash commands,
custom-agent selectors, or Canvas actions. The example prompts below work in
the selected Workshop Coach session, or normal repository Chat when neither
`/agent` nor an agent picker is available. Do not confuse that entry fallback with optional visual
alternatives later in the lessons.

## Select custom agents

A **custom agent profile** gives GitHub Copilot a reusable specialist role:
instructions describing its purpose, how it should work, and optionally which
tools it can use. It is not a new AI model or a deployed cloud service.

| Choice | What it controls |
|--------|------------------|
| **Custom agent**, selected with `/agent` or the documented agent picker in the prompt box | The specialist role and instructions for the GitHub Copilot app session, such as **Workshop Coach** |
| **Model**, selected with the model picker | The AI model powering the session; a profile can also specify a model, but Workshop Coach inherits your selection |
| **Interactive / Plan / Autopilot** | How the session collaborates with you or proceeds with work |
| **Microsoft Foundry agent and version** | The separately created cloud agent being configured or tested; selecting a GitHub Copilot profile does not select or deploy it |

### Select the existing Workshop Coach

In the GitHub Copilot app, open a session for this workshop repository. Type
**`/agent`** in its message box and choose **Workshop Coach**. Alternatively,
use the agent picker dropdown inside the prompt box if your app displays it.
Confirm the selected profile using the interface your build exposes; then send
**"Start the workshop"** for a fresh start, or **"Resume the workshop"** when
you intend to continue saved progress. Selecting a profile alone is not a
start/resume request and does not authorize Microsoft Foundry operations.

The profile is supplied in `.github/agents/workshop-coach.agent.md`.
Its presence is not proof that your app has discovered it. If the dropdown
is absent, try `/agent`; if neither selection route is available, use normal
repository Chat with the same coaching protocol. If selection is available
but Workshop Coach is missing, involve the facilitator to check the checkout
and discovery. Do not choose an unrelated profile or clear progress.

Participants select an existing profile; they do not need to create or edit
one. Selecting Workshop Coach does not change repository files or Microsoft
Foundry resources, deploy an agent, or reset saved workshop progress. Using
the selected profile still uses GitHub Copilot under your plan. Check selection
in the app's interface; a coach-like reply alone does not prove the profile
was selected.

These routes are documented in
[Using custom agents in the GitHub Copilot app](https://docs.github.com/en/copilot/how-tos/github-copilot-app/customize-github-copilot-app#using-custom-agents),
and the [`/agent` reference](https://docs.github.com/en/copilot/reference/github-copilot-app-reference/slash-commands).
Documented support is not participant-build verification; if controls differ,
describe what is visible instead of guessing labels.

## Where tests and exploration happen

Each module starts with where you are (plain-language stage and checkpoint),
its goal, a short plan and what will change or stay unchanged. Before a test,
the coach explains why you are running it, what you should observe and what
it cannot prove. At module close, review actual evidence and what you learned,
complete the existing single understanding check, and choose continue or pause.
There is no extra quiz after each action.

Use [the coach's learner-instruction rule](COACH.md#explain-what-and-why-before-every-step):
give the actual action or copy-ready prompt, its purpose, the starting
location/context and the expected result. Internal acceptance IDs belong in
coach records, never in participant messages, question dialogs or choices.
Do not ask learners to look up a case code to discover what they should do.
The lesson files provide concrete starting prompts for both specialists.

The coach names the route before every test or exploration:

| Route | What you do | What the coach does |
|-------|-------------|---------------------|
| **Run from the GitHub Copilot app - coach sends** | Stay in this GitHub Copilot app session and approve the stated test. Do not enter the prompt in Microsoft Foundry as well. | Send the prompt to your actual agent in Microsoft Foundry and show its reply here; capture usage locally for the checkpoint and cumulative workshop summary, not a per-call report. |
| **Run in the Microsoft Foundry portal - participant sends** | Follow the coach's verified steps from https://ai.azure.com/ to your exact project and agent, send the agreed prompt yourself, then report the result here. | Give the exact prompt, conversation context, controls and evidence to report, then wait without sending a duplicate call. |
| **Inspect in Microsoft Foundry - no prompt sent** | Look at the agent's saved settings or the specified test trace. Do not send a message or edit settings. | Explain what to inspect and accept your clear confirmation for routine hands-on completion. Corroborate only when a specific required assertion needs service evidence. |
| **Run in Microsoft Teams or Microsoft 365 Copilot - participant sends** | At 07/16 open your exact published Weather/workflow app in the chosen surface, send the approved prompt once, and return the actual reply. | Verify publication/target and channel identity, provide documented navigation from the returned launch link, then inspect the same run's Microsoft Foundry evidence without resending. |
| **Run in Microsoft Copilot Studio - participant sends** | At 16, if this integration route is chosen and rehearsed, test the primary agent connected to the released workflow using the same approved Playground behavior cases. | Verify the actual connected workflow/version, native approval controls and same-run specialist evidence; distinguish Studio integration testing from later published-channel CH02 evidence. |

Aim for **50/50 coach-sent and participant-sent test prompts** across each
specialist's lessons, using a **coach demonstrates, participant practices**
rhythm. Count prompts sent to the agent, not navigation, inspections, tool
approval continuations, or coaching messages. The Copilot app remains the home for explanations,
approvals, evidence review, and progress; the Foundry agent Playground is where
participants practice sending messages themselves. A Playground is the browser
test interface for the selected agent, not a separate agent or the model-only
chat playground.

| Lesson | Suggested mix of required tests |
|--------|---------------------------------|
| Baseline (01, 08) | Coach demonstrates a general-knowledge question; participant sends the lesson's missing-context question in a fresh Conversation and reports what happened. Supply the actual prompt and explain that the agent should ask for the missing location. A clear confirmation is enough for routine observation; copy an excerpt only when helpful or needed for a specific assertion. |
| Instructions (02, 09) | Reuse the saved baseline replies as the before side; send each exact input once to the new instruction version on the same route as its baseline. With the allocation above this yields two coach-sent and two participant-sent prompts across baseline/instructions. Balance later suitable cases, not extra before-change calls. |
| Conversations (03, 10) | Participant supplies a destination, sends a dependent follow-up in that same Conversation, then repeats the follow-up in a fresh Conversation. Give each exact prompt when needed and explain the expected context difference. Use this route if the interface supports the required history and identifier evidence; otherwise demonstrate through the supported client. |
| MCP and skills (04-05, 11-12) | Participant sends the first useful forecast or museum-guide prompt in the agent Playground. Explain the permission choices when they appear and let the participant select **Auto approve** for the displayed permitted-tool scope; continue to the answer and trace, not a separate denial drill. Divide remaining required prompts between routes to bring the running split toward half each. Keep isolated failure checks on the coach route. |
| Memory and release (06-07, 13-16) | Coach handles identity/scope, deletion, consumer-endpoint, and automated regression checks. A participant may send a required recall or normal-path test only when the interface can preserve its exact scope and target. Playground-only evidence never substitutes for a consumer-endpoint test. |
| Channel publication (07, 16) | Participant uses Weather in Microsoft Teams and/or Microsoft 365 Copilot before 08, then uses the released workflow there at 16. CH01/CH02 require channel-originated requests and same-run runtime evidence; a publish dialog is not a pass. |

Keep the channel prompts labeled and counted as participant-sent prompts on
their actual route. They are required distribution exercises, not a reason to
rebalance or duplicate the preceding specialist tests. See
[channel publication](PUBLISHING.md#required-channel-publication-at-07-and-16)
for documented controls, tenant prerequisites, separate approvals and blockers.

Plan the split before each specialist's lessons, record the route of each
actual prompt, and use the running counts to allocate remaining suitable tests.
Agree on one route before each test; these are defaults, not permission to send
anything automatically. Aim for half each, allowing a one-prompt difference
when the total is odd. Adapt to participant preference, accessibility, and
verified interface capabilities; explain and record any larger deviation rather
than weakening a test or approval boundary. Never add calls, repeat completed
tests, or split a matched pair or Conversation sequence just to balance counts.
Portal inspection and guided trace
exercises remain required even when the coach sent the prompt.

At occasional natural pauses, the coach checks whether you prefer the current
execution balance, more hands-on steps or more coach-executed steps. It also
occasionally offers to keep or change your explanation level for Microsoft
Foundry or the GitHub Copilot app: Beginner, Intermediate or Expert.
These are separate, optional questions, not a quiz or a survey after every
checkpoint; you can defer them or describe a preference in your own words.
An explicit execution preference adjusts remaining suitable actions rather
than enforcing the default 50/50 split. Required participant practice, approvals,
test evidence and checkpoint order remain unchanged. See
[experience check-ins](COACH.md#occasional-experience-check-ins).

For each participant-run test, the coach provides one copy-ready prompt, the
exact project/agent/version, fresh-or-existing Conversation instructions, the
documented or observed navigation and send control, and the bounded call/tool
approval scope and possible cost. The participant sends it once, waits for the
reply, and reports what happened. Follow
[participant trust](COACH.md#supportive-coaching-and-participant-trust):
clear confirmation of a routine manual step or visible response format is
enough to continue; no default screenshot, full pasted reply or identifier hunt.
Ask for an excerpt or specific Response/Conversation/tool details only when the
participant wants review, reports a problem, or a required assertion needs
them. Do not paste secrets or personal data. If a reply fails, stalls, or a
control differs, report that instead of retrying. The coach waits and uses one
demonstrated understanding check for the checkpoint, not another quiz after
every reply.

### Capture evidence before leaving the test

Before **Send**, confirm the exact **Version:**, model, intended Conversation
context and test case. Selecting "latest" is not a version check. Keep the
same selected version for the approved exchange and any matching tool
approval; do not switch versions in the middle.

For routine hands-on work, a confirmation such as "I saved the instructions
and can see all three headings" is sufficient. The coach accepts it as
participant-confirmed and moves on without automatically requesting a second
inspection. When a specific runtime assertion or requested review needs more
detail, return only the relevant fields from this public/synthetic record:

```text
Activity or question:
Selected agent / version:
Actual answer (or labeled safe excerpt):
Response ID, if exposed:
Conversation ID, when relevant:
Tool name / arguments / result or error, when relevant:
Usage, if exposed:
```

This is not a form to complete after every action. Missing fields are
**unknown**, not an invitation to guess or to repeat the request.
The coach checks required linkage read-only on the same run within
scope. For coach-sent tests, the [runner](runner/README.md) captures those
fields automatically; the participant still practices the required portal
tests and trace inspection. Confirm which answer a trace belongs to before
copying its ID: a denial reply is not the successful forecast.

Both test routes use the agent in Foundry and may incur Foundry charges.
Neither route's token totals measure the Workshop Coach conversation in the
Copilot app. Missing portal-test usage is marked unknown, not zero.
Switching routes does not approve extra calls, changes, or a different agent.
You may approve a bounded batch of specified tests on confirmed resources
using [COACH.md's scoped test approvals](COACH.md#scoped-test-approvals).
Covered tests do not need repeated per-call cost approvals. The coach retains
available Microsoft Foundry tokens, marking missing portal usage unknown,
without price lookups or mandatory money calculations. An end-of-workshop
estimate is optional, not a bill or completion gate. Scope/resource changes,
extra cases or expired terms need a new decision; explicit cost restrictions,
resource-write approvals and each human MCP tool approval remain separate.

For portal navigation, the coach gives a concrete, documented route first:
starting URL, your exact project and resource, control labels, and the expected
result. You do not need to list sidebar labels or provide a screenshot before
ordinary guidance. If the documented controls differ from your screen, stop
and describe the difference; a screenshot with personal details hidden is
optional. Missing traces do not authorize another test or telemetry setup.

When first connecting to your project, and again before a portal trace exercise,
the coach checks that your project is connected
to **Application Insights**, Azure's service for execution telemetry, and that
you can read the records. Saved Conversation history does not establish this
connection. The first check reads existing settings and access; it does not
enable tracing or send a model prompt. If it is missing, the coach explains the blocker before asking you
to search for a trace. Connection or resource changes need separate approval
and can incur telemetry charges not measured by model-token usage.

### Hosted workflow portal test at 16

This is the baseline for
[destination test parity](PUBLISHING.md#workflow-destination-test-parity):
the same applicable cases must also pass through the chosen Microsoft Teams
or Microsoft Copilot Studio route. Do not have the participant send a
destination prompt while the coach sends its duplicate in the Playground.

This route was observed in the English Microsoft Foundry portal on
2026-11-10 for an existing hosted workflow. It is not a guarantee of controls
in every tenant or a participant's current build.

From https://ai.azure.com/, open the participant's confirmed project and its
hosted workflow agent. Select **Playground**, then **Chat**. Read the actual
**Version:** selector and heading; select the approved candidate if necessary.
A `version` URL parameter or cached page alone is not confirmation.
Confirm the signed-in profile matches the approved participant identity.
If controls differ, stop and describe the screen rather than guessing.

For the approved W04 trip:

1. Select **New chat** for a fresh Conversation, enter the agreed supported
   trip prompt and press **Send** once. Do not also invoke it from the
   GitHub Copilot app.
2. Read the Weather tool name and arguments. The participant chooses
   **Approve** or **Deny** on that exact card once. A general test approval
   is not that tool decision.
3. If Weather is approved, wait for the separate Cultural card. Review its
   own tool name/arguments and make its own decision once; do not click the
   old Weather card again. For the success case, both cards must resolve and
   the combined answer must appear.
4. Open **Traces** associated with that answer and capture the Conversation
   and available run/response IDs. The coach corroborates both native calls
   and approval bindings read-only; the participant does not need to discover
   internal IDs or paste credentials.

**If it fails:** do not press **Send** again, repeatedly approve a retained
card, reload the page or switch versions while collecting the failed run.
Record the visible error, exact displayed version, time and available IDs.
Within approved diagnostic scope, capture the failing request's origin/path,
HTTP status, safe error code and correlation identifier when available.
Never paste authorization headers, cookies, tokens or an unsanitized network
archive. Ordinary participants need not configure Playwright or developer
tools; facilitator support owns deeper transport diagnosis.

Do not infer the cause from a generic HTTP 400, an outer HTTP 200, or the
last card still visible. A model/tool run may already have advanced.
No native-ID/API approval fallback or relaxed stale-reference check is allowed.
Any fresh diagnostic trip requires explicit approval for that additional
case and possible charges; it does not resume or erase the failed run. Apply the coach's
five-minute/two-attempt timebox and keep unresolved required gates blocked.

## Foundry navigation rehearsed before the workshop

**Observed on 2026-10-26:** the English **New Foundry** experience at
https://ai.azure.com/, using Edge and an existing Prompt Agent. These controls
were inspected read-only in a confirmed project; no message was sent, agent
saved/published, or resource created. This is a dated navigation reference,
not a guarantee that every tenant, role, screen size, or portal revision matches.
No classic-portal route was verified in this rehearsal.

Browser automation such as Playwright is a **facilitator preparation tool,
not part of live workshop coaching**. During the workshop, participants follow
these instructions themselves and copy results into the GitHub Copilot app.
Do not launch an automated browser, request browser tooling installation, or
take over their screen to recover a navigation mismatch. Ask one specific
question about the differing control, then give revised documented guidance or
involve the facilitator. Screenshots remain optional.

Before giving a live instruction, substitute the participant's confirmed
project, exact agent, and intended version for the generic descriptions below.
Do not send participants to the rehearsal author's project.

| Task | Observed route and expected result |
|------|------------------------------------|
| Confirm browser identity | At https://ai.azure.com/, use the website's **Sign in**, not Edge's profile **Add account**. **My profile settings** opens **Profile**, showing the signed-in account. This is separate from the coach's CLI identity. |
| Confirm project | The header's project-name button shows the current project. On **Home**, **Get started** includes the **Project endpoint** field and **Copy project endpoint**. Do not copy an API key or substitute the Azure OpenAI endpoint. |
| Find the agent | Select **Build** in the top navigation, then **Agents** under **Create** in the left navigation. Use **Search agents** if needed, then select the exact agent-name link. The list also contains **Routines** and **Workflows Preview**; neither is the Prompt Agent Playground. |
| Confirm version and configuration | The agent page has a **Version:** selector, and **Playground**, **Details**, **Traces**, and other tabs. In **Playground**, verify the version and **Model:** before testing. Inspect **Instructions** and **Tools** without editing. The version menu also contains deletion controls: do not use them for inspection. |
| Send an approved test | On the agent's **Playground** tab, use **Chat**, paste only the agreed test into **Message the agent...**, then select **Send** once. Do not paste it into **Write your prompt here to give your agent instructions.** That box changes the agent's instructions. **Save**, **Publish**, and **Improve instructions** are not test-send controls. |
| Start fresh context | **New chat** is visible above the Chat area. It was not clicked during rehearsal, so a new Conversation identifier and isolation must still be demonstrated in the approved D01-D02 tests, not inferred from the label. |
| Find a saved execution | From **Build → Agents → the exact agent**, select **Traces**, then **Trace view**. Use **Search by trace ID, conversation ID, or response ID** with the saved identifier. Check **Version**, **Status**, and **Date range**; the observed default was **Last Day**. The table's identifier column is **Trace ID**, not Response ID. |
| Inspect a tool call | Select the matching **Trace ID** to open its detail dialog. In **Trajectories**, select the **Execute Tool execute_tool ...** entry in the trace tree. **Input + Output** shows arguments and returned data; duration is shown above. **Metadata** shows `start_time`, `end_time`, and `status.status_code`. A span is one recorded operation within the trace. |
| Find the response identifier | In the inspected forecast tool span's **Metadata**, `attributes` contains `gen_ai.response.id` (`resp_...`). This identifies the response, not the trace or conversation. Do not assume every span exposes the same fields; use another relevant span or service evidence if absent. |
| Inspect a saved Conversation | Close the trace dialog, then select **Conversation view** within **Traces**. Its table shows **Conversation ID** (`conv_...`) and its search field is **Search by conversation ID**. This view aggregates conversations; it is not the complete list of response-only executions. Use **Trace view** for a response search. |

The observed forecast entry was labeled
`Execute Tool execute_tool mcp_weather_intelligence.weather_forecast`.
For another agent, use its actual MCP server/tool name rather than copying this
label. The tool result's source, forecast time, and service `served_at` time
have different meanings; a successful tool status does not prove every sentence
in the final answer is grounded.

The send button, version menu, and New chat control were located, not exercised.
Tool-approval dialogs, post-send copy controls, memory operations, and publishing
flows were not rehearsed. Do not invent their exact labels or treat this
read-only walkthrough as test evidence for those behaviors. Missing telemetry
or a different date filter does not authorize another model call or setup change.

### Before adding a direct MCP tool

**Additional observed controls, 2026-11-05:** these English portal observations
come from an approved author rehearsal, not the participant's current session
or a new direct-MCP runtime rehearsal. Use them only when the actual
screen matches; inspection does not authorize edits, tool calls or a test.

| Task | Observed route and limit |
|------|--------------------------|
| Inspect a saved agent binding | On the exact agent's **Playground**, confirm **Version:**, then **Setup -> Tools**. **YAML** shows the saved definition. Verify the direct server URL, allowlist and approval settings independently; a card alone proves no runtime access. |
| Inspect model parameters | On that same **Setup** screen, **Parameters** beside **Model:** exposes **Max output tokens**. In the rehearsal, an entered value did not persist after reopening and the service response reported no limit. A briefly displayed number is not an enforced test bound; stop before sending until the intended route's limit is verified. |
| Inspect display settings | **Configure** in **Chat** opened display-name, description, starter-prompt and voice settings, not the model-token limit. Do not direct learners there to configure output limits. |
| Inspect this reply's trace | Under the actual reply, **Traces** opens a drawer with **Trajectories**, **User view** and **Graph view**. Select the matching operation, then **Metadata** or **Input + Output** where present. `tools/list` is discovery, not execution; look for the actual server/tool's execution span and correlate the saved response identifier. Do not resend to recover an identifier. |

These observations do not verify approval controls, effective output limits,
memory, publishing or other tenants. Follow
[Direct MCP connections](MCP-CONNECTIONS.md) for the approved configuration
and actual runtime checks; portal visibility is not tool-execution evidence.

At 04, before using an agent's **Add** control, the coach explains the route:
**agent -> public Weather MCP server -> `weather_forecast`**. The first
candidate permits only this one tool. No Toolbox or upstream credential
connection is part of the core path.

The saved `server_url` must be `https://weather.datakoot.com/mcp`, with only
`weather_forecast` in the allowlist and `require_approval: "always"`. Do not
add `project_connection_id`, keys or authorization headers for this anonymous
server. The coach supplies these exact values, explains what is sent outside
Microsoft Foundry and obtains approval before one candidate change.
Do not assume the picker exposes every setting. If it cannot express the
approved definition, use the supported coach-executed skill/API route after
explaining it; do not save trial versions or invent controls.
Then, on the established agent page, refresh if needed, select the actual
returned **Version:** and inspect **Tools** without editing. If connection
details are not exposed there, review the coach's service-returned read-back;
do not guess a details control. Sending a test or publishing requires its own
approval. At 11, use a short reminder and inspect Cultural's direct
`https://mcp.travel.art/` binding with only `find_museum_guide`, leaving
Weather unchanged. First use of either route still needs the starting
portal URL, confirmed project, exact agent/version and documented controls.

### First tool use in the Playground

At 04 and 11, teach permissions when the first useful tool-backed question
reaches them, not through a separate approval/denial exercise:

1. On the exact agent's **Playground -> Chat**, confirm **Version:** and the
   approved fresh-or-existing Conversation. Supply the copy-ready forecast or
   museum-guide prompt from [MCP-SERVICES.md](MCP-SERVICES.md), the **Message
   the agent...** field and **Send** control, and the agreed execution limits
   and possible Microsoft Foundry charges. The participant sends once.
2. When the first tool-permission prompt appears, explain briefly:
   "**Approve** permits this proposed tool call; **Deny** blocks it.
   **Auto approve** lets the Playground approve subsequent calls within the
   permission scope shown here without asking each time."
3. Have the participant review the named service, tool and displayed scope,
   then select **Auto approve** for this specialist's permitted read-only MCP
   tools. Keep the effective one-tool allowlist at 04/11; review the scope
   again when expanding it at 05/12. If the scope is unclear or broader than
   intended, stop for that decision rather than accepting a blanket permission.
4. Continue to the returned forecast or museum guidance and inspect that same
   execution's tool arguments, result, sources and available timestamps. At
   04, give the full trace walkthrough; at 11, reuse it with a short reminder.
   Capture the participant's choice and actual execution evidence together.
   Do not add a deliberate denial or duplicate call to test the permission UI.

**Participant-reported portal behavior, 2026-11-17:** the user reports
**Auto approve** and denial choices at first tool use in a Playground chat.
This is not an independently observed runtime rehearsal or proof of the
setting's persistence. Use the actual displayed control and scope. If it is
absent or different, ask for that specific observation and agree a supported
explicit-approval route; do not invent clicks or silently broaden permission.

The Playground choice is not a GitHub Copilot app permission and does not
establish automatic approval through the SDK, Stable Agent Endpoint, hosted
workflow or published channel. Retain the documented
`require_approval: "always"` definitions and the runner's pending-approval
stops; do not infer `require_approval: "never"` or auto-submit runner
continuations from a portal choice. Inspect any actual saved configuration
change and obtain its scoped approval before using it elsewhere. Runtime
denial handling remains intact if a participant declines a real request;
the specialist lesson simply has no separate denial drill.

## Techniques to introduce along the way

| Checkpoints | Primary approach to practice | Useful alternative and tradeoff |
|-------------|-----------------------------|--------------------------------|
| 00 | Type `/agent` in the repository session, select Workshop Coach, send "Start the workshop", then try "Explain without editing." | Use the documented agent picker if visible; normal repository Chat is the fallback only when neither selection route is available |
| 01, 08 | "Explain this agent definition before editing it." Then explicitly request the small change | Ask for a proposed definition diff first to retain more control |
| 02, 09 | Review the focused instruction diff and compare the same test before and after | Ask for an instruction proposal without applying it |
| 03, 10 | Keep this coaching session; create separate runtime Conversations for each agent test | Use a new app session for an independent task; do not assume it inherits runtime history |
| 04, 11 | For each specialist inspect the direct server URL, exact agent version, one-tool effective allowlist and native approval policy; 04 includes the first full tool-trace walkthrough | Compare the GitHub Copilot app's MCP registration with the separate Microsoft Foundry agent binding |
| 05, 12 | Review each skill diff, tool allowlist, exact version, and delivery strategy | Use a file/editor panel if available; reading an artifact is not deployment evidence |
| 06, 13 | "Pause and save my progress." Then "Resume and recheck my target." | A new worktree needs an approved progress import and does not share agent memory |
| 07, 14, 16 | "Show the endpoint, selected version, and actual test results; don't infer success." | Use supported hosted controls when available; return to Chat for evidence review |
| 15 | "Show both agent versions, result contracts, workflow spans, and validation decisions." | Read sanitized trace/log evidence when no visual trace view is available |
| 17 | Write a two-specialist brief with scope, non-goals, tests, and cost boundaries | Choose a preset capstone or propose an equivalent custom scenario |
| 18 | "Change only this specialist capability and run these tests." Review the diff | Use an isolated branch/worktree for one risky experiment |
| 19 | Ask for a handoff with verified endpoints, versions, limitations, traces, and owned resources | Compare the handoff with a live demonstration |

## Teach control, not just prompting

**Request types:** explanation is read-only; a plan is a proposal; implementation
changes artifacts; execution can affect live resources. Teach students to state
which they want. "Show another way" is not approval to execute both alternatives.

**Changes:** review the proposed scope and resulting diff. Committing saves
source history, but does not deploy it. Pushing shares source, not the student's
local `.workshop/` evidence. Never silently commit or publish student work.

**Tool permissions:** the app's permission prompt controls what Copilot may do.
It is distinct from the deployed agent's tool approval, Azure RBAC, memory
scope, and the consumer's access. Approving a shell command does not authorize
every future cloud mutation.

**Sessions:** a Copilot app session, a worktree, a Foundry conversation, and a
memory store are four different things. A new runtime conversation can be
tested from the same coaching session. A new app session does not prove memory
is persistent in Foundry. Reusing a worktree also does not automatically share
app conversation history.

**Context:** point the coach at the relevant file or error rather than pasting
an entire environment dump. Ask it to separate observed evidence from guesses.
Do not paste credentials, secrets, or personal data.

**Alternatives:** use a direct SDK/CLI operation when it gives a needed,
inspectable result and no suitable app integration exists. Use the installed
Foundry skill when available. Prefer the smallest supported path; comparing
approaches does not mean installing extra extensions or provisioning duplicates.

## Optional visual surfaces

When an appropriate surface is actually available, the coach can use an editor
for an artifact, a terminal for a process the student should watch, or the
browser for a relevant preview. The core path does not require these surfaces.

Foundry Canvas is for supported hosted-agent operations under the app's routing
rules. Prompt-agent creation, explanation, troubleshooting, and mixed tasks
remain in Chat. Never route a teaching question into a deployment. A Canvas
handoff is not success evidence; return to the learning gate after the action.

## App learning evidence

At each checkpoint, record a brief `app_practice` object in the local attempt:
the technique used, the alternative discussed, and the student's explanation of
when to use it. A Chat equivalent is sufficient if a UI feature is unavailable.
Do not record full app transcripts or screenshots containing sensitive details.
