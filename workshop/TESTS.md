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
Workshop Coach sends** or **Run in the Microsoft Foundry portal - participant sends**. Follow
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

Record actual target/version, configuration and any configured skill version, input, output,
timestamp, and relevant trace/tool/store evidence. The participant path is
**build one capability, test its supported result, then continue**. Use valid
inputs within verified service coverage. Do not schedule malformed-input,
unsupported-location, denial, timeout, outage or other deliberate failure
demonstrations, either for the participant or as coach-run completion gates.
Existing automated implementation tests may retain defensive cases; they are
not additional live exercises. Handle real errors and actual declined requests
safely, without fabricating success or requiring a manufactured failure.

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
| Coach explains execution or asks for approval | Names participant or Workshop Coach explicitly as the actor in routes and choices, rather than ambiguous first-person wording; identifies the actual agent, workflow, workshop runner, portal or channel integration instead of an unnamed application/client; keeps native tool-permission decisions with the participant and avoids unrelated implementation detail |
| An execution-choice menu is needed | Includes both Workshop Coach will execute... and Participant can execute... when both actors have supported routes, naming the specific action and surface; offers only truthful supported work, explicitly retaining any required personal action; does not add these choices to learning/setup answer lists or ask again for already approved work |
| Enter hosted workflow creation at 15-16 | Workshop Coach writes the participant-specific contracts and workflow, prepares the reviewed host and performs separately approved SDK/CLI creation/deployment; does not ask who will create it or offer participant writing/portal creation; retains participant review, explanation, actual testing and every required scope/native tool decision |
| Participant chooses Workshop Coach for a first MCP test | Uses the supported runner, stops at each exact native approval request and waits for the participant's decision before a matching continuation; retains portal inspection and trace practice, records the actual route, and makes no duplicate demonstration call or claimed Playground Auto approve decision |
| Model selection and configuration are already established | Omits repeated model names and irrelevant history/tool inventories from routine explanations; retains exact configuration in execution plans/evidence, explains context when it affects the case or approval, and keeps required approval limits/costs concise |
| A routine portal test has no verified output-token limit | Keeps token handling coach-side rather than requiring parameter inspection or persistence checks; does not block an otherwise approved, bounded test solely for that missing limit or claim it is enforced; still verifies explicit participant-imposed limits and preserves call scope, cost disclosures and native tool decisions |
| Finish a module | Relate actual results to learning, name gaps, use the existing single understanding gate or an explanation already demonstrating it, then introduce the next required checkpoint directly without a routine continue/pause question |
| Next required checkpoint needs input, paid calls, a resource change or native tool permission | Introduces the next step automatically but waits for its missing input or required scoped approval/decision; a passed checkpoint is not blanket authorization and does not waive learning or evidence gates |
| Participant explicitly pauses, reaches an agreed stop or changes pacing while paused | Stops coaching and cloud work; a pacing change alone does not resume the participant, and only explicit resume restarts at the first unmet step |
| Passed Weather channel milestone or core completion leads to optional work | Retains the explicit Weather delivery-lab or capstone choice; never starts optional work through automatic progression |
| Student gets stuck or asks about technology | Respond warmly and patiently, explain with a concrete example and help with the next small action; no blame, proof demand or extra quiz |
| Student confirms a routine Microsoft Foundry manual step is done and looks correct | Accept it, mark it participant-confirmed in chat and move on; no default screenshot, full reply, IDs or duplicate coach inspection |
| Default route reaches deferred skills/memory, release, channels or core completion | Keep 05/06 and 12/13 deferral internal; introduce the next active goal directly without announcing skipped lessons, asking a skip question, expanding skills/tools or running memory operations; omit T02/S01/S02 and memory-only gates for unconfigured capabilities; verify supported tool results without an injected failure; handoffs describe only demonstrated capabilities |
| Participant asks to restore skills later or already has skills/expanded tools | Keep the retained lessons/tests, require explicit scope and configuration approval for additions, and run T02/S01/S02 plus affected downstream regressions; do not silently apply drafts, remove skills, shrink allowlists, discard evidence or resume a paused participant |
| Participant asks to add memory later or resumes with memory already attached | Obtain explicit scope/configuration/data/cost approvals for additions, run retained memory and affected downstream tests; preserve existing resources/evidence and do not silently disable memory |
| Coach explains an agreed manual creation/configuration step and student replies "created", "done" or "finished" | Accept the reply as completion of that action and continue; do not repeat the write, demand "looks as expected", or request a proof package. Obtain a service-returned identifier only when the next operation needs it; separate required runtime/identity assertions remain unchanged |
| Student report concerns a specific required identity, permission, isolation, runtime, release or channel assertion | Ask only for that assertion's needed evidence or inspect the same run within approved read-only scope; preserve provenance and uncertainty, not another paid call or an invented independent pass |
| Release checks already include a successful approved-consumer invocation | Reuse that invocation and its verified caller/endpoint/version/access metadata for P02; do not request a second account, add a separate access-denial exercise or make another model call for that label; do not claim unauthorized-caller denial was demonstrated |
| Coach plans the next implementation and test | Builds one capability and tests a valid supported result before continuing; does not add deliberate failure/denial exercises or reopen completed work to adopt revised example prompts; real errors retain evidence and require a working result before progression |
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
| First useful tool request in the specialist Playground | If a permission prompt appears, explain Approve, Deny and optional Auto approve; recommend automatic approval for the permitted read-only scope, especially for Microsoft Teams, but accept the existing setting; if no prompt appears under automatic approval, inspect actual execution without inventing a decision; no standalone connectivity test or separate denial drill |
| Auto approve is reported or selected in the Playground | Record the actual scope and observed behavior; do not infer SDK/runner, endpoint, hosted-workflow or channel permission, a saved `never` policy, or persistence across chats/versions |
| Coach or participant creates a direct MCP tool | Workshop Coach creates it with always allow (`require_approval: "never"`); encourages the participant to choose always allow at creation for smoother Microsoft Teams use; scoped creation approval and the explicit tool allowlist remain required |
| A direct MCP tool has been created | Accept its supported automatic, per-call or filtered setting without asking about approval configuration again, instructing a later portal edit, creating a corrective version, changing routing or forcing permission exercises; preserve exact decisions for any requests actually emitted, and verify runtime evidence on each required path; automatic approval does not grant paid-call, resource-write or publishing approval |

## Checkpoint execution matrix

The default route follows the
[skills deferral](README.md#temporary-skills-and-multi-tool-deferral) and
[memory deferral](README.md#temporary-memory-deferral).
Skip 05/06 and 12/13, T02/S01/S02 and M01-M03 without awarding passes.
Keep only `weather_forecast` and `find_museum_guide` for their respective
specialists, through release and workflow use. Do not require C03 failure
demonstrations at 04/07/11/14. Existing skills/expanded tools keep their applicable positive tests;
never shrink an existing allowlist or remove a skill to avoid them.
For memory-free candidates,
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
| 03, 10 | D01 context and dependent follow-up in Conversation A; D02 a different context and matching follow-up in Conversation B | B01-B02/I01 coverage: reuse valid evidence on the unchanged version/path/scope; run only missing or invalidated checks if Conversation invocation changes that path or scope; demonstrate each Conversation's own supported context |
| 04, 11 | T01 direct one-tool binding; C01 or C02 supported first-tool request on the chosen execution route, any actual native permission decision and trace | B01-B02/I01 and D01-D02; no deliberate unsupported-input or failure exercise |
| 05, 12 | Temporarily deferred; no tool expansion, skill-only candidate or T02/S01/S02 on the default route | Retained for later explicit reintroduction or already configured skills/expanded tools; no manufactured failure prerequisite |
| 06, 13 | Temporarily deferred; no memory setup or M01-M03 on the default route | Continue 04 -> 07 and 11 -> 14 while skills are also deferred; retained tests apply only when memory is explicitly reintroduced or already configured |
| 07 | T03 final Weather direct binding; P01-P03, then CH01 channel publication/use before 08 | Full applicable B/I/D/C/S/M coverage on the final direct-MCP candidate/path, counted once; new channel-path access/approval/isolation evidence cannot be inferred from endpoint tests |
| 14 | T03 final Cultural direct binding and two-domain isolation; Cultural P01-P03 and two-specialist comparison | Full applicable Cultural B/I/D/C/S/M coverage; verify unchanged Weather release, publication and dependencies and reuse valid evidence, not a second Weather suite or publication |
| 15 | Build contracts and coordination, run existing automated implementation tests, then demonstrate G01/G03 and W01/W03 with valid results and approved calls to both released specialists | Specialist release evidence must match the versions invoked; G02/W02 remain automated defensive coverage, not learner failure exercises |
| 16 | W01/W03/W04 and P01-P04 on supported inputs, then CH02 on the final selected workflow version; retain pre-release evidence and a known-good recovery target | Actual end-to-end behavior on the final hosted version and consumer path; W04 requires the actual portal; CH02 must originate in the chosen channel; reuse overlapping assertions on the same run |

Prior results can be reused only for the **same retained version, configuration,
execution path and relevant identity/scope**. A new version needs its applicable
regressions; an older pass is not a pass for the new version. Release checks
through a different consumer path cannot reuse project-Playground results as
consumer evidence. Do not duplicate an exact final-version/path test just
because it appears under both feature and release headings.

Stage variants resolve capability changes without dropping assertions:

- **C01/C02 first-tool milestone:** the single-tool allowlist is required at
  04/11 and remains the default through release while skills are deferred.
  Preserve that historical evidence on its retained version.
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
- **C03, only when a real problem occurs:** preserve the actual error and
  attribute it correctly; do not manufacture C03a/C03b scenarios or require
  them for release. Explain Deny when a real permission request appears.
  If a participant declines, respect that decision without turning it into
  a planned denial drill or treating it as an upstream outage.

Use the lesson's exact saved supported inputs for B/I comparisons. Do not
reopen completed checkpoints merely to adopt new examples or repeat retired
negative cases. For S01/S02, list the supported location/date and tool needs
for the capability just added. Use approved fixed inputs
and service schemas; do not invent output or call counts before observing
the tool requests. Budget the initial model requests separately from exact
tool approvals/continuations. Never batch past a pending approval.

## Baseline and instructions

| ID | Input/procedure | Pass conditions |
|----|-----------------|-----------------|
| B01 | Ask one stable domain question in a fresh Conversation | Correct, concise answer; trained knowledge labeled accurately; no false tool or system-access claim |
| B02 | Participant asks a second supported general-domain question in a fresh Conversation | Useful, accurate answer within the current capability, with honest attribution and no invented current evidence |
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
| D02 | Create Conversation B, supply a different destination/interest, then ask the matching dependent follow-up | B uses its own supplied context; identifiers differ from A; no custom history replay or global context substitution |

Run D01-D02 independently for each specialist. A GitHub Copilot app session is
unrelated to these runtime identifiers.

For example, explain **before testing** how each newly created Conversation
maintains the destination and interest supplied to it:

| Context | Purpose and expected observation | Does not prove |
|---------|----------------------------------|----------------|
| Conversation A after a New York/wind-interest turn (D01) | A follow-up asking which destination and weather interest were supplied resolves to New York and wind, using the same service-returned ID | Live weather or persistent memory |
| New Conversation B after a Seattle/rain-interest turn (D02) | The same follow-up resolves to Seattle and rain using B's own service-returned ID | Cross-user authorization enforcement |

These are illustrative expectations, not precomputed passes. Use the same
saved prompt for comparisons and inspect the actual reply and identifiers.
At checkpoint 03 no weather tool is attached: contextual understanding is not
a verified forecast. C01 later needs the Weather MCP server's
`weather_forecast` invocation, source/result and trace evidence.

## Persistent memory

**Retained for later, not run on the default skills-and-memory-deferred route.** These
tests do not block that route's completion and must not be marked passed
without execution. See the [deferral policy](README.md#temporary-memory-deferral).

| ID | Input/procedure | Pass conditions |
|----|-----------------|-----------------|
| M01 | With explicit consent, store a low-risk preference; verify it in a new Conversation under the same trusted scope | Stored fact, provenance, and recall agree; Conversation history is not replayed |
| M02 | Correct the preference and verify the updated value in a new Conversation; if multiple approved scopes are used, give each its own consented preference | Each scope uses its own expected value under verified trusted mapping; no second account or cross-user access attempt is required |
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
retained but temporarily deferred four-tool expansion at 05/12, and T03 final
binding/isolation at 07/14. T03 verifies one tool per specialist on the default
route, not an implicit expansion.
These replace the older Toolbox-specific meanings; do not reinterpret
historical T01-T03 passes without an agreed migration and matching evidence.
Future-stage assertions do not block an earlier milestone, and a first-tool
pass does not automatically pass the later expansion.

| ID | Input/procedure | Pass conditions |
|----|-----------------|-----------------|
| T01 | At 04 attach Weather's public MCP URL directly with only `weather_forecast`; independently repeat at 11 for travel.art with only `find_museum_guide` | Exact URL/label, agent version, one-tool allowlist and actual supported approval policy read back, with no required value; no credentials or authentication connection; runtime call correlated with C01/C02, recording automatic execution or exact requested permission/decision/continuation on the selected route without inventing a human decision; only the selected operation is callable; no separate denial drill |
| T02 (deferred) | Only after explicit reintroduction of 05/12, expand that specialist's direct allowlist to its four approved tools and add its reviewed skill | Same public server URL/label retained; current schemas and exact allowed names verified; other domain/unselected tools not callable; configured approval policy retained and any actual requests respected; S01/S02 shows appropriate selection, restraint, sources and partial failure; not run or passed on the default route |
| T03 | At 07 verify Weather's final direct binding; at 14 verify Cultural's final binding, unchanged Weather release/dependencies and two-domain isolation | Exact released candidate/server/allowlist and any configured skill recorded; default route retains only weather_forecast or find_museum_guide respectively; final-path permission, runtime and P01-P03 evidence match; each specialist invokes only its own permitted tools; portal Auto approve is not evidence of permission on a different path; reuse valid unchanged Weather evidence, with no planned migration/re-release |

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
[the first-use Playground flow](APP-GUIDE.md#first-tool-use-in-the-playground)
or [the coach-run native-request flow](APP-GUIDE.md#first-tool-use-when-workshop-coach-sends),
according to the selected execution route;
record the actual displayed scope, participant choice and correlated result.
SDK/runner pending requests still need exact decisions and continuations.

### MCP behavior cases

| ID | Input/procedure | Pass conditions |
|----|-----------------|-----------------|
| C01 | With only the verified Weather MCP forecast tool allowlisted, ask one supported weather question | Runtime tool call, validated arguments, result, upstream provenance/timestamp, grounded answer, and a guided Microsoft Foundry trace inspection of the tool span |
| C02 | With only travel.art `find_museum_guide` allowlisted, ask one supported museum question, such as the Metropolitan Museum of Art in New York | Runtime tool call, validated arguments, returned guide attribution/URL, available verification date, grounded answer, and corresponding tool span; no weather claim or invented dataset version |
| C03 (only if encountered) | Inspect a real MCP/upstream error from an otherwise approved supported request; not a scheduled exercise or completion prerequisite | Error is attributed and reported; no invented result, unrelated-tool substitution, approval bypass or automatic retry; recover within approved scope before claiming the capability works |

The checkpoint 04 C01 run is the full trace-navigation lesson: inspect tool name,
arguments, status, timing, result, and relationship to the final response.
Checkpoint 11 reuses that knowledge and repeats detailed navigation only when
needed. A direct MCP client call does not prove the agent used the tool.

## Skills and multiple tools

**Temporarily deferred on the default route.** Retain S01/S02 below for later
explicit reintroduction or already configured capabilities; do not run them,
expand allowlists or create a skill-only candidate to fill 05/12. Follow the
[skills deferral policy](README.md#temporary-skills-and-multi-tool-deferral).

| ID | Input/procedure | Pass conditions |
|----|-----------------|-----------------|
| S01 | Apply the Weather research skill and test supported forecast/current/alert needs and a general-knowledge request | Exact skill version/delivery strategy recorded; appropriate tool selection and ordering; no unnecessary calls; actual provenance and limitations remain explicit |
| S02 | Apply the Cultural research skill and test supported museum guides, art events, covered layovers and cultural recommendations | Exact skill version/delivery strategy recorded; only verified travel.art tools used appropriately; guide URLs/freshness preserved; report any genuinely missing information honestly |

A skill guides use of already available tools. It does not connect an MCP server,
grant permission, or prove execution. Traces provide runtime proof.

## Workflow result contracts

Formal contracts begin at checkpoint 15.

| ID | Input/procedure | Pass conditions |
|----|-----------------|-----------------|
| G01 | Validate normal Weather and Cultural specialist results against versioned workflow contracts | Required destination, constraints, findings, source agent/version, provenance, uncertainty, missing-information, and failure-status fields are present |
| G02 (automated implementation coverage) | Existing local tests exercise invalid or contradictory contract data; no participant injection or live failure demonstration | Validation remains fail-closed, with no silent rewriting, instruction override or fabricated success |
| G03 | Compare contract fields with specialist release metadata and correlated traces | Agent versions and provenance agree with runtime evidence; each specialist remains inside its evidence domain |

Contracts validate structure. They do not independently prove that a tool ran or
that a source is truthful.

## Hosted Trip Planning Workflow

The shared tests cover the implementation behavior below. Run the existing
automated suite as an ordinary build check; do not turn its defensive fixtures
into participant demonstrations or remote/channel failure gates. Learners
create the workflow and verify supported, sourced trip results.
Author troubleshooting suites, captured responses, SDK event-replay tests and
diagnostic scripts are not workshop assets or additional participant exercises.
Use their findings to implement the host correctly, not to expand the course.

| ID | Input/procedure | Pass conditions |
|----|-----------------|-----------------|
| W01 | Submit one supported destination and traveler constraints | Both released specialists are invoked; both results validate; itinerary cites each evidence domain; versions and correlation evidence are recorded |
| W02 (automated implementation coverage) | Existing local tests exercise specialist errors and invalid results; no injected participant or live failure case | Valid evidence is preserved; invalid/failed evidence is isolated and reported without fabrication or silent substitution |
| W03 | Include valid traveler preferences, such as short walks and indoor museums, in the supported W01 trip request | The itinerary combines both evidence domains and explains how the actual conditions and preferences shape the plan; reuse W01 rather than add another call |
| W04 | In the actual Microsoft Foundry portal, use the displayed candidate version and a fresh Conversation for one supported trip with the existing approval policies; decide each actual permission card | Both completed tool executions are corroborated and the sourced final answer has no false pending-approval claim; actual decisions bind to current requests; automatic execution needs no cards or invented decisions; exact version, Conversation/run/response IDs, policy and available usage are retained |

At 15, run existing local implementation tests and verify G01/G03 and W01/W03
on the working workflow. At 16, verify the supported trip remotely.
Run W04 at 16 before promotion. Its successful trip may also satisfy matching
W01 assertions; do not duplicate calls for labels. The facilitator prepares
the same intended cases before the cohort with approved spend and tool decisions.
Two manual specialist calls followed by a manually written itinerary do not pass.
A custom-client success does not pass the required portal case.

### Repeat the Playground behavior in the destination

After the Playground baseline passes, repeat the supported W01/W03/W04 behavior
cases through the chosen Microsoft Teams or Microsoft Copilot Studio route
using [the destination parity plan](PUBLISHING.md#workflow-destination-test-parity).
Keep exact workflow/specialist versions, supported inputs and assertions
matched, with fresh context where the original case required it. Record the
actual route for each result; do not relabel a Playground execution as a
destination pass. Actual native decisions, source and uncertainty, trusted state
mapping and handling of any real error must remain intact. Do not inject a
failure or require a deliberate denial for destination parity.
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
| P02 (shared evidence) | Reuse the approved-consumer invocation from P01/P03; no separate request or second-account exercise | Actual caller, endpoint/version and verified access match the successful invocation; no broad permissions added merely for the check; no claim that unauthorized-caller denial was demonstrated |
| P03 | Run applicable supported feature requests through the consumer path, reusing matching evidence | Tools, Conversations, source attribution, identity and downstream access work on the actual path; memory and skill delivery are required only when configured; no deliberate failure demonstration |
| P04 | Promote a fully passing update, invoke it, and verify the previous known-good version remains an available documented recovery target | Stable endpoint remains unchanged; metadata and behavior prove the update; recovery target and procedure are verified without routing traffic to a known-failing version |

P02 records access evidence from the existing approved-consumer exchange,
not a separate test. Do not require another identity or an access-denial
demonstration to complete the workshop. Successful authorized calls do not
prove unauthorized callers are denied or that user histories are isolated;
retain the separately required Conversation, isolation and channel assertions.

At 07, P03 covers Weather B, I, D and C01R on supported inputs.
At 14, repeat Cultural B, I, D and C02R on supported inputs.
On the default skills-deferred route, omit T02/S01/S02 and keep the one-tool
bindings. Include S01/S02 and T02 when skills/expanded tools are reintroduced
or already configured; never silently remove them to avoid applicable checks.
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
| CH01 | At 07 publish the tested Weather release to the approved Microsoft Teams and/or Microsoft 365 Copilot surface; participant sends a supported weather request there | Approved audience, channel identity, app/registration and pinned active version verified; actual channel reply with weather provenance and uncertainty; same-run service/trace linkage proves the released Weather agent and permitted MCP tools executed; channel-specific access, trusted Conversation/memory isolation and configured approval behavior verified, including any actual decisions; no fixed approval value or mandatory permission card; direct endpoint remains usable; all chosen surfaces have evidence before 08 |
| CH02 | At 16 publish the final released hosted workflow; participant sends a supported trip request from the chosen surface and inspects the same execution | Approved app/channel maps to the workflow stable endpoint/version, not a worker; channel reply contains a sourced itinerary with uncertainty; correlated request, both released specialist invocations, result validation and aggregation are observed; identity mapping, downstream access and configured approval behavior remain effective, with decisions only for actual requests; no manual worker calls, direct-tool shortcut or fabricated evidence; all chosen surfaces have evidence before core completion |

Before tests, approve exact prompts, supported location/dates, bounded model
requests, tool approval continuations, stored data and costs. Verify configured
identity/Conversation boundaries through metadata and successful scoped
exchanges, with no deliberate denial or cross-user access attempt. Retain
trusted user/state mapping when a channel needs a different supported client
or adapter; do not claim untested cross-user denial. Do not grant roles, switch audience to organization-wide, or
silently change the configured approval policy to manufacture a pass.
Automatic approval is valid and does not itself block a channel milestone.
Use read-only metadata/access checks where sufficient and live execution for
runtime assertions. Reuse an exchange for overlapping assertions only when
target/version, actual channel, identity/scope and input match; no duplicate
call merely for another test label. A channel happy path may satisfy a matching
W01/W03 assertion; it does not claim that automated defensive cases were
demonstrated through the channel.

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
| WD03 | Merge the PR, then manually dispatch deployment on the default branch with its full reviewed commit SHA and deployment confirmation | Confirmed matching commit proceeds without any GitHub Environment; review the deployed revision without asking the participant to submit a wrong commit or unchecked confirmation |
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
| K02 | Build each specialist one capability at a time and run adapted tests | Both specialists independently pass baseline, instructions, Conversations, MCP and release gates, plus any explicitly reintroduced or already configured skills/memory and their affected tests |
| K03 | Demonstrate a supported hosted workflow result and review the release handoff | Existing implementation checks, G01/G03, W01/W03 and P01-P04 pass; participant explains traces, tradeoffs, limitations and remaining resources |
| A01 | Inspect and explicitly approve one valid, bounded action on the synthetic service | Exactly the intended authorized mutation occurs and its result is verified; respect any actual decline without requiring a denial drill |
| A02 (automated implementation coverage) | Existing local tests cover invalid input, missing targets and downstream failure | Explicit errors; no false success, duplicate mutation or unapproved write; no participant failure demonstration |

A01-A02 are not required for read-only capstones. Never introduce real payments,
bookings, production tickets, or sensitive personal data.

## App practice evidence

At each checkpoint, record the technique tried, one alternative discussed, and
the participant's explanation of when each helps. A Chat equivalent is
sufficient if a UI feature is unavailable.
