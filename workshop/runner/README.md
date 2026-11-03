# Workshop execution helper

This is coach/facilitator plumbing, not another student lesson or a replacement
for the installed Foundry skill. Use that skill's applicable workflow first.
The helper implements the established explicit-Azure-CLI-credential fallback
for ordinary prompt agents. It does not configure hosted agents, memory,
consumer endpoints, telemetry, or role assignments.
It also does **not** register reusable Foundry tool connections, manage
Toolboxes, accept connection-backed MCP definitions, or authenticate Toolbox
endpoints. Its public direct-MCP examples are reference/partial-route
operations, not the full v8 core tool-management implementation. Use the
rehearsed current Foundry skill/API route in
[Tools and Toolboxes](../TOOLS-AND-TOOLBOXES.md) for those gates and their
runtime tests. Do not relax the helper's endpoint checks to bypass this limit.

## Prepare before the cohort

Run `python workshop\runner\workshop_runner.py readiness` in the same execution
environment that will run workshop operations. It checks executable presence
and exact package versions offline; it neither installs packages nor signs in.
An installed CLI is not proof of project access. On another operating system,
use its native path separators.

Use an isolated environment with `requirements.txt` from this folder. Install
only after a missing-dependency/version-mismatch result or a manifest change.
Do not install into unrelated environments. Rehearse SDK upgrades and update
this manifest and the runner's version check together. Run offline tests with:

`python -m unittest discover -s workshop\runner -p "test_*.py"`

## One reviewed operation, one plan

The coach creates a plan under ignored `.workshop/`, displays its target,
prompts/actions, context, output/call limits and possible cost, and obtains
current-step participant approval **before executing** it. An existing explicit
[bounded test-spend agreement](../COACH.md#bounded-test-spend-agreements) may
cover the exact displayed test plan; do not ask again solely because each
covered model call has a negligible price:

`python workshop\runner\workshop_runner.py execute --plan .workshop\approved-step.json`

A plan records approval; it does not obtain approval or enforce a security
boundary against someone editing local files. Never manufacture an approval
reference. Do not execute a plan merely because it exists, the participant said
"resume", or its run ID is unused. Public/synthetic data only; never put tokens,
authorization headers, private prompts, or credentials in plans/configurations.
Copy `plan.example.json` into `.workshop/` as a starting shape, fill it from
confirmed context, and use the exact previously saved inputs for regressions.
The example's empty target/permission/approval fields deliberately prevent
execution; its Weather prompts are not a Cultural baseline.

The runner bounds requests and output tokens, **not currency**. Before execution,
the coach must conservatively estimate/reserve the whole batch against the
agreed remaining allowance, including input/history, output and uncertainty,
and record sanitized cumulative estimates locally. Missing usage is unknown,
not zero; stop if costs cannot reasonably be bounded. No money field in a plan
enforces a billing cap. Changed targets/scope or further spending need renewed
approval; ongoing resource, telemetry and GitHub Copilot billing are outside a
model-token estimate. Never treat a spend allowance as resource-write or MCP
tool approval. All validation and pending-approval stops below still apply.

Required common fields:

| Field | Meaning |
|-------|---------|
| `run_id` | Unique current-step attempt name; existing evidence makes repeat execution fail |
| `operation` | One operation from the table below |
| `approval_reference` | Reference to the actual participant decision covering this exact scope; read-only checks must also be within the agreed inspection scope |
| `public_or_synthetic_data_only` | Must be `true`; evidence stores the actual exchange locally |
| `account`, `tenant`, `subscription` | Participant-confirmed identity and scope, not credentials |
| `azure_config_dir` | Absolute workshop-only CLI profile outside the repository; never the global profile |
| `endpoint`, `project_resource_id` | Exact confirmed Foundry project endpoint and discovered ARM ID; never construct a guessed resource ID |
| `required_permissions` | Nonempty list of `{ "kind": "actions" or "dataActions", "operation": "exact operation name" }`; discover the correct current permission names using supported guidance before presenting the plan |
| `agent_name`, `agent_version` | Exact target and immutable version; version omitted only for creation |
| `configuration` | Reviewed JSON file under `student/`, with `name` and `definition`; only ordinary prompt agents and the selected public MCP services, always approval |

| Operation | Additional fields and boundary |
|-----------|--------------------------------|
| `inspect` | Read back the pinned version and compare it with the local definition; no inference |
| `create-version` | Create one reviewed candidate and independently read it back; no tests, routing, or deletion. This narrow helper supports model/instructions/public MCP definitions only; other definition fields fail validation. Discover/check the intended agent name beforehand. |
| `run` | `cases`: 1-12 `{id, prompt, conversation_id?, store?}`; `max_requests` exactly equals case count; `max_output_tokens`: 16-4096. Separate requests have no replayed history. With an explicit returned `conversation_id`, store and use that managed Conversation. MCP configurations require `store: true` for same-run retrieval/approval; include retention/storage in the approval explanation. |
| `retrieve` | Exact `response_id`; retrieve a saved existing response, never generate a replacement. Linkage mismatches stop and preserve the raw record for review. Retrieval depends on the original response's storage/retention. |
| `new-conversation` | Create one managed Conversation without model inference; return its ID for a separately approved run |
| `continue` | Exact `response_id`, `approval_request_id`, `server_label`, `tool_name`, `arguments`, boolean `approve`, and `max_output_tokens`; inspect and match the pending request before submitting exactly one approval/denial and continuation |

Every execution checks CLI availability/sign-in in its operation process,
account/tenant/subscription, actual SDK token identity, project metadata,
declared permission grants/exclusions, direct project access, and pinned
configuration. The coach must verify the permission names cover the actual
operation; an unrelated permission in a plan is not permission to write.
Pagination or inconclusive permissions stop rather than create a write probe.
Checks for an approved batch share one process/client; CLI identity is checked
again before each model request or resource write. No global sign-in changes.

When a token's username claims differ from the selected CLI account label,
the runner first verifies the token's tenant, rechecks the CLI account, tenant
and subscription, then uses the read-only Microsoft Graph lookup
`az ad signed-in-user show --query id` to compare the selected user's directory
object ID with the token's `oid`. This alias path requires access to that
signed-in-user lookup; a failed lookup, empty/invalid ID or different/missing
token ID stops execution. The lookup is repeated for each alias token, not
cached across requests or scopes. Exact-name matches keep the existing
tenant-and-username check without requiring the lookup. The runner does not
change sign-in profiles, grant permissions, or save tokens or directory identity
details in evidence.

MCP tool discovery can occur during inference even when no weather/cultural
tool executes; record that distinction. On a new tool-approval request, the
runner **stops the batch**. Remaining cases are not run. Inspect the proposed
tool and inputs and obtain a separate scoped decision; a new continuation plan
cannot approve a different request or multiple calls. Decline is supported.
An incomplete response, version mismatch or error also stops without retry.

## Evidence and recovery

Evidence is written exclusively to `.workshop/evidence/<run_id>.json`, with
pending markers **before** a write or paid request. Responses are saved before
linkage/behavior judgement. The helper does not mark checkpoints passed, edit
participant progress, change model choice, or calculate a guessed price.
Usage absent from a response stays `null`. Use response IDs to deduplicate the
existing progress ledger; apply only separately verified matching token rates.

The record includes prompts, response IDs, reported agent/version, actual
replies, tool/approval output, Conversation linkage and available usage.
The coach shows the meaningful paired results together, judges them against
TESTS.md, then records progress once per result/status boundary.

Do not delete an attempt record, change its run ID, or rerun after an
interruption to "see if it worked". Reconcile its service-returned response,
version or Conversation ID read-only first; if unknown, involve the facilitator.
The journal is a local duplicate-attempt guard, not a server-side idempotency
guarantee. Different run IDs do not authorize a retry.

## Scope and validation limits

Offline tests cover request shaping, pinned versions, approval boundaries,
budget validation, identity/permission helpers, result preservation and repeat
guards using synthetic objects. They do **not** prove current Foundry runtime,
MCP reachability, telemetry, hosted deployment or consumer authorization.
Rehearse those integrations in an explicitly approved environment before the
cohort. Use supported specialist helpers for memory, release and hosting rather
than extending this runner opportunistically during a live lesson.
