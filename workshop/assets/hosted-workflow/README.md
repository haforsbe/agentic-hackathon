# Hosted workflow plumbing and facilitator reference

This asset supports checkpoints 15-16 in the **GitHub Copilot app** workshop.
It is not a completed participant exercise or a deployment command.

`src/trip_server.py` provides reusable Microsoft Foundry hosting plumbing;
`trip_responses.py` connects chat input and exact native tool decisions to a
workflow. `trip_workflow.py` is a **facilitator reference implementation**:
Workshop Coach must still create participant-specific versioned contracts,
specialist invocation, failure isolation and sourced aggregation at checkpoint
15. Participants review and explain the generated implementation and test the
actual workflow; they do not write it themselves or create this code-first
hosted agent directly in the Microsoft Foundry portal. Local preparation and
creation/deployment below are coach-executed under the
[execution ownership rule](../../COACH.md#hosted-workflow-execution-ownership)
and its separate approvals. Copying or running this reference is not
participant completion.
The host imports no workshop runner modules or unpublished author tooling.

The reference intentionally accepts only the Metropolitan Museum of Art in
New York and one visit date within the next six UTC days. It does not silently
accept additional traveler constraints. Other requests ask for clarification
without calling a specialist. This narrow teaching story is not a general
travel planner.

## What stays authoritative

Weather and Cultural Travel are independent, already released Microsoft Foundry
specialists. Each native approval request must match its configured server label
and qualified tool name; each continuation binds the exact pending request and
arguments. Prose never grants approval. Denial remains denial, with no replacement
tool, fabricated evidence or model retry.

No particular specialist approval setting is required. Automatic execution
and mixed per-tool policies are valid: a completed tool call must still match
the configured specialist, tool and source evidence, without an invented human
decision. Actual pending requests still require their exact decisions.
The always-allow recommendation belongs at direct-tool creation, especially
for Microsoft Teams; retain existing settings without later configuration
questions or corrective versions.

Align specialist instructions with the saved policy when authoring the
definition. Do not retain a blanket human-approval prerequisite for a tool
configured for automatic execution. A prose claim of pending approval without
a native request is a failed result, not a permission card to invent or approve.

One graph is exposed through Responses and Invocations. Request-scoped clients,
trusted user/session scope, SDK-owned checkpoints and separate run storage prevent
shared conversation history. The runtime verifies token tenant/principal claims
against the confirmed configuration and excludes developer sign-in fallbacks.
The hosting platform remains responsible for authenticating requests and supplying
trusted scope headers; do not expose this reference as an unauthenticated public
HTTP service or forward arbitrary caller-supplied identity headers.

Final evidence must match its specialist/version and completed native tool call.
Direct claims that approval is still pending fail closed after a resolved native
decision. They are reported as an unusable specialist result, not silently
removed or treated as success. Historical, conditional and policy discussion of
approval remains allowed. Sources and uncertainty from the other valid specialist
remain visible. This narrow narrative check cannot prove the truth of every
natural-language claim; live quality review remains necessary.

Keep specialist summaries concise and their output allowance large enough for
all required sections, sources and uncertainty. A completed tool call followed
by an incomplete model reply is not a successful specialist result. Preserve
the service's incomplete-response reason, reject the truncated reply and obtain
fresh scoped approval before another paid attempt; do not retry automatically.

Outer Responses `include` selectors are validated against the installed public
SDK contract and never forwarded to specialists. Caller model, tool, instruction
and runtime overrides are rejected.

## Configuration and dependencies

Use Python 3.12 or later locally. The manifest targets the Microsoft Foundry
Python 3.13 remote-build runtime. `src/pyproject.toml` pins the direct SDK
versions, including `azure-ai-agentserver-responses==2.2.0b1`.
`src/requirements.txt` exports the complete resolved version pins with platform
markers, without private download URLs.
Use an approved package feed that actually supplies those versions; do not
silently substitute other packages, feeds or SDK versions.

The asset does **not** include a portable transitive lock. The accessible feed
resolved a private development lock containing organization-scoped artifact
URLs; that lock is deliberately excluded. The exported requirements preserve
resolved versions but do not lock artifact hashes or package availability.
A successful local restore does not prove that a participant's remote build can
access the same packages. Resolve that prerequisite before approving a deployment.

From this asset directory, create a local environment and install the pinned
requirements using your approved feed:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --index-url <approved-feed> -r .\src\requirements.txt
```

Use that environment's interpreter for every local check below. A global
installation can expose incompatible preview APIs even when its packages are
newer. Restore the pinned environment instead of changing the imports, upgrading
global packages or substituting dependency versions.

There is one non-secret runtime configuration: `WORKFLOW_CONFIG_JSON`. Make a
local copy of `config.example.json` as `config.local.json`. Fill every field from
the participant-confirmed project, deployed runtime identity and independently
verified specialist releases. Versions are positive integer **strings**.
`server_label` and `tool_name` are exact discovered runtime names; they are not
derived from agent names. No account, endpoint, credential or resource fallback
is provided. The blank example is intentionally unconfirmed and cannot start
the host.

Confirm access and current-operation permissions separately. Only after verifying
the chosen values, set `participant_confirmed` to `true`. This setting records
configuration confirmation, **not** permission to deploy, spend, change roles or
approve a tool call.

```powershell
$env:WORKFLOW_CONFIG_JSON = Get-Content -Raw .\config.local.json
.\.venv\Scripts\python.exe .\src\workflow_config.py |
    Set-Content -Encoding utf8 .\azure.yaml
```

That command only renders local deployment plumbing from the same configuration;
it creates no cloud resource and generates no workflow graph.
Inspect the resulting ignored `azure.yaml`. The exact project endpoint, workflow
name and runtime JSON all come from that one validated setting. Do not separately
edit its targets. Invalid, missing, unknown or unconfirmed settings fail explicitly
before real credentials or clients are created.

Actual deployment remains a separate approved operation using the current
Microsoft Foundry skill and workshop instructions. Do not deploy the facilitator
reference in place of the reviewed coach-created workflow, copy someone else's
configuration, change runtime identity to make a check pass, or automatically
create missing dependencies.

Native Conversations, stored responses and workflow state can contain user input
and tool results. The runtime keeps request/checkpoint records for safe
continuation and uncertain-request reconciliation; they are not shared fixtures.
Apply appropriate access, retention and data/cost approval. Never commit those
records, environment files, configured manifests or local configuration.

## Usage and limits before live tests

Before a participant runs the hosted workflow, require passing offline tests,
the exact reviewed configuration and a [scoped test approval](../../COACH.md#scoped-test-approvals).
Explain possible charges, execution scope and supported controls. Price lookup,
monetary reservations and whole-case cost estimates are not workshop gates.
Keep available service-reported tokens for an optional end-of-workshop estimate;
missing pricing or internal-turn counts do not by themselves block a test.

The reference has these application controls:

| Control | What it bounds | What it does not establish |
|---|---|---|
| At most four native Responses submissions per trip, journaled before submission | Two initial specialist requests and their two exact human-decision continuations; uncertain attempts consume entries and cannot be replayed automatically | Four underlying model inference turns or a cumulative input-token limit |
| `max_output_tokens=500` on each submission | Requested generated response tokens, including reasoning tokens | Cumulative internal input processing, separately billed memory work, or a currency cap |
| `max_retries=0`, client timeout and exact tool-decision validation | Client retries, individual client waits and which pending decision the application continues | Cancellation of server-side work, a billing timeout, or prevention of costs already incurred before a returned response is rejected |
| Workflow `max_iterations=10` | Local graph supersteps | The managed specialist's internal model/tool/memory loop |
| Deterministic itinerary assembly | No extra model call by the assembly executor | The cost of the independently hosted specialists |

The native response bodies and available `usage` are retained in the runtime
`requests.json` journal, keyed by submission, with returned response IDs.
Existing records can inform an approved read-only reconciliation; deduplicate
by response ID and treat absent usage as unknown. Do not create another model
response just to populate usage. The journal's usage is not proof of inclusion
of separately processed memory work or a full account bill. Do not add a
workflow aggregate to the same specialist usage twice; retain the actual
model/deployment/version, checkpoint and execution route where available.
Keep detailed accounting in existing execution evidence and follow the
[exercise-end token policy](../../COACH.md#checkpoint-usage-summaries) for the
single participant-facing total. Do not create a separate cost-readiness ledger.

An optional monetary estimate is on request, never a completion gate. Follow
the coach's [usage-summary policy](../../COACH.md#checkpoint-usage-summaries)
for matched official rates and explicit missing-usage/excluded-charge limits.
Any participant-imposed cost restriction still applies; if compliance cannot
be established, pause the affected action and clarify. A prior test approval
or resume request never authorizes extra calls.

The reference does not set `max_tool_calls` or claim an aggregate managed-agent
token/spend control. A parameter in an installed SDK is not proof that the
exact agent endpoint accepts it, that it covers MCP/memory, or that it enforces
a billing limit. Adding controls requires documented route semantics, separate
change approval and affected regressions. Do not bypass human decisions or
silently disable memory or replace specialist tools. Preserve uncertain-request
recovery; no usage record alone proves runtime behavior passed.

## Intended local tests

From this asset directory:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s .\tests -p "test_*.py" -v
```

The tests use **small synthetic fixtures**. Clients are patched; no
Microsoft Foundry account, model request, MCP tool execution or human decision
is needed or claimed.

The repository's `Workshop runner offline checks` workflow runs these same
tests on Linux with Python 3.13, separately from the SDK-free runner tests.
It installs the exported requirements from
`https://packagefeedproxy.microsoft.io/pypi/simple`, the feed used for the
local restore, without a fallback index. Feed or package failures block the
check rather than silently changing dependencies. A green check establishes
that CI environment's offline behavior, not a Microsoft Foundry remote build
or any live gate below.

| Test | Intended assertion |
|---|---|
| `test_required_evidence_fields_and_source_sections` | G01: required versioned fields and both evidence domains |
| `test_invalid_or_contradictory_final_evidence_is_not_success` | G02/W02: invalid, instruction-shaped extra fields or contradictory final evidence cannot become success |
| `test_release_version_and_tool_origin_match_contract` | G03: configured origin/version/domain agree with synthetic evidence |
| `test_supported_trip_combines_both_specialists` | W01/W03: both invocations, sources, uncertainty and traveler preferences survive assembly |
| `test_automatic_and_mixed_policies_preserve_completed_tool_evidence` | Automatic and mixed policies retain both domains' completed tool evidence without invented decisions |
| `test_automatic_execution_still_checks_tool_origin_and_approval_linkage` | Automatic execution still validates the selected tool, origin, completion and any approval reference |
| `test_failed_or_invalid_specialist_preserves_other_evidence` | Automated W02 coverage: each isolated failure/invalid result preserves the other domain without retry or fabrication |
| `test_ambiguous_request_requires_clarification` | Automated clarification guard: unsupported constraints do not trigger calls or silent coercion |
| `test_two_separate_decisions_produce_sourced_reply` | Checkpoint 15 local W04 prerequisite: ordinary chat input, current native decisions, continuation and assembly |
| `test_automatic_tool_execution_needs_no_synthetic_permission_cards` | The Responses adapter returns sourced output without permission cards when both tools execute automatically |
| `test_denial_stays_partial_without_executing_denied_tool` | Automated safety coverage: actual denials remain effective; not a participant denial exercise |
| `test_native_submission_limits_and_uncertain_attempts` | Request/output limits, disabled client retries, recorded-response reuse and unknown usage remain distinct from a model-cost cap; a fifth or uncertain submission cannot be sent |

These defensive fixtures remain ordinary automated implementation coverage.
Do not ask participants to inject failures, submit malformed trips or decline
a request to demonstrate them. The learner path builds the workflow and tests
a supported result, with actual decisions only when the runtime requests them.

These are not full live G03/W01 execution proofs. **W04 requires the participant's
actual Microsoft Foundry chat exchange**, completed native tool execution and any
requested human decisions, correct final reply and correlated same-run
specialist/validation/assembly traces on the exact deployed version. Synthetic
tests, an Invocations reply or a successful response schema cannot pass that gate.

Stable consumer/release assertions and CH01/CH02 require their own real,
approved consumption and channel evidence in the required checkpoint order.
Neither this asset nor these tests mark any checkpoint, publication or channel
milestone as passed.
