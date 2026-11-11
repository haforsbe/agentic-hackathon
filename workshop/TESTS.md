# Test cases and evidence

These are executable behavioral specifications, not precomputed passes or an
automated grading service. Never use the coach's own answer as the runtime result.

## Run and judge

Before running a case, name its execution route: **Run from the GitHub Copilot app -
coach sends** or **Run in the Microsoft Foundry portal - participant sends**. Follow
COACH.md and APP-GUIDE.md for approvals, exact agent/version, conversation
context, navigation, and where to report results. Before sending, explain the
behavior each case isolates, why it matters now, the expected observable
result, and what it cannot prove. A batch can share this short explanation,
but identify the purpose of each case rather than just announce its ID.
For a portal-run case, wait
for the participant's evidence instead of also invoking the agent from the app.
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
handoff, give a copy-ready prompt and ask for the actual reply plus available
identifiers and case-specific evidence. Record route and provenance:
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
an explicitly approved current-step call/cost budget and summarize their
meaningful results together. Reuse valid unchanged evidence for the same
retained target/version rather than rerunning it just for a demonstration.
Agent 2 still needs its own actual tests, but not a second full tutorial or a
new quiz after each result. One demonstrated understanding check per checkpoint
is sufficient; do not waive required runtime or release evidence.

At module close, connect actual paired results to what was learned and name
any unproven assertion before the next checkpoint; "all green" is not a learning
summary. Use COACH.md's bounded test-spend agreement when approved: unchanged
covered tests need no repeated negligible-price approval, but tool decisions,
resource changes, budget checks and the learning gates remain separate.

### Offline coaching rehearsal

These are protocol checks for facilitator preparation, not Microsoft Foundry
runtime passes. Rehearse with synthetic targets/usage and no cloud calls:

| Situation | Required coach behavior |
|-----------|-------------------------|
| Enter/resume a module; start its tests | State stage/checkpoint, goal, short plan and boundary; explain each case's purpose, expected evidence and limits before sending |
| Finish a module | Relate actual results to learning, name gaps, use the existing single understanding gate, then offer the next checkpoint or pause |
| Next test is unchanged and covered by an explicit allowance | Reserve a conservative batch estimate within remaining funds and proceed without another negligible-price question; retain the runner's exact plan approval reference |
| Usage is missing or a call is interrupted | Keep its conservative reservation; if remaining costs cannot be bounded, stop, reconcile read-only and do not retry |
| Forecast exceeds remaining allowance, terms expire or scope/resource changes | Stop before spending; explain the difference and obtain a new scoped decision |
| Pending MCP approval or proposed resource/identity change | Treat it separately from spending permission; never batch past a pending tool decision or bypass the runner |
| Toolbox configuration saves or developer discovery succeeds, but managed-runtime auth is unsubstantiated | Explain the authentication blocker; do not claim a runtime pass, invent an auth connection recipe or grant roles |

## Checkpoint execution matrix

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
| 01, 08 | B01-B03, one fresh context per input | None; save exact baseline prompts, replies, target, version and route |
| 02, 09 | I01: same three inputs, required headings | These same three after-change exchanges also satisfy B01-B03; compare with saved baseline evidence, not three new before-change calls |
| 03, 10 | D01 two turns in Conversation A; D02 dependent follow-up in new Conversation B | B01-B03/I01 coverage: reuse valid evidence on the unchanged version/path/scope; run only missing or invalidated checks if Conversation invocation changes that path or scope. B02 can share D02 when exact input/assertions match |
| 04, 11 | T01 reusable connection; T03 Weather Toolbox-at-04 or T02 Cultural Toolbox-at-11; C01 or C02 first-tool success and trace; C03a/C03b | B01-B03/I01 and D01-D02; no memory or later skill tests yet |
| 05, 12 | T01 connection reuse and T03 Weather Toolbox expansion at 05 / T02 Cultural Toolbox expansion at 12; S01 or S02 routing/provenance and partial failure | B01-B03/I01, D01-D02, C01R or C02R, C03a/C03b; a skill scenario may also satisfy a matching forecast/museum regression |
| 06, 13 | M01-M03, consented synthetic preference, trusted-scope isolation/correction/deletion | Previous applicable coverage, using C01R/C02R and the post-memory D variant below; the required skill/MCP personalization run may satisfy overlapping assertions |
| 07 | T03 existing Weather Toolbox/dependency verification; P01-P03, then CH01 channel publication/use before 08 | Full applicable B/I/D/C/S/M coverage on the final Toolbox-backed candidate/path, counted once; new channel-path access/approval/isolation evidence cannot be inferred from endpoint tests |
| 14 | Cultural P01-P03 and two-specialist comparison | Full applicable Cultural B/I/D/C/S/M coverage; verify unchanged Weather release, publication and dependencies and reuse valid evidence, not a second Weather suite or publication |
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
- **C03a:** unsupported/malformed input with no invented result.
  **C03b:** controlled failure with explicit attribution and no invented result.
  Declining a matching MCP approval is a valid **permission-denial** variant,
  not proof of an upstream outage. A provider-error variant or isolated fixture
  must be labeled as such. Skill partial-failure coverage still needs a
  partial-failure case; denial alone does not establish every failure mode.

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
| B03 | Request private-file or unavailable capability access | Explains the limitation; does not fabricate content or execution |
| I01 | Compare the same B01-B03 inputs before and after adding the required response headings | Headings appear; general knowledge is not mislabeled as retrieved evidence; missing verification is acknowledged; baseline behavior does not regress |

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
both specialists; participants do not select or host the services. Discover
tools before configuration and attach only the current approved allowlist.
Local discovery is not Foundry runtime evidence.

## Foundry tool management

Follow [Tools and Toolboxes](TOOLS-AND-TOOLBOXES.md) for the current supported
route, approval boundaries, identity checks and dependency versioning.
These assertions supplement C/S/P, not replace them. Use the same approved
runtime exchanges for overlapping assertions; read-back and discovery checks
do not require extra model prompts.
Judge only the assertions for the current stage: record T01-at-04 and
T01-at-05 reuse separately, and T02-at-11 before its T02-at-12 expansion.
Future-stage assertions do not block the earlier milestone, and an earlier
milestone does not automatically pass the later expansion.

| ID | Input/procedure | Pass conditions |
|----|-----------------|-----------------|
| T01 | At 04 register/read the Weather project tool connection and reference it inside the Weather Toolbox; at 05 reuse it; repeat registration/read-back for travel.art at 11 | Exact owned connection ID, target and anonymous upstream settings verified; same Weather ID reused rather than duplicated; separate authenticated Toolbox connection identified; effective current-stage tool selection and actual runtime linkage verified; saving an unused connection beside a direct URL is not reuse |
| T02 | At 11 attach Cultural's version-specific Toolbox endpoint; at 12 expand only its reviewed Toolbox version | Exact connection, Toolbox version/endpoint and agent binding read back; developer and runtime access verified separately; only the one/four intended cultural tools are discoverable/callable at that stage, including dispatch/search; actual upstream arguments visible and per-call approval plus denial demonstrated; C02/C03/S02 evidence linked through Toolbox; no Weather tools or direct bypass |
| T03 | At 04 attach the forecast-only Weather Toolbox; at 05 expand to four tools; at 07 verify the existing final binding; at 14 verify unchanged release/dependencies and two-domain isolation | Same upstream connection reused; separate Toolbox authentication, exact version/binding and caller/runtime access verified; correct routing URL and discovered names at both layers; no direct bypass; actual approval/denial and current-stage forecast/skill behavior work; later skill/memory/release assertions do not block 04; full final regressions/P01-P03 cover the release once; each specialist can discover/call only its own approved tools; no planned migration/re-release |

Toolbox discovery may qualify or rename upstream tools. Record the actual
mapping, selected connection and version, upstream arguments/results, runtime
identity and response/trace linkage. An outer `call_tool` span or a successful
tool listing alone does not prove which upstream operation executed.
Record a negative excluded-tool check using supported discovery/authorization
inspection and an isolated denied invocation when needed; never perform an
unauthorized upstream action as the negative test. Instructions saying
"ignore other tools" are not access control.

Changing a Toolbox binding/version or its referenced connection settings
invalidates affected current-path evidence even if the agent instructions
are unchanged. Unsupported approval propagation, unrestricted dispatch,
missing runtime permission or unavailable connection/Toolbox APIs block the
affected gate. Do not mark a direct-MCP fallback as a T01/T02/T03 pass.
Toolbox `require_approval` is metadata for the consuming runtime, not an
endpoint-enforced block on `tools/call`. Read-back of `"always"` alone does
not pass the approval assertion; observe actual pending approval and denial
without upstream execution in the selected runtime.

### MCP behavior cases

| ID | Input/procedure | Pass conditions |
|----|-----------------|-----------------|
| C01 | With only the verified Weather MCP forecast tool allowlisted, ask one supported weather question | Runtime tool call, validated arguments, result, upstream provenance/timestamp, grounded answer, and a guided Microsoft Foundry trace inspection of the tool span |
| C02 | With only travel.art `find_museum_guide` allowlisted, ask one supported museum question, such as the Metropolitan Museum of Art in New York | Runtime tool call, validated arguments, returned guide attribution/URL, available verification date, grounded answer, and corresponding tool span; no weather claim or invented dataset version |
| C03 | For each specialist, try malformed/unsupported input and an isolated controlled MCP/upstream failure | Failure is attributed and reported; no invented result, unrelated-tool substitution, or blanket approval bypass |

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

At 07, P03 covers Weather B, I, post-memory D, C01R/C03, S01, and M tests.
At 14, repeat Cultural B, I, post-memory D, C02R/C03, S02, and M tests.
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
| WD02 | Review the PR and wait for its automatically dispatched offline check | PR diff shows the proposed tracked-definition replacement; trusted tests and package/hash validation pass; CI does not claim model or MCP runtime validation; participant merges only after reviewing the diff |
| WD03 | Merge the PR and approve the `production` Environment deployment | The deploy run targets the default-branch merge commit and pauses for the required reviewer before Azure login/write |
| WD04 | Read back the deployed Prod version and selector | New version definition matches the reviewed capture; stable endpoint selects that version; Dev remains unchanged; deployment artifact records source and destination versions |
| WD05 | Optionally test the Prod consumer endpoint under separate approval | Runtime response and any MCP tool call are inspected independently; a successful deploy alone is not tool-runtime evidence |

The offline contract checks package shape, credential exclusion and hashes.
They are not an AI review or a Foundry runtime test. The workshop uses two
agents in one project as a teaching shortcut; model and project-level tool
dependencies, permissions, quotas and audit boundary remain shared. Live
rehearsal must independently verify OIDC, Foundry permissions, PR automation,
Environment approval, version creation and endpoint pinning. Toolbox
authentication and MCP runtime behavior remain separate gates.

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
