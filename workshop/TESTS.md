# Test cases and evidence

These are executable behavioral specifications, not precomputed passes or an
automated grading service. Never use the coach's own answer as the runtime result.

Case IDs in this document are internal references for coach planning and
validation records, not wording to present to students. Follow
[the learner-instruction rule](COACH.md#explain-what-and-why-before-every-step):
always supply the actual task or copy-ready prompt, purpose, location/context
and expected observation. Keep acceptance codes out of participant messages,
question dialogs, choices and prompts; do not merely add a gloss to the code
or ask the student to look it up.

## Run and judge

Before running a case, name its execution route: **Run from the GitHub Copilot app -
coach sends** or **Run in the Microsoft Foundry portal - participant sends**. Follow
COACH.md and APP-GUIDE.md for approvals, exact agent/version, conversation
context, navigation, and where to report results. Before sending, explain the
behavior each case isolates, why it matters now, the expected observable
result, and what it cannot prove. A batch can share this short explanation,
but identify the purpose of each case rather than just announce its ID.
For a portal-run case, wait
for the participant's report instead of also invoking the agent from the app.
Use [participant trust](COACH.md#supportive-coaching-and-participant-trust):
accept clear confirmation of routine manual completion or visible response
format and continue, without requiring screenshots, a full pasted exchange or
a duplicate check. Mark it participant-confirmed, not independently verified.
Portal inspection alone is not a test. Both routes require actual Foundry
runtime evidence, not the coach's predicted answer; missing usage is unknown.

At 07 and 16 there is also **Run in Microsoft Teams or Microsoft 365 Copilot -
participant sends**. Name the exact chosen surface and published app before
the test. CH01/CH02 require actual channel-originated requests, not a duplicate
coach or Playground call. Record these participant prompts by channel; never
add calls to rebalance the earlier demonstration/practice target.

Distribute required cases using the
[mixed test plan](APP-GUIDE.md#where-tests-and-exploration-happen); participant
Playground tests are normal practice, with a 50/50 target for coach-sent and
participant-sent prompts across each specialist's lessons. Track actual prompts
by route, allocate remaining suitable cases to balance them, and record any
capability or preference exception; never add duplicate calls for the ratio. For each
handoff, give a copy-ready prompt and explain the expected observation.
Ask for the actual reply or identifiers only when a specific assertion or
requested review needs them. Record route and provenance:
participant-pasted output is participant-reported until corroborated. It does
not alone prove tool execution, Conversation linkage, memory isolation, or
consumer-endpoint invocation. Inspect the same run read-only within approved
scope when needed; otherwise keep that requirement incomplete. Deduplicate
usage by response identifier and label unavailable participant-run usage unknown.

Record actual target/version, configuration and skill version, input, output,
timestamp, and relevant trace/tool/store evidence. Use live positive integration
tests; controlled test doubles can demonstrate failures only when clearly
labeled. Do not break shared services for testing.

Run previously applicable cases using the stage-aware matrix below after a
capability change. A known-failing
candidate must remain outside Stable Agent Endpoint routing. A successful build,
deployment command, or plausible answer is not a pass.

Keep the [core agenda](FACILITATOR.md#five-to-six-hour-core-agenda) by reducing
repeated teaching, not test coverage. Group coach-side regression checks within
an explicitly approved current-step case/request limit and summarize their
meaningful results together. Reuse valid unchanged evidence for the same
retained target/version rather than rerunning it just for a demonstration.
Agent 2 still needs its own actual tests, but not a second full tutorial or a
new quiz after each result. One demonstrated understanding check per checkpoint
is sufficient; do not waive required runtime or release evidence.

At module close, connect actual paired results to what was learned and name
any unproven assertion before the next checkpoint; "all green" is not a learning
summary. Use COACH.md's scoped test approvals: unchanged covered tests need no
repeated per-call cost approval, but tool decisions, resource changes,
explicit participant restrictions and learning gates remain separate.
Retain available tokens; price lookups and money calculations are not required.

### Offline coaching rehearsal

These are protocol checks for facilitator preparation, not Microsoft Foundry
runtime passes. Rehearse with synthetic targets/usage and no cloud calls:

| Situation | Required coach behavior |
|-----------|-------------------------|
| Only the repository instructions or Workshop Coach profile are initially loaded | Follow AGENTS.md's request routing; load START.md for orientation or COACH.md before teaching, not every linked reference; reuse unchanged loaded guidance; missing required guidance blocks teaching rather than triggering an improvised protocol |
| Enter/resume a module; start its tests | State stage/checkpoint, goal, short plan and boundary; give the actual action or copy-ready prompt, its purpose, where/context and expected result, not an acceptance-case ID |
| Coach planning uses B01/B02 or another acceptance ID | Translates it into complete plain-language student instructions and approval choices; codes stay in internal records, even if a short definition could be attached; the student can act without consulting TESTS.md |
| Coach asks a student to act, decide or report a result | Uses a short plain-text question saying exactly what is required, with descriptive choices when useful; explanation and navigation come first, not codes, headings, field-label templates or test-checklist wording inside the question |
| Finish a module | Relate actual results to learning, name gaps, use the existing single understanding gate or an explanation already demonstrating it, then offer the next checkpoint or pause |
| Student gets stuck or asks about technology | Respond warmly and patiently, explain with a concrete example and help with the next small action; no blame, proof demand or extra quiz |
| Student confirms a routine Microsoft Foundry manual step is done and looks correct | Accept it, mark it participant-confirmed in chat and move on; no default screenshot, full reply, IDs or duplicate coach inspection |
| Default route reaches 06/13, release, channels or core completion | Briefly note memory is deferred, continue 05 -> 07 or 12 -> 14 without a skip question or memory operations, and omit memory-only gates for memory-free candidates; report completion of the memory-deferred route, never an M pass |
| Participant asks to add memory later or resumes with memory already attached | Obtain explicit scope/configuration/data/cost approvals for additions, run retained memory and affected downstream tests; preserve existing resources/evidence and do not silently disable memory |
| Coach explains an agreed manual creation/configuration step and student replies "created", "done" or "finished" | Accept the reply as completion of that action and continue; do not repeat the write, demand "looks as expected", or request a proof package. Obtain a service-returned identifier only when the next operation needs it; separate required runtime/identity assertions remain unchanged |
| Student report concerns a specific required identity, permission, isolation, runtime, release or channel assertion | Ask only for that assertion's needed evidence or inspect the same run within approved read-only scope; preserve provenance and uncertainty, not another paid call or an invented independent pass |
| Enter checkpoint 16 | Explain that this is the final core checkpoint, including release/update and channel requirements; 17-19 are optional |
| All core gates pass, including CH01/CH02 | Proactively announce core completion and provide the evidence-based handoff; do not wait for "are we done?" or automatically start the capstone |
| Participant stops at 16 with blocked or skipped requirements | Explicitly announce partial completion, list the actual gaps, keep `completed` false, and distinguish unfinished checks from additional lessons |
| Participant resumes after a full or partial end-of-core message | Lead with saved status and the agreed route; do not restart completed lessons, repeat checks for closure, or silently start optional 17-19 |
| Participant answers setup/preferences or finishes/pauses a checkpoint | Reuse the chat input and normal closing reply; no progress.json read/write, replacement per-turn ledger or whole-history scan |
| New/resumed chat has earlier context but a stale legacy progress.json exists | Use the latest explicit chat choices; leave the legacy file untouched unless import/export is explicitly requested |
| Earlier input or exact approval is missing after context loss | Retrieve only the needed history or ask for the missing fact; do not invent approval, infer execution from a summary or restart the welcome |
| A cloud operation was interrupted and chat has no confirmed result | Keep the outcome/usage uncertain, inspect that operation's execution evidence and remote state read-only; do not retry based on a reconstructed progress claim |
| Next test is unchanged and covered by an explicit scoped approval | Verify its cases, target/version, input/history scope and execution limits; proceed without a price lookup, calculation or repeated per-call approval; retain the runner's exact approval reference |
| Usage is missing or a call is interrupted | Mark tokens unknown, not zero; reconcile only within approved read-only scope and never repeat a paid call just for token totals |
| Hosted workflow lacks prices or an aggregate internal-input/memory cost estimate | Do not block solely on that missing calculation; require the approved case, supported execution limits, runtime safety and actual tool decisions; do not claim a billing cap |
| Checkpoint or workshop token summary includes cached input, linked traces and specialist results | Count cached input as a reported subset, deduplicate response IDs and avoid adding parent aggregates to the same specialist usage; retain available model/version and route metadata |
| Participant asks for money spent at the end | Estimate only on request using observed tokens and matched official rates; mark missing usage and excluded charges, distinguish an estimate from the Azure bill; unavailable pricing does not invalidate completion |
| SDK exposes a tool-limit parameter but the managed route's enforcement/coverage is unverified | Do not attach it or claim a cost cap; preserve the released configuration and name the facilitator-readiness gap |
| Approval terms expire, cases exceed the agreed limit or scope/resources change | Stop before another call and obtain a new scoped decision; do not turn this into a mandatory price calculation |
| Participant explicitly imposes a monetary restriction | Honor it; if compliance cannot be established, pause the affected action and clarify, never claim a billing cap or silently discard the restriction |
| Pending MCP approval or proposed resource/identity change | Treat it separately from spending permission; never batch past a pending tool decision or bypass the runner |
| Direct MCP configuration saves, but no runtime call or permission choice is observed | Keep the integration gate incomplete; require the actual tool/arguments, participant's native permission choice and correlated execution evidence |
| First useful tool request in the specialist Playground | Explain Approve, Deny and Auto approve when the prompt appears; participant selects Auto approve for the displayed permitted-tool scope, then reviews the answer and trace; no standalone connectivity test or separate denial drill |
| Auto approve is reported or selected in the Playground | Record the actual scope and observed behavior; do not infer SDK/runner, endpoint, hosted-workflow or channel permission, a saved `never` policy, or persistence across chats/versions |

## Checkpoint execution matrix

The default route follows the [temporary memory deferral](README.md#temporary-memory-deferral).
Skip 06/13 and M01-M03 without awarding passes. For memory-free candidates,
omit M coverage and post-memory D variants from all later regressions,
release and channel gates; ordinary Conversation and identity isolation tests
remain required. Existing memory-enabled candidates retain their applicable
checks until a separately approved configuration change. Adding memory later
requires the retained tests and affected path regressions.

Plan the following required coverage before asking for the step's approval.
A case may satisfy several assertions in one exchange: label each assertion
and its evidence rather than send duplicate prompts. A batch is an explicitly
approved collection of checks on the **current candidate**, not authorization
for future lessons, tool approvals or retries. Use the
[shared runner](runner/README.md) for its supported operations.

Treat the regression column as required **coverage**, not an instruction to
send every historical prompt again. Before the batch, match each assertion to
its candidate/version, configuration and dependencies, actual execution path,
identity and Conversation/memory scope. Reuse an existing pass only when all
relevant dimensions remain valid; execute missing or invalidated coverage.
No new version or capability change does not by itself invalidate unrelated
evidence. New consumer/channel paths and changed authorization or state still
need their own affected checks. Keep release suites complete on the actual
final version/path; never infer a channel pass from project tests.

| Checkpoints | Required new behavior | Regression on the current candidate |
|-------------|-----------------------|-------------------------------------|
| 01, 08 | B01-B02, one fresh context per input | None; save exact baseline prompts, replies, target, version and route |
| 02, 09 | I01: same two inputs, required headings | These same two after-change exchanges also satisfy B01-B02; compare with saved baseline evidence, not two new before-change calls |
| 03, 10 | D01 two turns in Conversation A; D02 dependent follow-up in new Conversation B | B01-B02/I01 coverage: reuse valid evidence on the unchanged version/path/scope; run only missing or invalidated checks if Conversation invocation changes that path or scope. B02 can share D02 when exact input/assertions match |
| 04, 11 | T01 direct one-tool binding; participant-sent C01 or C02 first-tool request, permission choice and trace; C03a | B01-B02/I01 and D01-D02; no separate denial drill, memory or later skill tests yet |
| 05, 12 | T02 four-tool direct allowlist and unchanged server; S01 or S02 routing/provenance and partial failure, shared with C03b | B01-B02/I01, D01-D02, C01R or C02R and C03a; a skill scenario may also satisfy a matching forecast/museum regression |
| 06, 13 | Temporarily deferred; no memory setup or M01-M03 on the default route | Continue 05 -> 07 and 12 -> 14; retained tests apply only when memory is explicitly reintroduced or already configured |
| 07 | T03 final Weather direct binding; P01-P03, then CH01 channel publication/use before 08 | Full applicable B/I/D/C/S/M coverage on the final direct-MCP candidate/path, counted once; new channel-path access/approval/isolation evidence cannot be inferred from endpoint tests |
| 14 | T03 final Cultural direct binding and two-domain isolation; Cultural P01-P03 and two-specialist comparison | Full applicable Cultural B/I/D/C/S/M coverage; verify unchanged Weather release, publication and dependencies and reuse valid evidence, not a second Weather suite or publication |
| 15 | G01-G03 and W01-W03: local fixtures for validation/failure branches and approved live calls to both released specialists | Specialist release evidence must match the versions invoked; no specialist rewrite or full rerun merely to scaffold the workflow |
| 16 | W01-W04 and P01-P04 remotely, then CH02 on the final selected workflow version; retain pre-release evidence and a known-good recovery target | Full applicable G/W behavior on the final hosted version and consumer path; W04 requires the actual portal; CH02 must originate in the chosen channel; reuse overlapping assertions on the same run |

Prior results can be reused only for the **same retained version, configuration,
execution path and relevant identity/scope**. A new version needs its applicable
regressions; an older pass is not a pass for the new version. Release checks
through a different consumer path cannot reuse project-Playground results as
consumer evidence. Do not duplicate an exact final-version/path test just
because it appears under both feature and release headings.

Stage variants resolve capability changes without dropping assertions:

- **C01/C02 first-tool milestone:** the single-tool allowlist is required at
  04/11. Preserve that historical evidence on its retained version.
  **C01R/C02R later regression:** verify the current reviewed allowlist, then
  prove the relevant forecast/museum tool executes with valid inputs, returns
  grounded evidence, and has corresponding trace linkage. Do not shrink a
  four-tool configuration back to one tool merely to repeat the first lesson.
  Supplied forecast coordinates should not trigger unnecessary geocoding.
- **D01/D02 after memory:** use an authorized synthetic scope with no stored
  destination/referent, verified through the supported memory API. Retain the
  same-versus-fresh Conversation and no-history-replay assertions. A consented
  unit/activity preference is not destination context. Do not disable shared
  memory, erase real preferences, or let a prompt choose its security scope.
  If a clean scope cannot be established, keep the test blocked.
- **C03a at 04/11:** unsupported/malformed input with no invented result.
  **C03b at 05/12:** controlled failure with explicit attribution and no
  invented result, shared with the skill's partial-failure case rather than
  another first-use exercise. Label an isolated fixture or actual provider
  error accurately. Explain Deny in the first-use permission prompt without a
  separate specialist denial test. If a participant actually declines a call,
  preserve it as permission denial, not an upstream outage or proof of every
  partial-failure mode.

Use the lesson's exact saved inputs for B/I comparisons. For S01/S02, list
the chosen supported location/date, tool needs, ambiguous input, no-tool case
and controlled partial failure before execution. Use approved fixed inputs
and service schemas; do not invent output or call counts before observing
the tool requests. Budget the initial model requests separately from exact
tool approvals/continuations. Never batch past a pending approval.

## Baseline and instructions

| ID | Input/procedure | Pass conditions |
|----|-----------------|-----------------|
| B01 | Ask one stable domain question in a fresh Conversation | Correct, concise answer; trained knowledge labeled accurately; no false tool or system-access claim |
| B02 | Ask a follow-up with missing destination or referent in a new empty Conversation | Requests context rather than pretending to know it |
| I01 | Compare the same B01-B02 inputs before and after adding the required response headings | Headings appear; general knowledge is not mislabeled as retrieved evidence; missing verification is acknowledged; baseline behavior does not regress |

Use `Answer`, `Source`, and `Uncertainty` for Weather and `Guidance`, `Source`,
and `Uncertainty` for Cultural Travel.

## Microsoft Foundry-managed Conversation behavior

Before running checkpoint 03 or 10 tests, verify the
[portal trace prerequisite](SETUP.md#portal-trace-prerequisite): the exact
project's Application Insights connection and the inspection identity's
telemetry-read access. D01-D02 runtime evidence can pass independently of
tracing, but a missing trace connection or access leaves the required portal
inspection blocked and the checkpoint incomplete. Preserve those runtime
results; do not repeat model calls or change telemetry setup without approval.
After an approved setup change, do not assume historical traces are backfilled.

| ID | Input/procedure | Pass conditions |
|----|-----------------|-----------------|
| D01 | Provide destination/context, then ask a dependent follow-up in the same Conversation; capture its identifier | Context is retained; the same Conversation identifier is reused; no custom history store is implemented |
| D02 | Ask the dependent follow-up in a newly created Conversation before memory is attached | Missing context is requested; identifiers differ; history is not replayed or shared globally |

Run D01-D02 independently for each specialist. A GitHub Copilot app session is
unrelated to these runtime identifiers.

For example, explain **before testing** why context changes the meaning of
"What about there tomorrow?":

| Context | Purpose and expected observation | Does not prove |
|---------|----------------------------------|----------------|
| Fresh empty Conversation (B02/D02) | No location/referent has been supplied, so the agent should ask where "there" means rather than guess | Retained context or live weather |
| Same managed Conversation after a Stockholm turn (D01) | Reusing the service-returned Conversation ID should let the agent resolve "there" to Stockholm without replaying history | Live weather, persistent memory, or isolation by itself |

These are illustrative expectations, not precomputed passes. Use the same
saved prompt for comparisons and inspect the actual reply and identifiers.
At checkpoint 03 no weather tool is attached: contextual understanding is not
a verified forecast. C01 later needs the Weather MCP server's
`weather_forecast` invocation, source/result and trace evidence.

## Persistent memory

**Retained for later, not run on the default memory-deferred route.** These
tests do not block that route's completion and must not be marked passed
without execution. See the [deferral policy](README.md#temporary-memory-deferral).

| ID | Input/procedure | Pass conditions |
|----|-----------------|-----------------|
| M01 | With explicit consent, store a low-risk preference; verify it in a new Conversation under the same trusted scope | Stored fact, provenance, and recall agree; Conversation history is not replayed |
| M02 | Correct the preference and test another authorized synthetic identity/scope | Updated value is used; no cross-user recall or chat-selected identity spoofing |
| M03 | Delete the preference, then test another fresh Conversation | Removed value is no longer applied; deletion is scoped and observable |

Use a Celsius preference for Weather and a low-risk activity preference for
Cultural Travel. Memory supplies preferences; MCP tools supply external facts.

## Remote MCP

Use the exact endpoints, actual schemas, and examples in
[MCP-SERVICES.md](MCP-SERVICES.md). The coach provides connection details for
both specialists; participants do not select or host the services. Resolve
tool metadata needed for configuration within the approved work and attach
only the current approved allowlist. Do not add a standalone reachability test;
use the first useful agent request for runtime evidence. Local discovery is
not Microsoft Foundry runtime evidence.

## Foundry tool management

Follow [Direct MCP connections](MCP-CONNECTIONS.md) for the current supported
route, approval boundaries, identity checks and candidate versioning.
These assertions supplement C/S/P, not replace them. Use the same approved
runtime exchanges for overlapping assertions; read-back and discovery checks
do not require extra model prompts.
In v10, T01 covers each specialist's first direct binding at 04/11, T02 its
four-tool expansion at 05/12, and T03 final binding/isolation at 07/14.
These replace the older Toolbox-specific meanings; do not reinterpret
historical T01-T03 passes without an agreed migration and matching evidence.
Future-stage assertions do not block an earlier milestone, and a first-tool
pass does not automatically pass the later expansion.

| ID | Input/procedure | Pass conditions |
|----|-----------------|-----------------|
| T01 | At 04 attach Weather's public MCP URL directly with only `weather_forecast`; independently repeat at 11 for travel.art with only `find_museum_guide` | Exact URL/label, agent version, one-tool allowlist and `require_approval: "always"` read back; no credentials or authentication connection; participant's first-use Playground permission choice, displayed scope and actual runtime call correlated with C01/C02; only the selected operation is callable; no separate denial drill |
| T02 | At 05/12 expand that specialist's direct allowlist to its four approved tools and add its reviewed skill | Same public server URL/label retained; current schemas and exact allowed names verified; other domain/unselected tools not callable; native per-call approval retained; S01/S02 shows appropriate selection, restraint, sources and partial failure |
| T03 | At 07 verify Weather's final direct binding; at 14 verify Cultural's final binding, unchanged Weather release/dependencies and two-domain isolation | Exact released candidate/server/allowlist/skill recorded; final-path permission, runtime and P01-P03 evidence match; each specialist invokes only its own permitted tools; portal Auto approve is not evidence of permission on a different path; reuse valid unchanged Weather evidence, with no planned migration/re-release |

Record actual upstream names, server URL/label, candidate version,
arguments/results, runtime context and response/trace linkage. A successful
tool listing alone does not prove which operation executed.
Verify excluded tools through supported read-only authorization/configuration
inspection, not an extra participant denial exercise or an unauthorized
upstream action. Instructions saying
"ignore other tools" are not access control. The public server may advertise
more tools than the agent is permitted to call; do not equate server discovery
with the effective agent allowlist.

Changing the direct binding, allowlist or upstream behavior invalidates
affected current-path evidence even if instructions are unchanged. Missing
runtime access, unsupported native approval or unsafe restrictions block
the affected gate. Read-back of `"always"` alone does not establish the
participant's permission choice or successful tool execution. Follow
[the first-use Playground flow](APP-GUIDE.md#first-tool-use-in-the-playground);
record the actual displayed scope, participant choice and correlated result.
SDK/runner pending requests still need exact decisions and continuations.

### MCP behavior cases

| ID | Input/procedure | Pass conditions |
|----|-----------------|-----------------|
| C01 | With only the verified Weather MCP forecast tool allowlisted, ask one supported weather question | Runtime tool call, validated arguments, result, upstream provenance/timestamp, grounded answer, and a guided Microsoft Foundry trace inspection of the tool span |
| C02 | With only travel.art `find_museum_guide` allowlisted, ask one supported museum question, such as the Metropolitan Museum of Art in New York | Runtime tool call, validated arguments, returned guide attribution/URL, available verification date, grounded answer, and corresponding tool span; no weather claim or invented dataset version |
| C03 | At 04/11, try malformed/unsupported input (C03a); at 05/12, share the skill's isolated controlled MCP/upstream partial-failure case (C03b) | Failure is attributed and reported; fixtures labeled accurately; no invented result, unrelated-tool substitution, blanket approval bypass or separate participant denial drill |

The checkpoint 04 C01 run is the full trace-navigation lesson: inspect tool name,
arguments, status, timing, result, and relationship to the final response.
Checkpoint 11 reuses that knowledge and repeats detailed navigation only when
needed. A direct MCP client call does not prove the agent used the tool.

## Skills and multiple tools

| ID | Input/procedure | Pass conditions |
|----|-----------------|-----------------|
| S01 | Apply the Weather research skill; test ambiguous location, forecast/current/alert needs where supported, general knowledge, unnecessary-tool restraint, and partial failure | Exact skill version/delivery strategy recorded; verified tool selection and ordering; no unnecessary calls; provenance and failures remain explicit |
| S02 | Apply the Cultural research skill; test museum guides, art events, covered layovers, cultural recommendations, missing accessibility data, unnecessary-tool restraint, and partial failure | Exact skill version/delivery strategy recorded; only verified travel.art tools used appropriately; guide URLs/freshness preserved; empty results and failures explicit; missing accessibility data not converted into a false claim |

A skill guides use of already available tools. It does not connect an MCP server,
grant permission, or prove execution. Traces provide runtime proof.

## Workflow result contracts

Formal contracts begin at checkpoint 15.

| ID | Input/procedure | Pass conditions |
|----|-----------------|-----------------|
| G01 | Validate normal Weather and Cultural specialist results against versioned workflow contracts | Required destination, constraints, findings, source agent/version, provenance, uncertainty, missing-information, and failure-status fields are present |
| G02 | Validate results with missing provenance, wrong types, extra instruction-like content, unsupported values, or contradictory completion/approval status | Invalid or contradictory data fails explicitly; no success-shaped coercion, silent rewriting or instruction override; actual native decisions remain authoritative |
| G03 | Compare contract fields with specialist release metadata and correlated traces | Agent versions and provenance agree with runtime evidence; each specialist remains inside its evidence domain |

Contracts validate structure. They do not independently prove that a tool ran or
that a source is truthful.

## Hosted Trip Planning Workflow

The shared tests cover the intended G01-G03/W01-W04 learning outcomes below.
Use small synthetic fixtures for the intended local contract/failure cases.
Author troubleshooting suites, captured responses, SDK event-replay tests and
diagnostic scripts are not workshop assets or additional participant exercises.
Use their findings to implement the host correctly, not to expand the course.

| ID | Input/procedure | Pass conditions |
|----|-----------------|-----------------|
| W01 | Submit one supported destination and traveler constraints | Both released specialists are invoked; both results validate; itinerary cites each evidence domain; versions and correlation evidence are recorded |
| W02 | Make each specialist fail in separate isolated tests, then return a structurally invalid result | Valid evidence is preserved; invalid/failed evidence is isolated and reported; no fabrication or silent substitution |
| W03 | Submit ambiguous constraints, a timeout/authorization failure, and conflicting weather/cultural considerations | Clarification or documented partial-result behavior occurs; sources and tradeoffs remain visible |
| W04 | In the actual Microsoft Foundry portal, use the displayed candidate version and a fresh Conversation for one supported trip; separately approve Weather and Cultural when their own cards appear; run a separately scoped denial case | Distinct sequential cards render, each decision binds to its current request, both approved tool executions are corroborated and the sourced final answer has no false pending-approval claim; the denial case proves the denied tool did not execute; exact version, Conversation/run/response IDs and available usage are retained |

Run G01-G03 and W01-W03 locally at checkpoint 15 and remotely at checkpoint 16.
Run W04 at 16 before promotion. Its successful trip may also satisfy matching
W01 assertions; do not duplicate calls for labels. The facilitator prepares
the same intended cases before the cohort with approved spend and tool decisions.
Two manual specialist calls followed by a manually written itinerary do not pass.
A custom-client success does not pass the required portal case.

### Repeat the Playground behavior in the destination

After the Playground baseline passes, repeat the applicable W01-W04 behavior
cases through the chosen Microsoft Teams or Microsoft Copilot Studio route
using [the destination parity plan](PUBLISHING.md#workflow-destination-test-parity).
Keep exact workflow/specialist versions, supported inputs and assertions
matched, with fresh context where the original case required it. Record the
actual route for each result; do not relabel a Playground execution as a
destination pass. Separate native decisions, denial/no-execution, source and
uncertainty, state isolation and explicit failure behavior must remain intact.
Channel rendering can differ; behavioral correctness cannot.

A Microsoft Copilot Studio test-pane pass is integration evidence, not CH02
channel evidence. A subsequent published Microsoft Teams/Microsoft 365 Copilot
run may satisfy both matching workflow parity assertions and CH02 without
duplicate calls. Missing destination behavior stays blocked rather than being
silently waived because it passed in Microsoft Foundry.

## Consumer endpoint and release

| ID | Input/procedure | Pass conditions |
|----|-----------------|-----------------|
| P01 | Discover the Stable Agent Endpoint, select the fully tested version, and invoke through an approved consumer | Successful response; exact endpoint/version recorded; not project-playground-only |
| P02 | Invoke as a valid identity without access, then as the approved consumer | Boundary denies the former and allows the latter; no broad permissions added |
| P03 | Run all applicable feature tests through the consumer path | Tools, Conversations, memory, skill delivery, errors, identity, and downstream access still behave as tested |
| P04 | Promote a fully passing update, invoke it, and verify the previous known-good version remains an available documented recovery target | Stable endpoint remains unchanged; metadata and behavior prove the update; recovery target and procedure are verified without routing traffic to a known-failing version |

At 07, P03 covers Weather B, I, D, C01R/C03, and S01.
At 14, repeat Cultural B, I, D, C02R/C03, and S02.
Only when memory is configured, use post-memory D and add the M tests.
Retain the original single-tool C01/C02 milestone evidence separately.
At 16 add G and W tests.
At 19 use the capstone equivalents.

Failed candidate tests are retained for diagnosis, but a known-failing candidate
is never promoted or deployed as the stable release. Execute rollback only for
an unforeseen problem discovered after a fully passing candidate was promoted;
otherwise P04 verifies recovery readiness without changing stable routing back.

## Microsoft Teams and Microsoft 365 Copilot publication

Follow [PUBLISHING.md](PUBLISHING.md#required-channel-publication-at-07-and-16).
At least one participant-chosen surface is required for each milestone; if
both are chosen, record each separately. Cultural's channel publication is
not required. Do not equate release P01-P04 with channel CH01/CH02.

| ID | Input/procedure | Pass conditions |
|----|-----------------|-----------------|
| CH01 | At 07 publish the tested Weather release to the approved Microsoft Teams and/or Microsoft 365 Copilot surface; participant sends a supported weather request there | Approved audience, channel identity, app/registration and pinned active version verified; actual channel reply with weather provenance and uncertainty; same-run service/trace linkage proves the released Weather agent and permitted MCP tools executed; channel-specific access, trusted Conversation/memory isolation and actual approval/denial verified; direct endpoint remains usable; all chosen surfaces have evidence before 08 |
| CH02 | At 16 publish the final released hosted workflow; participant sends a supported trip request from the chosen surface and inspects the same execution | Approved app/channel maps to the workflow stable endpoint/version, not a worker; channel reply contains a sourced itinerary with uncertainty; correlated request, both released specialist invocations, result validation and aggregation are observed; identity mapping, downstream access and per-call approval remain effective; no manual worker calls, direct-tool shortcut or fabricated evidence; all chosen surfaces have evidence before core completion |

Before tests, approve exact prompts, supported location/dates, bounded model
requests, tool approval continuations, stored data and costs. Include a scoped
channel denial check and synthetic-user isolation verification; retain the
same security assertions when a channel requires a different supported client
or adapter. Do not grant roles, switch audience to organization-wide, or
disable approvals to manufacture a pass.
Use read-only metadata/access checks where sufficient and live execution for
runtime assertions. Reuse an exchange for overlapping assertions only when
target/version, actual channel, identity/scope and input match; no duplicate
call merely for another test label. A channel happy path may satisfy a matching
W01 assertion but not the complete W02/W03 suite.

Capture publication status, returned launch link/app identifiers, audience,
channel and tested version, exact input/reply or labeled safe excerpt,
timestamp, available response/Conversation/correlation identifiers, trace
linkage and known/unknown usage. Corroborate participant-reported output with
the actual run, not screenshots of an installed app. Native streaming/citation
cards are not promised; verify readable source attribution in the actual reply
and full provenance in execution evidence.
If permissions, tenant policy/licensing, protocol support, approval flow or
required linkage cannot be verified, keep CH01/CH02 and its checkpoint blocked.
Saved endpoint passes remain valid for their unchanged paths; an explicitly
approved partial route remains incomplete. Publication success or admin
approval alone never passes either channel test.

## Optional Weather delivery lab

This lab is outside numbered checkpoints and is not required for completion.
Its offline contracts live in `workshop/weather_delivery/`; run them with:

```text
python -S -m unittest discover -s workshop/weather_delivery -p "test_*.py" -v
```

| ID | Input/procedure | Pass conditions |
|----|-----------------|-----------------|
| WD01 | Capture a selected saved Dev version and inspect the generated PR | Exact Dev name/version and intended Prod name are recorded; definition hash matches; credential-like fields are rejected; capture reads Dev only |
| WD02 | Review the PR, handle workflow approval if GitHub requires it, and wait for the required offline check | Authorized participant reviews/approves the workflow using the displayed control or involves the owner; approval policy is not bypassed; trusted tests and package/hash validation pass on the current PR head; workflow approval is not deployment or tool approval; participant reviews the diff before merge |
| WD03 | Merge the PR, then manually dispatch deployment on the default branch with its full reviewed commit SHA and deployment confirmation | Merge alone does not deploy; unchecked confirmation and wrong commit fail before Azure login/write; confirmed matching commit proceeds without any GitHub Environment |
| WD04 | Read back the deployed Prod version and selector | Created or reused version definition matches the reviewed capture; stable endpoint selects that version; Dev remains unchanged; artifact records source and destination versions; reuse of identical configuration is not a changed-version rollout |
| WD05 | Finish with a guided manual basic-response test on the exact deployed Prod version under separate cost/storage approval | Record agent/version, actual prompt/reply and absence of tool calls; distinguish participant-reported from independently inspected evidence; portal behavior does not prove the consumer endpoint or Weather tools; if blocked or skipped, retain delivery results and mark runtime unverified |

Automated consumer-endpoint testing and live Weather tool tests are optional,
separately approved extensions, not new completion gates. The corrected helper
uses `?api-version=v1` on invocation only; offline coverage does not establish
prompt-agent runtime compatibility. A successful live rehearsal of that exact
route is still required before describing it as verified automation. Each actual
MCP call retains its separate approval/denial requirement.

The offline contract checks package shape, credential exclusion and hashes.
They are not an AI review or a Foundry runtime test. The workshop uses two
agents in one project as a teaching shortcut; model and project-level tool
dependencies, permissions, quotas and audit boundary remain shared. Live
rehearsal must independently verify OIDC, Foundry permissions, PR automation,
manual deployment confirmation, version creation and endpoint pinning.
MCP runtime execution and per-call approval remain separate gates.

## Capstone gates and optional mutations

| ID | Input/procedure | Pass conditions |
|----|-----------------|-----------------|
| K01 | Review the capstone brief before implementation | Participant explains two evidence domains, workflow need, scope/non-goals, tests, data/resource boundaries, and cost limits |
| K02 | Build each specialist one capability at a time and run adapted tests | Both specialists independently pass baseline, instructions, Conversations, MCP, skill, optional memory, and release gates |
| K03 | Demonstrate the hosted workflow normal and degraded paths and review the release handoff | G01-G03, W01-W03, and P01-P04 pass; participant explains traces, tradeoffs, limitations, and remaining resources |
| A01 | For a write action, decline one inspected attempt, verify unchanged state, then approve a separate attempt | No mutation on decline; exactly intended authorized mutation after approval |
| A02 | Try invalid input, nonexistent target, and isolated downstream failure | Explicit errors; no false success, duplicate mutation, or unapproved write |

A01-A02 are not required for read-only capstones. Never introduce real payments,
bookings, production tickets, or sensitive personal data.

## App practice evidence

At each checkpoint, record the technique tried, one alternative discussed, and
the participant's explanation of when each helps. A Chat equivalent is
sufficient if a UI feature is unavailable.
