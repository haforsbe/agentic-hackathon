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

Follow **build one capability, test its supported result, then continue**.
The required participant path does not include deliberate failure, denial,
unsupported-input or outage demonstrations. Existing automated defensive
tests remain implementation checks; handle real problems when encountered.

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
supported trip, source attribution and actual permission handling must work in the
chosen destination; see [test parity](PUBLISHING.md#workflow-destination-test-parity).
Microsoft Copilot Studio's test pane is not a published channel. The existing
CH02 requirement still needs actual Microsoft Teams or Microsoft 365 Copilot
use, either directly or after the Microsoft Copilot Studio integration.

Each module opens with its checkpoint, plain-language goal and short plan.
Before tests, the coach explains their purpose and expected evidence; at the
close, actual results lead to a short learning summary, the existing single
understanding check and the next step. After a passed checkpoint, the coach
introduces the next required checkpoint automatically, without a routine
continue/pause question. Say **"Pause the workshop"** when you want to stop;
explicit pauses and agreed stopping points remain binding. Required approvals,
hands-on results and learning checks still stop the flow when input is needed,
and optional work still requires your choice. For specified tests, you may give a
[scoped batch approval](COACH.md#scoped-test-approvals) instead of repeated
per-call cost approvals. The coach retains available Microsoft Foundry tokens;
routine price lookups/calculations are removed. A monetary estimate at the end
is optional, not a completion requirement or billing cap. Resource changes,
explicit cost restrictions and human tool approvals remain separate.

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
| Skills and multiple tools (temporarily deferred) | Skip 05; retain weather research procedure | Skip 12; retain cultural research procedure | 15 still validates formal result contracts |
| Persistent memory (temporarily deferred) | Skip 06 | Skip 13 | Lessons retained for later; no memory prerequisite |
| Independent release | 07 | 14 | 16 releases the hosted workflow |
| Publish and use in Microsoft Teams and/or Microsoft 365 Copilot | 07, after release and before 08 | No additional channel publication required | 16, after final release/update checks |
| Agent collaboration | Specialists stay independently callable | Specialists stay independently callable | 15-16 coordinate both releases |

The learning path keeps both prompt agents independently publishable.
It teaches [direct MCP connections](MCP-CONNECTIONS.md): attach Weather's
public server with only `weather_forecast` at 04 and verify that same one-tool
binding at 07. Independently attach only `find_museum_guide` to Cultural at 11.
Skills and four-tool expansion at 05/12 are retained but deferred. At 14 verify both releases
without migrating or re-releasing unchanged Weather.
Tools supply operations; skills guide use without granting access.
Each specialist retains only its own tools, explicit allowlists and native
per-call human approval. Toolboxes and authentication connections for them
are deferred, not prerequisites or core exercises.
The current curriculum is `two-specialists-workflow-v10`; earlier progress
requires an agreed migration, not automatic new passes. Version 10 replaces
Toolbox requirements with direct-MCP T01-T03 evidence without renumbering.
Preserve the required Weather CH01 and workflow CH02 channel gates at 07 and
16. The hosted workflow and checkpoint numbering are unchanged; the default
route skips the retained skill and memory lessons.
Existing Toolbox-path evidence does not prove a direct binding, and endpoint
evidence is not channel evidence. See
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
manual workflow with explicit commit/intent confirmation deploys to the separate
Prod agent. No GitHub Environment is required; merge alone does not deploy.
The workflow is not live-rehearsed or configured with Azure OIDC/project
permissions; a successful deploy does not establish MCP runtime execution or
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

## Temporary skills and multi-tool deferral

Student agent skills and their associated multi-tool expansion are temporarily
outside the default route, not removed from the curriculum. Skip 05 and 12
alongside deferred memory at 06/13: continue **04 -> 07** and **11 -> 14**.
Weather retains only `weather_forecast`; Cultural retains only
`find_museum_guide`. Do not add the other tools, compose/upload a skill, create
a skill-only candidate, or run T02/S01/S02 merely to fill the skipped slots.
Keep managed Conversations at 03/10 and all active identity, native approval,
runtime, release, workflow and CH01/CH02 channel gates.

Treat 05/12 and T02/S01/S02 internally as **deferred, not passed**, without a
status ledger or participant-facing announcement. They do not block release,
publication, workflow or completion of
this skills-and-memory-deferred route. Skill versions/delivery are required
only when configured. Test each specialist's supported one-tool result at
release; do not add an isolated failure or denial exercise.

Keep the lesson text, tool/schema references and tests available for later
reintroduction. Adding skills or expanding tools later requires an explicit
scope decision, reviewed delivery/allowlist changes and separate approvals,
then applicable T02/S01/S02 and affected consumer, workflow and channel regressions.
Do not silently remove existing skills, shrink an existing expanded allowlist,
delete drafts/resources, discard evidence or resume a paused participant.
On an explicit later resume, introduce the next active goal and continue at the
first unmet active gate; no skip question or automatic draft application.
Existing skill-enabled or expanded candidates retain their applicable checks
until a separately approved configuration change.

This defers student agent capabilities, not the installed Microsoft Foundry
or Agent Framework builder skills used by Workshop Coach for supported work.

## Temporary memory deferral

Persistent Microsoft Foundry memory is temporarily outside the default workshop
route, not deleted from the curriculum. Skip 06 and 13; with the skills deferral
also active, continue 04 -> 07 and 11 -> 14 without creating memory stores,
adding embedding deployments, storing preferences, or running M01-M03.
Keep managed Conversations at 03/10.
Keep this deferral internal; do not announce it at transitions or turn it into
another participant decision, exercise or understanding check.

Treat 06/13 and memory-only assertions internally as **deferred, not passed**,
without a status ledger or participant-facing announcement. They do not block
release, channel publication, the hosted
workflow or completion of this skills-and-memory-deferred route. All other applicable
tests, identity/Conversation isolation and native approvals remain required.
Use the ordinary D tests, not post-memory variants, when no memory is attached.
Report core completion through the demonstrated capabilities, without a
deferral label or a claim that skills or memory passed.
Checkpoint numbering and retained lesson/test identifiers
stay stable.

Reintroduce the retained lessons only after an explicit scope decision and
approval for the required configuration, data retention and possible costs.
Then run M01-M03 and the affected specialist, consumer, workflow and channel
regressions on the changed versions/paths before claiming memory support.
Do not silently remove or disable memory on an existing participant's agents,
erase previous evidence, migrate legacy progress, or resume a paused participant
during authoring. An existing memory-enabled candidate still needs its applicable
safety/isolation evidence; changing it requires separate approval.

## Checkpoints

| ID | Lesson | Required test evidence | App practice |
|----|--------|------------------------|--------------|
| 00 | [Setup](SETUP.md) | Participant's dedicated project (existing or created during setup), direct project identity check, operation-specific permission verification, deployment inventory, participant choice to reuse or explicitly approve a Model Deployment, ownership, capability inventory | Repo context, cost boundary, and approvals |
| 01 | [Weather baseline](01-prompt-agents.md#01-create-the-weather-research-agent) | B01-B02 | Explain vs implement |
| 02 | [Weather instructions](01-prompt-agents.md#02-refine-weather-instructions) | I01 | Review a focused instruction diff |
| 03 | [Weather conversations](01-prompt-agents.md#03-test-weather-managed-conversations) | D01-D02 | App session vs runtime Conversation |
| 04 | [First Weather MCP tool](01-prompt-agents.md#04-connect-the-first-weather-mcp-tool) | T01 direct forecast-only binding, supported C01 on the chosen execution route and guided trace inspection | Any actual native permission decision on the chosen route; forecast evidence |
| 05 | [Weather skill and multiple tools (deferred)](01-prompt-agents.md#05-guide-multiple-weather-tools-with-a-skill) | T02/S01 deferred, not passed; keep forecast-only binding | Retained for later |
| 06 | [Weather memory (deferred)](01-prompt-agents.md#06-add-and-test-weather-memory) | Not run or passed; continue 04 -> 07 | Retained for later |
| 07 | [Release and publish Weather Research Agent](01-prompt-agents.md#07-release-the-weather-research-agent) | T03 final direct binding, final-path regressions, P01-P03, then CH01 channel publication/use before 08 | Distinguish release from publishing; review the participant's channel test evidence |
| 08 | [Cultural baseline](01-prompt-agents.md#08-create-the-cultural-travel-agent) | B01-B02 | Compare independent agent definitions |
| 09 | [Cultural instructions](01-prompt-agents.md#09-refine-cultural-instructions) | I01 | Review a focused instruction diff |
| 10 | [Cultural conversations](01-prompt-agents.md#10-test-cultural-managed-conversations) | D01-D02 | Verify isolated runtime state |
| 11 | [First Cultural Travel MCP tool](01-prompt-agents.md#11-connect-the-first-cultural-travel-mcp-tool) | T01 direct museum-guide-only binding and supported C02 on the chosen execution route | Any actual native permission decision on the chosen route; guide evidence |
| 12 | [Cultural skill and multiple tools (deferred)](01-prompt-agents.md#12-guide-multiple-cultural-tools-with-a-skill) | T02/S02 deferred, not passed; keep museum-guide-only binding | Retained for later |
| 13 | [Cultural memory (deferred)](01-prompt-agents.md#13-add-and-test-cultural-memory) | Not run or passed; continue 11 -> 14 | Retained for later |
| 14 | [Release Cultural Travel Agent](01-prompt-agents.md#14-release-the-cultural-travel-agent) | Cultural final-path regressions/P01-P03, unchanged Weather release/dependency verification, T03 isolation and two-agent comparison | Review two independent direct-MCP releases without a planned Weather migration |
| 15 | [Build Trip Planning Workflow](02-hosted-agents.md#15-build-and-test-the-trip-planning-workflow) | Workshop Coach creates the code-first workflow using the reviewed host; existing automated checks, G01/G03 and a supported W01/W03 trip | Review and explain coach-generated contracts, coordination, request-owned state, approval bindings and traces |
| 16 | [Deploy, release and publish workflow](02-hosted-agents.md#16-hosted-release) | Supported W01/W03 remotely, actual portal W04, P01-P04, then CH02 on the final version | Review any requested tool decisions and sourced output; send a channel request and inspect both specialist calls |
| 17 | [Choose a capstone](CAPSTONE.md#17-choose-and-scope) | K01 | Turn an idea into a bounded two-specialist plan |
| 18 | [Build capstone specialists](CAPSTONE.md#18-build-and-release-the-specialists) | K02 and applicable specialist regressions | Small tasks, diff review, focused debugging |
| 19 | [Build and release capstone workflow](CAPSTONE.md#19-build-release-and-demonstrate-the-workflow) | K03, existing automated checks, G01/G03, supported W01/W03, P01-P04 | Handoff with evidence and cleanup choices |

Each active checkpoint depends on the preceding active checkpoint; 05/06 and 12/13
are temporarily deferred under the policy above. Both prompt agents must
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
| "Resume the workshop" | Recover the current step from chat and recheck the target, then continue |
| "Give me a hint" | Explain the smallest missing idea without solving future steps |
| "Explain, don't edit" | Inspect and teach without modifying files or resources |
| "Help me implement this step" | Make only the current agreed change |
| "Show another way" | Compare a relevant alternative and its tradeoff |
| "Test this checkpoint" | Execute the current tests and applicable regressions |
| "Show my progress" | Show passed, failed, blocked, and not-started gates |
| "Pause the workshop" | Acknowledge the pause/current step in chat; leave files and cloud resources unchanged |
| "Clean up" | List exact owned targets and ask before stopping/deleting |

Participant answers, preferences and coaching progress stay in chat history.
The coach reuses loaded context rather than reading/writing `progress.json`.
Legacy files remain untouched unless an import/export is explicitly requested;
required execution evidence and interrupted-operation recovery are separate.
If earlier chat context is unavailable, recover or ask for the missing fact,
not the whole questionnaire; never infer a pass or missing approval.

## Completion

Core completion requires the active checkpoints in 00-16, excluding deferred
05/06 and 12/13; an explicitly chosen capstone
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
