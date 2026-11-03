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
the selected Workshop Coach session, or normal repository Chat when the app
has no agent selector. Do not confuse that entry fallback with optional visual
alternatives later in the lessons.

## Where tests and exploration happen

Each module starts with where you are (plain-language stage and checkpoint),
its goal, a short plan and what will change or stay unchanged. Before a test,
the coach explains why you are running it, what you should observe and what
it cannot prove. At module close, review actual evidence and what you learned,
complete the existing single understanding check, and choose continue or pause.
There is no extra quiz after each action.

The coach names the route before every test or exploration:

| Route | What you do | What the coach does |
|-------|-------------|---------------------|
| **Run from the Copilot app - coach sends** | Stay in this GitHub Copilot app session and approve the stated test. Do not enter the prompt in Foundry as well. | Send the prompt to your actual agent in Foundry, then show its reply, available token counts, and estimated cost here. |
| **Run in the Foundry portal - participant sends** | Follow the coach's verified steps from https://ai.azure.com/ to your exact project and agent, send the agreed prompt yourself, then report the result here. | Give the exact prompt, conversation context, controls and evidence to report, then wait without sending a duplicate call. |
| **Inspect in Foundry - no prompt sent** | Look at the agent's saved settings or the specified test trace. Do not send a message or edit settings. | Explain what to inspect and compare your observation with service-returned evidence. |

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
| Baseline (01, 08) | Coach sends B01 to demonstrate the exchange; participant sends B02 and B03 in separate fresh Conversations and copies each result back. |
| Instructions (02, 09) | Reuse the saved baseline replies as the before side; send each exact input once to the new instruction version on the same route as its baseline. With the allocation above this yields two coach-sent and four participant-sent prompts across baseline/instructions. Balance later suitable cases, not extra before-change calls. |
| Conversations (03, 10) | Participant sends the three-message D01-D02 sequence if the interface supports the required history and identifier evidence. Otherwise use the supported client route and explain the limitation. Rebalance using later suitable tests. |
| MCP and skills (04-05, 11-12) | Coach demonstrates the first tool request and approval boundary. Divide remaining required prompts between routes to bring the running split toward half each; participant returns the answer plus tool evidence. Keep controlled failures on the coach route when they need an isolated test client. |
| Memory and release (06-07, 13-16) | Coach handles identity/scope, deletion, consumer-endpoint, and automated regression checks. A participant may send a required recall or normal-path test only when the interface can preserve its exact scope and target. Playground-only evidence never substitutes for a consumer-endpoint test. |

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

For each participant-run test, the coach provides one copy-ready prompt, the
exact project/agent/version, fresh-or-existing Conversation instructions, the
documented or observed navigation and send control, and the bounded call/tool
approval scope and possible cost. The participant sends it once, waits for the
reply, and copies the actual reply back here, with the Response/Conversation
identifiers and relevant tool details if available. Do not paste secrets or
personal data; a safe excerpt can be labeled as such. If a reply fails, stalls,
or a control differs, report that instead of retrying. The coach waits, reviews
the returned evidence, and uses one demonstrated understanding check for the
checkpoint, not another quiz after every reply.

### Capture evidence before leaving the test

Before **Send**, confirm the exact **Version:**, model, intended Conversation
context and test case. Selecting "latest" is not a version check. Keep the
same selected version for the approved exchange and any matching tool
approval; do not switch versions in the middle.

Return this short public/synthetic record in one message:

```text
Case:
Selected agent / version:
Actual answer (or labeled safe excerpt):
Response ID, if exposed:
Conversation ID, when relevant:
Tool name / arguments / result or error, when relevant:
Usage, if exposed:
```

Missing fields are **unknown**, not an invitation to guess or to repeat the
request. The coach checks required linkage read-only on the same run within
scope. For coach-sent tests, the [runner](runner/README.md) captures those
fields automatically; the participant still practices the required portal
tests and trace inspection. Confirm which answer a trace belongs to before
copying its ID: a denial reply is not the successful forecast.

Both test routes use the agent in Foundry and may incur Foundry charges.
Neither route's token totals measure the Workshop Coach conversation in the
Copilot app. Missing portal-test usage is marked unknown, not zero.
Switching routes does not approve extra calls, changes, or a different agent.
You may agree a bounded batch or allowance for specified low-cost tests on
confirmed resources using [COACH.md's spending agreement](COACH.md#bounded-test-spend-agreements).
Covered tests do not need repeated negligible-price approvals. The coach tracks
conservative cumulative estimates, including uncertain portal usage, and stops
before the remaining allowance would be exceeded or costs cannot be bounded.
This is not a billing hard cap and excludes ongoing resource/telemetry charges
and GitHub Copilot billing. Scope/resource changes or further spend need a new
decision; resource writes and each human MCP tool approval remain separate.

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
and can incur telemetry charges beyond the displayed model-token estimates.

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

## Techniques to introduce along the way

| Checkpoints | Primary approach to practice | Useful alternative and tradeoff |
|-------------|-----------------------------|--------------------------------|
| 00 | Select Workshop Coach in the GitHub Copilot app, send "Start the workshop", then try "Explain without editing." | If the app has no selector, use normal repository Chat with the same prompt and protocol |
| 01, 08 | "Explain this agent definition before editing it." Then explicitly request the small change | Ask for a proposed definition diff first to retain more control |
| 02, 09 | Review the focused instruction diff and compare the same test before and after | Ask for an instruction proposal without applying it |
| 03, 10 | Keep this coaching session; create separate runtime Conversations for each agent test | Use a new app session for an independent task; do not assume it inherits runtime history |
| 04, 11 | For each specialist inspect the upstream connection, Toolbox version/endpoint, separate authentication connection, agent binding, one-tool effective allowlist and runtime identity; 04 includes the first full tool-trace walkthrough | Compare Copilot registration, reusable Foundry connection, Toolbox and authenticated agent binding |
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
