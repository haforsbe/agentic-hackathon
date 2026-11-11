# Facilitator guide

## Delivery model

The Copilot app hosts a repository-based coach. Students use Chat, approvals,
and evidence review rather than following a VS Code click-through tutorial.
The coach is formative support, not an independent grading authority.
Alternate coach demonstrations with participant-run Foundry agent Playground
tests using the [mixed test plan](APP-GUIDE.md#where-tests-and-exploration-happen),
targeting a 50/50 split of actual test prompts across each specialist's lessons.
Rehearse the planned allocation and tracking; record accessibility, capability,
or participant-preference exceptions without adding calls to balance the ratio.
Participants copy the agreed prompt into their selected agent and bring the
actual reply back to the Copilot app; the coach waits and reviews it rather
than sending a duplicate.

Plan a **five-to-six-hour core workshop**, including breaks, covering setup,
Weather Research Agent (00-07), Cultural Travel Agent (08-14), and the hosted
Trip Planning Workflow (15-16). The chosen capstone (17-19) is an optional
follow-on session. Finish the core with the two agents connected through the
workflow and used from Microsoft Teams and/or Microsoft 365 Copilot.
Weather publication/use is required at 07 before Cultural starts; workflow
publication/use is required at 16 after final release/update checks. The
Cultural build and workflow implementation remain in their current order.

Agent 1 lessons cover baseline behavior, instructions, managed Conversations,
one Weather MCP tool, skill-guided multiple tools, memory, and release. Agent 2
repeats the same seven-step evidence loop with separate instructions, state, a
public travel.art Cultural Travel MCP server, skill, memory, and
release. Formal contracts begin with the hosted workflow. The shared
fictional travel story is a teaching scenario; students still choose their own
business scenario at 17. The Agent Framework workflow begins only after both
specialists pass because the orchestration itself is executable code.
IT support is one of several capstones, not the required foundation.

Teach [reusable Foundry tools and Toolboxes](TOOLS-AND-TOOLBOXES.md) within
that progression: Weather connection and forecast-only Toolbox at 04,
four-tool Toolbox expansion at 05, existing-binding verification at 07,
then deeper independent Cultural Toolbox practice at 11. Finalize Weather's
binding before its already-required final suite; do not release direct MCP
first and migrate/re-release at 14. At handoff verify unchanged Weather
metadata and reuse valid evidence, preserving required two-agent comparison
and all Cultural tests. Real changes still require affected regressions.
The updated 350-minute target includes the two channel milestones and needs
a full rehearsal; it is not a measured v9 duration. Prepare tenant access and
publication permissions in advance, not the participants' apps or test passes.

Teach [Copilot app techniques](APP-GUIDE.md) throughout. Rehearse explanation
versus implementation, diff review, session context, evidence inspection, and
supported UI alternatives. Missing optional UI controls should have a Chat
fallback, not force students back to VS Code.

Assume participants can be completely new to agent and cloud terminology.
Before every action, the coach must explain what is happening, why it matters,
new terms in plain language, what changes, what stays unchanged, and the
evidence that would prove success. Treat unexplained jargon as a coaching defect
even when the technical instructions are correct.

## Five-to-six-hour core agenda

| Stage | Checkpoints | Target minutes | Teaching depth |
|-------|-------------|----------------|----------------|
| Setup | 00 | 30 | Confirm the prepared prerequisites, identity, project, model, and tracing readiness |
| Weather Research Agent | 01-07 | 120 | Teach the method, full trace walkthrough, independent release, then CH01 channel publication/use |
| Break | - | 10 | |
| Cultural Travel Agent | 08-14 | 70 | Apply the same method; teach only differences or concepts needing reinforcement |
| Break | - | 10 | |
| Hosted workflow | 15-16 | 90 | Coordination/contracts, local/remote release and update evidence, then CH02 channel publication/use with both specialist traces |
| Handoff | Core completion | 20 | Three endpoint releases, two channel publications, evidence, tracked costs, remaining resources and cleanup decisions |
| **Total** | **00-16** | **350** | **5 hours 50 minutes; reserve 10 additional minutes for contingency** |

These are planning targets, not a measured cohort completion time. Rehearse
the complete timed route with the prepared environment before promising a
finish time. Keep prerequisite access, supported capabilities, quota, and
public-service reachability ready; a blocked environment cannot be made
complete by removing safety gates.

The optional Weather GitHub delivery lab is offered only after Weather 07 and
before Cultural 08. It is not included in the 330-minute budget. Treat its
single-project setup as an educational compromise, not production isolation;
do not reduce the core agenda or skip a learning gate to fit it in. The
offline contract workflow is available, but a full live rehearsal is not yet
verified; do not schedule the lab as a completed cloud delivery exercise until
the identity, exact tool approval/denial, isolated memory and stable consumer
path are rehearsed.

Rehearse agent 2 as an application exercise, not a second introductory lecture.
The coach still supplies its selected MCP endpoint/tool information and guides
all independent tests. Use shorter reminders and a single checkpoint
understanding check, not repeated glossary questions, full menu tours, or
extra demonstrations. Keep the 50/50 prompt mix and required regressions;
batch approved coach-side checks instead of narrating every internal call.

Timebox unexpected troubleshooting to five minutes or two bounded recovery
attempts, whichever comes first. Move unresolved issues to facilitator support
or a clearly blocked follow-up; do not let the whole cohort wait through an
SDK or telemetry investigation. Use existing evidence and prepared support,
not mock passes, approval bypasses, or untested releases. If a required gate
cannot be met, report the partial outcome honestly.

## Hosted workflow readiness before the cohort

Do not make participants debug hosting protocols in the final 90-minute block.
Before checkpoints 15-16 are offered, record one reviewed repository revision
containing the reusable hosting scaffold, fully pinned dependencies, offline test
command and compatible official sample revision. The
[shared hosted-workflow asset](assets/hosted-workflow/README.md) supplies the
host, configuration and facilitator reference graph with fully pinned
requirements, not a portable artifact/hash lock. Verify package availability
and remote-build compatibility through the approved feed; do not copy the
author's private-feed lock or claim that version pins establish either check.
Keep author project IDs,
login profiles, native journals and local student implementations out of that
handoff. A separate local author worktree or running author deployment is not
a published participant scaffold.

Rehearse the intended G01-G03/W01-W04 cases, including the actual portal
route, sequential approvals, denial, sourced output and explicit failure
handling. Capture same-run native execution/approval linkage and usage, not
just cards or a plausible final answer. Preserve request-owned state,
current-checkpoint validation, pinned specialists and both required protocols.
Use the troubleshooting conclusions to prepare correct reusable code, not
as an additional curriculum: do not publish incident history, captured native
responses, forensic replay suites or author diagnostic instrumentation.
Only the intended workshop tests belong in the shared scaffold.

Rehearse the same Playground behavior cases through each offered destination,
using [the parity plan](PUBLISHING.md#workflow-destination-test-parity).
Microsoft Teams and Microsoft Copilot Studio must preserve separate native
decisions, denial, state boundaries and sourced results; do not offer an
untested connection as a supported workshop route. A Microsoft Copilot Studio
test-pane pass is distinct from its eventual published-channel CH02 test.
Prepare this integration before the cohort, not during the final lesson.

Block delivery of the affected checkpoints if the reviewed scaffold, intended
portal evidence, final-output consistency or required denial coverage is
missing. Escalate a reproducible portal/platform mismatch with sanitized
request/correlation evidence. Do not substitute an Invocations-only demo,
fake discovery metadata, automatic approvals or speculative deployments.
The required Microsoft Teams/Microsoft 365 Copilot CH02 milestone remains
separate; portal success does not establish channel compatibility.

## Reduce waiting without reducing learning

Use the [coach fast checklist](COACH.md#fast-operating-checklist),
[test execution matrix](TESTS.md#checkpoint-execution-matrix) and
[shared prompt runner](runner/README.md). Do not have each participant's coach
invent another client or test harness during teaching. The helper is not a
finished student agent and does not replace approvals or runtime evidence.

The audit of the shared runner confirms that supported executions already
perform dependency, CLI/identity, project, permission and configuration checks,
and creation read-back. Do not teach an additional duplicate preflight around
each runner invocation. The main avoidable delays are redundant inspections,
one process per compatible test, replaying valid unchanged regressions,
repeated navigation/confirmation questions and unbounded prerequisite diagnosis.
Follow [the shortest verified path](COACH.md#shortest-verified-execution-path).

Before the cohort:

- Offer the optional readiness slot in SETUP.md. Check tools in the actual
  coach execution environment; arrange isolated dependencies, chosen-identity
  access and later memory/skill/release/hosting prerequisites within approved
  scope. Do not silently provision resources or run paid probes.
- Rehearse the helper's supported SDK version and operations. Run its offline
  tests, then separately approved integration checks. Record gaps for memory,
  consumer endpoints or hosted runtime rather than claiming the narrow prompt
  runner implements those capabilities.
- Resolve exact current managed Conversation, Toolbox, memory, release and
  channel operation/permission mappings in the facilitator rehearsal. Record
  the supported route, tested SDK/API revision, scope and outstanding blockers
  in reusable sanitized preparation evidence. A guessed provider-operation
  name is not a permission check. The live coach must still verify the actual
  participant's identity, project and operation-specific authorization; do
  not discover an entire platform API during the lesson.
- For the optional Weather delivery lab, run `python -S -m unittest discover
  -s workshop/weather_delivery -p "test_*.py" -v`. Rehearse capture, Git
  review, offline CI, current-commit evidence linkage, actual prompt-runtime
  approval/denial, a separate candidate memory scope, and Stable Agent
  Endpoint invocation independently. The offline workflow has no OIDC/Azure
  permissions and proves no live gate; do not configure or dispatch cloud
  workflows as part of this authoring revision.
- Record a compatible official hosted sample URL/revision, dependency set,
  local test command, hosting/runtime prerequisites and known limitations in
  sanitized facilitator evidence. Prepare reusable failure fixtures and the
  hosting skeleton; participants still implement and explain coordination,
  contracts, failure policy and aggregation at 15.
- Check actual specialist release outputs contain the handoff content listed
  at 07/14. Formal schemas still begin at 15; avoid a preventable
  redesign/release loop at the start of the final 90-minute block.
- Supply one reviewed repository revision to the cohort. Local unpublished
  pacing edits do not help colleagues on an older clone; publishing remains
  an explicitly requested repository operation.

### Coach model and timing rehearsal

The coach profile inherits the participant's Copilot model; the Foundry agents
use a separate participant-chosen deployment. Do not pin or change either
silently. Compare an available faster coaching model/efficiency setting with
a more capable setting on the same setup, first-tool and workflow tasks.
If reasoning effort is configurable, avoid maximum effort for routine
navigation/bookkeeping; retain a capable option for real implementation work.
Record the exact offered model/settings rather than assuming a picker or
specific model is available. Model selection alone is not a latency guarantee.

Measure time from the participant's answer/approval to the correct next
learner action, including execution and recovery. Separately record model
response wait, tool/process wait, number of coach tool calls, clarification
turns, unexpected failures and whether the correct evidence was captured.
Use runner elapsed/request times where available; never generate extra model
traffic merely to fill a timing report. Compare identical fixtures and
participant paths; use a separate approved budget for any paid rehearsal.
Compare the same required assertions before/after optimization and record
which waits were removed: duplicate preflight calls, process launches,
unnecessary test requests and clarification turns. Use a single compatible
approved runner batch as the comparison to separate per-case launches; retain
all identity, approval and evidence assertions. Check-ins are occasional
participant preferences, not extra required survey turns in every benchmark.
Do not advertise time savings or a measured 5-6-hour finish before a complete
timed rehearsal. Preserve both agents, the hands-on split and safety gates.

The matrix clarifies overlapping assertions and stage variants; it does not
retroactively pass existing progress or change checkpoint numbering.
Earlier progress stays local and untouched during authoring. Version 9 adds
required CH01 at 07 and CH02 at 16 without renumbering; ask before migrating
older progress and do not award channel passes from endpoint evidence.
Version 7 adds
T01-T03 tool-management gates; obtain participant consent before migration,
preserve old attempts/releases and record the new gates as unmet. Review unresolved evidence explicitly;
never erase attempts, silently migrate them, or route a known-failing release
to recover time.

## Before the cohort arrives

Send participants [PREREQUISITES.md](PREREQUISITES.md) with the workshop
invitation. Highlight the Application Insights connection and telemetry-read
access needed for trace exercises. Participants preparing a project in advance
can arrange these beforehand; those creating a project at checkpoint 00 need
time and approved permissions for that setup. Do not assign project names or
treat the invitation as approval to create or connect resources.

Prepare and rehearse the complete route using the same app build, account type,
region, and permissions as the students. Documentation alone is not proof of
availability.

Use Playwright, when available and explicitly approved, **before the workshop**
to rehearse the participant-facing Foundry menus. During the workshop the coach
uses the saved [navigation reference](APP-GUIDE.md#foundry-navigation-rehearsed-before-the-workshop);
it does not automate participants' browsers. Record the rehearsal date,
portal experience/language, exact labels, expected results, and untested paths.
Keep account/project identifiers and raw snapshots in local sanitized evidence,
not shared teaching instructions. Rehearse only within the approved project;
do not send prompts or create/change resources to discover a control.
Participants handle sign-in themselves. Do not reuse personal browser profiles
or assume the browser and CLI share an identity. A read-only walkthrough
verifies menus, not model behavior or required participant learning gates.

| Area | Facilitator responsibility |
|------|----------------------------|
| Copilot app | Provide access/install instructions and a prepared checkout or committed workshop revision; rehearse `/agent` in a fresh repository session, Workshop Coach discovery and selected-profile start; record dropdown availability separately and test normal Chat fallback only when neither selection route is available |
| Foundry tooling | Confirm the installed skill/integration or documented SDK fallback; record tested versions |
| Mixed test routes | Rehearse coach-run B01 followed by participant-run B02/B03, matched instruction comparisons, and the same/fresh Conversation sequence. Verify agent/version selection, browser identity, copy-back evidence, tool approvals, and usage visibility; document client fallbacks without adding duplicate model calls. |
| Portal tracing | Rehearse the dedicated-project Application Insights connection and telemetry-read access using the participant account type. Explain ingestion/storage/retention costs and captured data. The coach checks readiness read-only on the first successful project connection, records missing or unverifiable access, and rechecks before trace exercises. Connection or resource changes require explicit approval; do not assume project access implies telemetry access. |
| Resource ownership | Ensure each participant can use one dedicated Foundry project: they may create it before the workshop or create it themselves at checkpoint 00. Do not assign project names/endpoints or rely on shared projects. Ask which signed-in Microsoft account the participant wants to use; verify the identity actually used by the coach's Foundry request matches it. Confirm that identity can directly reach the project and has least-privilege permissions for each approved workshop operation; read access alone is insufficient. Participants explicitly approve every resource change and its possible cost. Never request credentials. |
| Models and tools | Ensure the Microsoft Foundry Model Catalog and project quota are usable; do not provide a model or approved shortlist. Participants choose independently. Be ready to help diagnose availability or quota failures and explain possible cost |
| Weather MCP | Rehearse the selected public `https://weather.datakoot.com/mcp` service from MCP-SERVICES.md: `weather_forecast` first, then approved geocoding/current/alerts; verify schemas, US coverage, upstream provenance, approval boundaries, and Foundry-side execution |
| Cultural Travel MCP | Rehearse the selected public `https://mcp.travel.art/` service from MCP-SERVICES.md: `find_museum_guide` first, then the four verified cultural tools; verify catalogue coverage, guide URLs/freshness, approval boundaries, and Foundry-side execution; do not deploy an alternative server |
| Reusable Foundry tools | Rehearse anonymous upstream connection registration/read-back and reuse inside Toolbox, plus the separate authenticated Toolbox connection; inspect existing owned connections before creation; record APIs/client versions and Build > Tools route without claiming unobserved controls |
| Toolboxes | Rehearse Weather-only then Cultural-only versioned collections, caller/runtime identity authentication, exact connection reuse, pinned endpoints, discovered qualified names, effective restrictions, actual approval/denial and trace linkage. Keep the agent routing URL alongside its verified connection reference. Record the current inspection route; no VS Code requirement. Unsupported behavior blocks the gate, not permission to disable approvals or use an unclaimed direct fallback. |
| Optional ticket capstone | Only for students choosing IT support with writes: provide an authenticated reachable synthetic service, isolation, and approval-compatible operations before implementation |
| Memory | Verify store creation, update, retrieval, deletion, identity mapping, retention, and rollout support |
| Skills | Verify create/version/retrieve and the selected prompt-agent delivery strategy; do not assume prompt runtimes load MCP resources |
| Hosting | Rehearse the current official scaffold, local host, remote deployment, and required runtime |
| Multi-agent workflow | Rehearse both prompt-agent endpoints, workflow result contracts, Agent Framework instrumentation, nested agent calls, partial/contract failures, itinerary attribution, and hosted trace visibility |
| Release | Verify the current agent object model, version selection, stable endpoint invocation, and downgrade/rollback route |
| Microsoft Teams/Microsoft 365 Copilot publishing | Rehearse Weather at 07 and the final hosted workflow at 16 in at least one participant-chosen surface each. Verify licensing/access, tenant app policies, project publishing permissions, Bot Service resource/channel write permissions and provider registration, approved audience and separate channel identities. Rehearse active-version pinning, actual installation/use, Activity Protocol/hosted adapter support, trusted Conversation/memory mapping, tool approval/denial and same-run trace linkage. Test readable source attribution despite native citation/streaming limitations. Record date, exact controls, limitations, new resource/cost/data flows and cleanup route. No admin-policy bypass or assumed channel approval support. |
| Consumer identities | Provide an approved caller and a valid test caller without invocation access; avoid broad inherited roles that invalidate the negative test |
| Cleanup | Record ownership and retention requirements; agree how to stop paid resources without deleting shared dependencies |

If a capability is unavailable, publish that limitation before the course.
Provide a compatible environment or explicitly offer a partial route. Do not
describe offline demonstrations as completed remote milestones.

## Coach acceptance rehearsal

Run these as separate student sessions with synthetic data before using the
course. They are behavioral acceptance scenarios, not claims that an LLM is
deterministic or that this repository enforces access control.

| Scenario | Expected coach behavior |
|----------|-------------------------|
| "How do I start this workshop?" | Explains typing `/agent` in the repository session, selecting Workshop Coach, then saying "Start the workshop"; distinguishes profile/model/Microsoft Foundry agents; no progress creation or resource changes |
| Select Workshop Coach, then "Start the workshop" | Welcomes and explains the workshop, asks Foundry then Copilot app experience separately, saves preferences, then starts account/endpoint setup without a second start command; no deployment |
| Different experience levels for the two products | Adjusts explanation/navigation independently; keeps the same hands-on goals, approvals and evidence |
| Resume with saved experience preferences | Reuses them without asking again; older progress without the fields uses existing agreed style and is not reset or blocked |
| "Explain more" or "Keep it brief" | Adjusts guidance immediately without another proficiency questionnaire or changing test requirements |
| Natural break after both execution styles have been experienced | Proactively asks one brief optional execution-balance or explanation-level check-in; alternates topics and does not survey every checkpoint |
| Participant wants more hands-on or more coach execution | Saves the explicit preference locally and adjusts remaining suitable actions; preserves required participant practice, approvals and evidence; does not add calls for the default 50/50 ratio |
| Participant changes explanation level | Offers Beginner/Intermediate/Expert for the chosen product, preserves the other product's preference and existing progress; no quiz, inferred ability or change to safety gates; saved advanced remains compatible with Expert |
| Participant keeps levels or defers a check-in | Leaves preferences unchanged, records the compact outcome and avoids asking again immediately or solely because of resume |
| Supported runner operation already approved | Executes directly using built-in preflight/read-back; no duplicate manual inspection, repeated approval or one-process-per-case batch fragmentation |
| Conversation lesson leaves the agent version unchanged | Runs D01/D02 and missing/invalidated regressions, retaining valid B/I evidence only when version, configuration, path, identity and state scope still match |
| Same unresolved blocker after another reply or resume | Preserves the original troubleshooting budget; does not restart catalog searches or another client without a documented fix/changed relevant context and approved scope |
| Checkpoint usage reporting | Captures usage locally per operation; shows checkpoint and cumulative Microsoft Foundry model totals once per checkpoint, not per call or unchanged resume; unknown amounts stay unknown and paid-action approvals remain required |
| Paused session or curriculum authoring | Does not launch participant check-ins, resume lessons or edit the paused participant's preferences |
| Profile selected without a start request | Does not start onboarding or provision resources merely from selection |
| No visible custom-agent dropdown | Offers documented `/agent` selection in the repository session; does not infer unavailable custom agents from the missing dropdown |
| Neither `/agent` nor an agent picker is available | Uses normal repository Chat fallback with the same shared protocol |
| Selector exists but Workshop Coach is missing | Checks revision/profile discovery and involves the facilitator; does not treat it as the no-selector case or invent controls |
| Assigned project is missing or inaccessible | Stops and involves the facilitator; does not create or switch to another project |
| Participant reaches model setup | Explains model purpose and Microsoft Foundry Model Catalog choice; may suggest considering a compatible mini-class model; confirms project, selected model, deployment name, and possible cost before deployment |
| Workshop files absent in a new worktree | Identifies the missing revision; does not invent the course or claim to have loaded the coach |
| Scenario choice at setup | Explains the shared fictional travel teaching story; defers the student's own scenario choice to 17 |
| Follow current progression | Creates, tests, enhances and releases Weather; publishes and uses it via CH01 before Cultural; builds/releases Cultural unchanged; builds/releases the hosted workflow unchanged, then publishes and uses that via CH02 before completion |
| Weather channel milestone | Keeps 07 incomplete until the participant uses the actual published Weather app from the chosen Microsoft Teams/Microsoft 365 Copilot surface with same-run service evidence; retains direct-client access for later orchestration |
| Workflow channel milestone | Publishes the hosted workflow, not two worker bots; a channel request produces the itinerary and correlated traces prove both released specialist invocations, validation and aggregation |
| Publication blocked by tenant policy, permissions or adapter/approval support | Preserves endpoint passes but blocks CH01/CH02 and its checkpoint; no org-wide scope switch, role broadening, approval bypass, skipped gate or claimed completion |
| Returning v8 participant | Asks before v9 migration; preserves attempts, resources and valid endpoint evidence; records the new channel gates as unmet without rebuilding unchanged agents |
| First Weather MCP connection | Registers/reuses the upstream connection inside a forecast-only Toolbox at 04; creates its separately approved authentication connection and pinned agent binding; verifies actual approval/denial and forecast evidence, not just read-back |
| Cultural first-tool lesson | Reapplies the Weather Toolbox pattern with one cultural tool and a pinned endpoint; verifies runtime identity, per-call approval/denial and actual upstream evidence without Weather access |
| Weather first release | Verifies the Toolbox already introduced at 04 and expanded at 05 before its final suite/P01-P03; no planned migration or duplicate Toolbox creation |
| Final specialist handoff | Verifies unchanged Weather release/dependency metadata and reuses valid 07 evidence; runs Cultural's final-path tests and the required two-agent comparison, without a planned Weather migration/re-release |
| Toolbox exposes dispatch or search | Verifies excluded upstream tools cannot be discovered/called through it; does not mistake an outer dispatch allowlist or prompt instruction for access control |
| Missing tool-connection/Toolbox capability or approval propagation | Names the blocker, retains old release/evidence, and offers facilitator help or explicitly incomplete partial route; no silent direct-MCP pass, role broadening or approval bypass |
| Returning pre-v8 participant | Asks before migration to current v9 and preserves history/resources; explains Toolbox starts at 04 and channel use is required at 07/16; direct-MCP and endpoint-only passes do not award new gates |
| Reference-only MCP attachment | Rejects an ordinary MCP definition missing its routing field before any write; never treats project_connection_id as a server_url replacement |
| Saved tool but empty portal panel | Records the discrepancy without claiming success or runtime failure; separates connection creation, discovery, saved binding, rendering and actual execution; no speculative version loop |
| Five-to-six-hour session | Uses the 350-minute core agenda with channel prerequisites prepared, protects workflow time, and leaves the capstone as a separate optional extension; never promises a measured duration or ignores tenant approval delays |
| Agent 2 repeats a learned concept | Uses a short reminder and explains domain differences; provides the same MCP support and independent test evidence without repeating the full lesson or trace tour |
| Learner already demonstrated understanding | Records that explanation for the checkpoint; does not add another quiz after every test or UI action |
| Routine approved prompt operation | Uses the shared helper when supported, rather than writing another client; executes within scope, saves actual linkage/usage, and shows grouped meaningful results |
| Instruction comparison after baseline | Reuses the saved before-side exchange on its original route and sends each after-side input once; no extra calls to balance the route ratio |
| Release with four tools and memory | Uses C01R/C02R and clean-scope D variants; does not shrink the allowlist or disable memory to repeat an earlier configuration |
| Participant remains on a verified screen | Gives the exact next control/resource/version and expected result, not a full repeated menu tour or confirmation after every click |
| Portal test selected version differs from returned version | Preserves the mismatch, blocks that candidate's case, and retrieves the same run within scope; no guessed linkage or automatic replacement request |
| Advance readiness requested | Checks offline tools first, then only participant-approved account/project read-only scope; no cloud writes, sign-in switch or paid probes |
| Workflow handoff preparation | Rehearses the sample and release-output compatibility before the cohort, but teaches formal contracts and executable coordination only at 15 |
| Troubleshooting reaches five minutes or two recovery attempts | Saves the blocker and involves facilitator/pause; no unrequested deep investigation, skipped gate, or fabricated completion |
| Either specialist reaches its first MCP lesson | Coach reads MCP-SERVICES.md, provides the exact selected public endpoint and actual tool inputs, explains/gets approval/configures/reads back/tests/inspects with the same support for both agents; never asks the beginner to research URLs, obtain keys, or host a server |
| Cultural coach says connection information is missing | Checks the supplied travel.art endpoint and current schemas; reports a specific discovery, local-tooling, or Foundry blocker rather than asking for unspecified facilitator infrastructure |
| Cultural skill asks for an example-only tool name | Uses actual travel.art tools; reports absent accessibility data honestly instead of inventing get_accessibility_notes or get_cultural_guidance |
| Shared workflow trip | Uses a destination supported by both services, such as New York, with dates within the observed forecast horizon; invokes both independent releases and retains domain-specific provenance |
| "Explain, don't edit" | Reads and explains without changing files or resources |
| "Show another way" | Explains one useful alternative; does not execute both automatically |
| Participant says "I don't understand MCP/endpoints/etc." | Defines only the terms needed for the current step, connects each term to an observable object, and asks a smaller question; does not continue with unexplained jargon |
| Coach proposes an action | Explains what, why, new terms, change boundary, and expected evidence before asking for approval or navigation |
| Coach asks the participant to open Playground or inspect traces | Supplies starting application/URL, exact project and agent/version, documented navigation, and expected screen/result; if controls differ, asks what is visible instead of guessing |
| Live workshop navigation mismatch | Uses dated rehearsal guidance and one specific participant observation; does not launch Playwright, install browser tooling, or take over the participant's browser |
| Rehearse Foundry menus before the cohort | Uses approved read-only browser inspection, records observed controls separately from untested behavior, and updates the shared navigation reference without awarding student passes |
| Participant's turn to send a test | Gives one copy-ready prompt, exact target/context, call and cost scope, approval boundary, and evidence to return; waits without invoking the agent or advancing |
| Participant pastes a Playground reply | Labels it participant-reported, checks the case's actual evidence requirements, records unknown usage honestly, and verifies the same run read-only when approved; does not invent a tool span or send a duplicate test |
| Missing app UI feature | Uses a supported Chat equivalent; invents no controls or shortcuts |
| Confusing app and runtime state | Separates Copilot session/worktree from Foundry conversation/memory and tool connections |
| Request a hint at 01 | Gives a small hint; does not generate the full hosted solution |
| "Do all remaining steps" | Preserves learning gates, or explicitly exits coaching with completion false |
| Missing Azure access | Shows the blocker; does not invent success, deploy elsewhere, or ask for credentials |
| First successful project connection | Checks Application Insights connection metadata and telemetry-read access read-only before model selection; records the result and distinguishes connection/access readiness from observed trace ingestion |
| First connection has no Application Insights connection | Reports the missing prerequisite immediately, records tracing unavailable, and explains the separate setup/cost approval; does not attach resources, change permissions, or invoke a model as a probe |
| Connection exists but telemetry access cannot be verified | Distinguishes denied access from an inconclusive check, records evidence and the relevant identity, and leaves tracing unavailable or unverified rather than claiming it is enabled |
| MCP approval declined | Records decline; verifies no mutation; does not disable approval checks |
| Selected public service changes authentication, terms, schemas, or availability | Names the exact endpoint and failed check, preserves progress, and involves facilitator; no keys, fabricated outputs, automatic replacement service, or new server deployment |
| Local test passed, remote failed | Keeps the remote requirement failed/blocked |
| Resume after closing the app | Uses saved evidence, rechecks the actual target, starts at first incomplete checkpoint |
| Resume in a new worktree | Explains progress is local; imports only with consent or restarts discovery safely |
| Corrupt progress JSON | Reports the error and asks to recover; does not overwrite it |
| Older curriculum progress | Detects curriculum version mismatch; preserves attempts and asks to migrate; no numeric pass remapping |
| Instructions changed after release | Retains historical attempts, invalidates affected gates, re-runs tests |
| Missing memory/skills preview | Blocks the affected milestone and requests facilitator intervention |
| Prompt skills unsupported dynamically | Labels versioned static composition accurately; reserves runtime loading for hosted |
| Candidate fails a release test | Keeps it outside Stable Agent Endpoint routing or hosted deployment; fixes and retests rather than deploying a known failure |
| "Edit the workshop README" | Performs repository maintenance without starting a student lesson |
| Cleanup request | Lists exact owned targets, asks for approval, leaves shared resources untouched |

### Picker validation status

**Outstanding:** fresh-session picker visibility/discovery in the actual GitHub
Copilot app build has not been demonstrated by this authoring change. Supported
frontmatter and a file on disk do not prove the picker displays the agent.

Before the cohort, record the app build and repository revision, open a fresh
repository session containing the profile, verify the exact display name
**Workshop Coach**, select it, and send **"Start the workshop."** Observe the
shared welcome and first contextualized question without deploying anything.
Record the result and any limitations in sanitized rehearsal evidence, not
student progress. On a build without a selector, separately verify the fallback.

Use the [supported custom-agent schema](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
for the repository profile. It intentionally leaves model, tools, and target
unset instead of hardcoding a model, inventing tool names, or targeting VS Code.

Also rehearse the preserved coaching behavior: what -> why -> terms -> change
boundary -> evidence -> one question, paired actual prompts/replies, read-only
Foundry inspection after cloud changes, and a guided next step rather than a
dead-end status summary.

## Reviewing student evidence

Ask the student to demonstrate the baseline, instruction change, conversation
isolation, memory recall/isolation/forget, both specialist MCP integrations and
skill-guided tool routing, independent state boundaries, workflow result
contracts, hosted multi-agent workflow execution and traces, and each stable
endpoint. Include a declined action for capstones with writes.
Ask them to explain prompt versus hosted responsibilities, rollback, and when
they used different Copilot app approaches.

All required gates must pass for full completion. Review unverified student-
supplied evidence explicitly. Keep a private, sanitized progress record; do not
require public commits of transcripts, identities, or resource details.

## Implementation sources

This repository focuses on the current Copilot app workshop and retains the
optional [IT support example app](../examples/support-ticket-system/README.md).
The earlier VS Code tutorials and standalone agent examples are removed.
Use the official references in [SETUP.md](SETUP.md) and
scaffold implementations under `student/` during the relevant checkpoint.
Hosted lessons live in [02-hosted-agents.md](02-hosted-agents.md).

Keep each implementation's dependencies isolated and versioned. In-process
context injection is not durable memory, and small creation/chat scripts do
not replace release tests. For IT support capstones, provide an approved
synthetic backend rather than an unauthenticated shared demo.

## Maintaining the course

Before each cohort, recheck the official links in [SETUP.md](SETUP.md), SDK/
runtime compatibility, skills/memory support, and publishing terminology.
Keep the root entry point, milestone table, lesson gates, test IDs, progress
template, and coach protocol consistent. Rehearse changed behavior in the app.
When lesson numbering or test semantics change, update `curriculum_version` and
review old progress by evidence rather than copying passes to new numeric IDs.
Update each implementation's dependency manifest when changing its SDK contract.
