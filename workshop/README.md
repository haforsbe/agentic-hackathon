# Workshop map

**First time here?** Follow [Start here](START.md), type **`/agent`** in the
GitHub Copilot app's repository session, select **Workshop Coach**, then send
**"Start the workshop."** The documented agent picker in the prompt box is
another selection route if visible. Use normal repository Chat only when
neither route is available.

The coach runs in the **GitHub Copilot app**; the student's agents run in
**Microsoft Foundry**. Learn both one small change at a time. Changing the
coach's instructions, memory, skills, or MCP server/tool connections does not
configure a deployed agent.

**Plan for 5-6 hours** for the core workshop, ending at checkpoint 16 with two
working specialists connected through the hosted workflow, with Weather and
the workflow published and used from Microsoft Teams and/or Microsoft 365 Copilot.
At each publication milestone choose at least one surface. The first agent
teaches the method; the second applies it with shorter reminders, not repeated
lectures. Required tests and approvals stay in place. See the
[5-hour-50-minute planning agenda](FACILITATOR.md#five-to-six-hour-core-agenda).
The capstone at 17-19 is a separate optional extension.

For the workflow, follow one clear delivery sequence: **create it**, **deploy
and test it in Microsoft Foundry Playground**, then **connect/publish and test
the same workflow in Microsoft Teams or Microsoft Copilot Studio**. The same
applicable approval, denial, sourced-output and failure tests must pass in the
chosen destination; see [test parity](PUBLISHING.md#workflow-destination-test-parity).
Microsoft Copilot Studio's test pane is not a published channel. The existing
CH02 requirement still needs actual Microsoft Teams or Microsoft 365 Copilot
use, either directly or after the Microsoft Copilot Studio integration.

Each module opens with its checkpoint, plain-language goal and short plan.
Before tests, the coach explains their purpose and expected evidence; at the
close, actual results lead to a short learning summary, the existing single
understanding check and the next step. For specified low-cost tests, you may
approve a [bounded test-spend agreement](COACH.md#bounded-test-spend-agreements)
instead of repeated negligible-price approvals. Resource changes and human
tool approvals remain separate; this estimate is not a billing hard cap.

To keep that time for learning, the coach uses the
[checkpoint execution matrix](TESTS.md#checkpoint-execution-matrix) and
[shared execution helper](runner/README.md), captures evidence during tests,
and reuses already learned navigation. These automate plumbing, not the
participant's approvals, hands-on tests or understanding. Facilitators can
offer the [optional advance readiness check](SETUP.md#optional-advance-readiness-same-live-approval-boundaries).

## Learning sequence

| Concept/reference | Weather Research Agent | Cultural Travel Agent | Hosted workflow |
|-------------------|------------------------|-----------------------|-----------------|
| Minimal prompt agent | 01 | 08 | 15 scaffolds the orchestrator |
| Instruction refinement | 02 | 09 | Reused for tested updates |
| Managed conversations | 03 | 10 | Workflow passes explicit request/correlation state |
| First MCP tool | 04: `weather_forecast` | 11: `find_museum_guide` | Workflow invokes agents, not their tools |
| Skills and multiple tools | 05: weather research procedure | 12: cultural research procedure | 15 validates formal result contracts |
| Persistent memory | 06 | 13 | Workflow does not merge memory stores |
| Independent release | 07 | 14 | 16 releases the hosted workflow |
| Publish and use in Microsoft Teams and/or Microsoft 365 Copilot | 07, after release and before 08 | No additional channel publication required | 16, after final release/update checks |
| Agent collaboration | Specialists stay independently callable | Specialists stay independently callable | 15-16 coordinate both releases |

The learning path keeps both prompt agents independently publishable.
It also teaches [Foundry tools and Toolboxes](TOOLS-AND-TOOLBOXES.md):
register Weather's reusable tool connection and forecast-only Toolbox at 04,
expand that Toolbox at 05, verify its existing binding at 07, and deepen independent Toolbox
practice with Cultural at 11. At 14 verify both releases, without migrating
and re-releasing Weather.
Tools supply operations, Toolboxes manage collections, and skills guide use.
Each specialist retains only its own tools. This replaces connection plumbing
within the existing checkpoints; changed bindings still require regressions.
The current curriculum is `two-specialists-workflow-v9`; earlier progress
requires an agreed migration, not automatic new passes.
Version 9 preserves the sequence and adds required Weather CH01 and workflow
CH02 channel gates inside 07 and 16; the second agent and workflow build are
unchanged. Existing endpoint evidence is not channel evidence. See
[publishing prerequisites and steps](PUBLISHING.md#required-channel-publication-at-07-and-16).
The Weather Research Agent and
Cultural Travel Agent own different tools and evidence domains. Formal
machine-readable contracts appear only when executable orchestration needs to
validate both results.

The [selected MCP services and shared story](MCP-SERVICES.md) are fixed workshop
inputs: Weather uses `https://weather.datakoot.com/mcp`; Cultural Travel uses
`https://mcp.travel.art/`. Both are public free-to-use services with no API key
or participant hosting requirement. The coach provides the connection details,
discovers actual schemas, and guides the same approval, configuration, test,
trace, and teach-back process for each specialist. Foundry charges still apply.

After Weather checkpoint 07 passes, including CH01, participants may choose the separate
[optional Weather-agent GitHub delivery lab](weather-delivery/README.md) before
checkpoint 08. It does not add a numbered checkpoint or extend the 5-6-hour
core estimate. Skip or completion both return to 08. The lab's one-project
setup is explicitly an educational compromise, not production isolation;
capture opens a reviewed PR, offline checks validate its package, and a
protected GitHub Environment gates deployment to the separate Prod agent.
The workflow is not live-rehearsed or configured with Azure OIDC/project
permissions; a successful deploy does not establish Toolbox runtime access or
per-call approval.

## Terms the coach introduces when needed

The coach does not assume prior agent or cloud experience and does not present
this as a vocabulary test. It introduces each term immediately before use:

| Term | Plain-language meaning |
|------|------------------------|
| Microsoft Foundry Project | The participant's dedicated cloud workspace, which they may prepare before the workshop or create during checkpoint 00, containing models, agents, connections, and related resources |
| Microsoft Foundry Project Endpoint | The network address used to access that project through supported clients |
| Microsoft Foundry Model Deployment | A named configuration that makes the participant's selected model callable; it uses quota and may incur cost |
| Agent | A model combined with instructions and optional capabilities |
| MCP server and tool | The server publishes callable tools; a tool is one specific operation, such as `weather_forecast` |
| MCP Server Endpoint | The network address where a client reaches an MCP server |
| Stable Agent Endpoint | The supported address used to invoke a released agent version |
| Conversation | Managed history for a related sequence of messages |
| Memory | Stored information that can be available beyond one conversation |
| Skill | A reviewed reusable procedure that can guide tool use but does not grant tool access |
| Version and release | A version is a candidate configuration; release selects a fully tested version for consumers |
| Channel publication | Making a released agent available in Microsoft Teams or Microsoft 365 Copilot; distinct from coaching in the GitHub Copilot app |
| Workflow | Executable logic that coordinates steps or agents |
| Trace | A timeline showing calls, tools, durations, and failures |
| Contract | A versioned machine-readable definition of data the workflow can validate |

## Checkpoints

| ID | Lesson | Required test evidence | App practice |
|----|--------|------------------------|--------------|
| 00 | [Setup](SETUP.md) | Participant's dedicated project (existing or created during setup), direct project identity check, operation-specific permission verification, deployment inventory, participant choice to reuse or explicitly approve a Model Deployment, ownership, capability inventory | Repo context, cost boundary, and approvals |
| 01 | [Weather baseline](01-prompt-agents.md#01-create-the-weather-research-agent) | B01-B03 | Explain vs implement |
| 02 | [Weather instructions](01-prompt-agents.md#02-refine-weather-instructions) | I01 | Review a focused instruction diff |
| 03 | [Weather conversations](01-prompt-agents.md#03-test-weather-managed-conversations) | D01-D02 | App session vs runtime Conversation |
| 04 | [First Weather MCP tool](01-prompt-agents.md#04-connect-the-first-weather-mcp-tool) | T01 reusable tool, T03 forecast-only Toolbox, C01, C03 and guided trace inspection | Inspect upstream connection, Toolbox authentication and agent binding |
| 05 | [Weather skill and multiple tools](01-prompt-agents.md#05-guide-multiple-weather-tools-with-a-skill) | T03 four-tool Toolbox expansion, S01 | Review skill delivery, pinned binding and tool routing |
| 06 | [Weather memory](01-prompt-agents.md#06-add-and-test-weather-memory) | M01-M03 | Save/resume vs agent memory |
| 07 | [Release and publish Weather Research Agent](01-prompt-agents.md#07-release-the-weather-research-agent) | T03 existing Toolbox verification, final-path regressions, P01-P03, then CH01 channel publication/use before 08 | Distinguish release from publishing; review the participant's channel test evidence |
| 08 | [Cultural baseline](01-prompt-agents.md#08-create-the-cultural-travel-agent) | B01-B03 | Compare independent agent definitions |
| 09 | [Cultural instructions](01-prompt-agents.md#09-refine-cultural-instructions) | I01 | Review a focused instruction diff |
| 10 | [Cultural conversations](01-prompt-agents.md#10-test-cultural-managed-conversations) | D01-D02 | Verify isolated runtime state |
| 11 | [First Cultural Travel MCP tool](01-prompt-agents.md#11-connect-the-first-cultural-travel-mcp-tool) | T01/T02 reusable tool and Cultural Toolbox, C02, C03 | Inspect Toolbox version, agent binding, effective allowlist and provenance |
| 12 | [Cultural skill and multiple tools](01-prompt-agents.md#12-guide-multiple-cultural-tools-with-a-skill) | S02 | Review skill delivery and tool routing |
| 13 | [Cultural memory](01-prompt-agents.md#13-add-and-test-cultural-memory) | M01-M03 | Verify separate memory scope |
| 14 | [Release Cultural Travel Agent](01-prompt-agents.md#14-release-the-cultural-travel-agent) | Cultural final-path regressions/P01-P03, unchanged Weather release/dependency verification, T03 isolation and two-agent comparison | Review two independent Toolbox-backed releases without a planned Weather migration |
| 15 | [Build Trip Planning Workflow](02-hosted-agents.md#15-build-and-test-the-trip-planning-workflow) | Reviewed portal-compatible scaffold, G01-G03 and W01-W03 locally | Review contracts, request-owned state, approval bindings and traces |
| 16 | [Deploy, release and publish workflow](02-hosted-agents.md#16-hosted-release) | W01-W03 remotely, actual portal W04 success/denial, P01-P04, then CH02 on the final version | Review sequential tool cards and sourced output; send a channel request and inspect both specialist calls |
| 17 | [Choose a capstone](CAPSTONE.md#17-choose-and-scope) | K01 | Turn an idea into a bounded two-specialist plan |
| 18 | [Build capstone specialists](CAPSTONE.md#18-build-and-release-the-specialists) | K02 and applicable specialist regressions | Small tasks, diff review, focused debugging |
| 19 | [Build and release capstone workflow](CAPSTONE.md#19-build-release-and-demonstrate-the-workflow) | K03, G01-G03, W01-W03, P01-P04 | Handoff with evidence and cleanup choices |

Each checkpoint depends on the preceding checkpoint. Both prompt agents must
pass and be released independently before checkpoint 15 introduces executable
orchestration. Where a checkpoint has substeps, test and pause between them.
The optional Weather delivery lab is offered only after 07; skipping or
completing it leaves the numbered route unchanged and continues at 08.
Capstone selection happens at 17 if the participant chooses that follow-on,
not during setup or as extra work inside the core time budget.

Each lesson also has an **App practice** and **Alternative**. Try the primary
approach and explain when the alternative is useful; repeating the whole lesson
is unnecessary. See [APP-GUIDE.md](APP-GUIDE.md) for examples and UI fallbacks.
At occasional natural pauses, the coach offers a short
[experience check-in](COACH.md#occasional-experience-check-ins): keep or adjust
the execution balance, or the product-specific Beginner/Intermediate/Expert
explanation level. One optional question at a time; no repeated assessment or
change to required approvals, hands-on practice or evidence.

## Student controls

| Say | Coach behavior |
|-----|----------------|
| "Start the workshop" | Begin 00; one question at a time |
| "Resume the workshop" | Recheck local progress and the target, then continue |
| "Give me a hint" | Explain the smallest missing idea without solving future steps |
| "Explain, don't edit" | Inspect and teach without modifying files or resources |
| "Help me implement this step" | Make only the current agreed change |
| "Show another way" | Compare a relevant alternative and its tradeoff |
| "Test this checkpoint" | Execute the current tests and applicable regressions |
| "Show my progress" | Show passed, failed, blocked, and not-started gates |
| "Pause the workshop" | Save progress; leave cloud resources unchanged |
| "Clean up" | List exact owned targets and ask before stopping/deleting |

## Completion

Core completion requires checkpoints 00-16; an explicitly chosen capstone
extension also requires 17-19. Leave unchosen capstone checkpoints not started,
not passed. All checkpoints required for the agreed route must pass, with
observed test evidence and student teach-back. A compatible alternative app interaction can satisfy app practice;
an unavailable UI control must not block the course. An unavailable required
Microsoft Foundry capability does block its integration checkpoint.
Microsoft Teams/Microsoft 365 Copilot publication and live use are required
at 07 and 16. A missing tenant permission, policy, entitlement or supported
runtime/approval path blocks that gate; an endpoint-only result is not core
completion.

An explicitly approved partial route stays labeled incomplete. The facilitator
can review evidence the coach cannot verify; the coach is not an independent
examiner or a certification service. Follow [FACILITATOR.md](FACILITATOR.md) for
cohort preparation and rehearsal.
