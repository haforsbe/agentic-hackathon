# Direct MCP connections for the core workshop

Curriculum `two-specialists-workflow-v10` connects each Microsoft Foundry
Prompt Agent directly to its selected public MCP server. A tool is one
operation exposed by that server; a skill guides which permitted tools to
use and in what order. Registering a server for the GitHub Copilot app does
not configure a Microsoft Foundry agent.

Toolboxes and their authentication connections are **not core prerequisites
or exercises**. Their managed prompt-agent authentication path was not
established, so they are deferred rather than presented as a working advanced
lab. This revision is a curriculum change, not a fallback that passes old
Toolbox gates. Do not create Toolbox resources, authentication connections,
roles or replacement hosted specialists to complete the direct-MCP lessons.
Existing participant resources remain untouched.

## Route and incremental scope

The coach supplies the endpoints, current schemas and coverage information
from [MCP-SERVICES.md](MCP-SERVICES.md). Participants do not host MCP servers,
research URLs or obtain upstream credentials.

| Specialist | Direct route | First tool | Expanded allowlist |
|---|---|---|---|
| Weather Research Agent | Agent -> `https://weather.datakoot.com/mcp` -> requested Weather tool | `weather_forecast` at 04 | `geocode`, `weather_forecast`, `weather_current`, `weather_alerts` at 05 |
| Cultural Travel Agent | Agent -> `https://mcp.travel.art/` -> requested cultural tool | `find_museum_guide` at 11 | `find_museum_guide`, `find_art_events`, `find_layover_itinerary`, `recommend_art_trip` at 12 |

These are separate domain-scoped bindings, not both servers attached to both
agents. At 07 verify Weather's final binding before release and CH01 channel
use. At 14 independently release Cultural and verify Weather's unchanged
release/dependencies, reusing valid evidence rather than re-releasing it.
The hosted workflow at 15-16 calls the two released specialists, not their
MCP servers directly.

## Configure one approved candidate

1. Use the selected endpoint and tool fragments in MCP-SERVICES.md. Resolve
   metadata needed for configuration as part of that work, not a standalone
   connectivity test or participant discovery exercise. Local discovery, if
   needed, is not Microsoft Foundry execution evidence. Establish runtime
   access through the first useful forecast or museum-guide request.
2. Verify Azure CLI availability/sign-in, the actual request identity, exact
   project access and current operation permission using COACH.md and the
   supported skill/API route. The [shared runner](runner/README.md) supports
   the selected public direct-MCP definitions; do not broaden its URL checks.
3. Explain the exact agent/version, endpoint, allowlist, unchanged resources,
   public/synthetic data flow and possible costs. Obtain current-step approval
   before creating the candidate. A configuration approval does not authorize
   a paid model test or any proposed tool call.
4. Attach the current specialist's [first-tool fragment](MCP-SERVICES.md#first-tool-configuration)
   to a new candidate. Retain `server_url`, an unambiguous `server_label`,
   the explicit `allowed_tools` and `require_approval: "always"`. The participant's
   later Playground Auto approve choice does not establish a saved
   `require_approval: "never"` policy or permission on another route. Do not add a
   `project_connection_id`, bearer token, API key or authorization header:
   neither selected public upstream service needs an authentication connection.
   Microsoft Foundry project and consumer authentication remain separate.
5. Independently read back the saved candidate, then guide one read-only
   participant inspection using [APP-GUIDE.md](APP-GUIDE.md#before-adding-a-direct-mcp-tool).
   Verify URL, tool names, allowlist and native approval policy, not just the
   display name. Preserve model, governing instructions, previous versions
   and the other specialist.

At 05/12 expand only that candidate's direct allowlist to its four approved
tools, after schema discovery and separate approval. Keep the same server URL
and label; do not create an unused saved project connection to demonstrate
reuse. Review the skill references against the actual upstream tool names.
This path has no Toolbox-qualified tool-name mapping or mutable Toolbox default.

## First use and permission

Run the existing C/S/P cases and [T01-T03](TESTS.md#foundry-tool-management)
on the actual current candidate/path, sharing exchanges for overlapping
assertions rather than adding model prompts.

- At 04/11, the participant sends the first useful prompt in the exact agent's
  Playground. Follow [the first-use permission flow](APP-GUIDE.md#first-tool-use-in-the-playground):
  explain Approve, Deny and Auto approve when the prompt appears, then let the
  participant select Auto approve for the displayed permitted-tool scope.
  Record the actual choice, scope and observed execution. Do not run a separate
  denial exercise; if a participant actually declines, preserve that decision.
- Continue to the answer and correlate the actual tool execution, arguments,
  result, source/available timestamps and grounded answer. Share this exchange
  with C01/C02 and T01 rather than sending a coach-side duplicate.
- On the coach's SDK/runner route, a native `mcp_approval_request` still needs
  the participant's decision for that exact tool and arguments. The runner
  requires `store: true`, stops at pending approval and needs a separately
  approved exact continuation plan. A portal choice is not transferable
  permission. Retain the same supported response/Conversation context; do not
  replay a prompt or approve a different request to recover missing context.
- Deny means the operation is not authorized. Explain that meaning without
  making it a specialist participant drill. If denial occurs, verify no denied
  execution or invented result before continuing; fixture coverage must be
  labeled and never described as an observed upstream outage.
- Check the current-stage effective allowlist and domain isolation. A server
  may advertise additional tools, but the agent must only be able to call its
  selected tools; do not claim the public server hides every unselected schema.
  Prompt instructions alone are not enforcement. Never execute an unauthorized
  upstream call as a negative test.

Use C03a for unsupported input at 04/11. Share C03b's isolated tool/service
failure with the skill partial-failure case at 05/12, not an extra first-use
approval/denial test.

Weather checkpoint 04 includes the first full trace walkthrough; Cultural 11
reuses that navigation with its own tool and evidence. Saving a definition,
portal visibility, local discovery and an agent saying it used a tool are
not runtime proof. Missing native approvals, unreachable services, unsafe
restrictions or uncorrelated results block the affected gate. Do not disable
approval or silently change the endpoint, runtime, identity or model.

Before release, verify actual consumer-path and required channel behavior.
Anonymous upstream services remove upstream credential setup, not the need
for Microsoft Foundry authorization, trusted Conversation/memory mapping,
per-call decisions or CH01/CH02 evidence. This documentation revision does
not claim a newly completed live rehearsal.

## Evidence, rollback and existing participants

Use the participant's chat decisions for the selected scope and inputs.
Include the direct integration type, server URL/label, selected names,
agent/version, approval policy and actual evidence references in the normal
checkpoint handoff. Retain discovery/read-back and runtime artifacts separately;
do not copy participant input into `tool_assets`, `capabilities` or another
progress ledger. Report runtime restrictions/approval readiness truthfully;
never store credentials or sensitive transcripts.

An immutable agent candidate pins its binding and allowlist, not the public
provider's implementation. External services can change or become unavailable;
retain dated schema/source evidence and revalidate affected behavior.
Rollback restores the retained candidate, not an upstream service version.

For any older curriculum, including v9, ask before migration. Preserve all
attempts, releases, channel evidence, preferences, legacy connection/Toolbox
metadata and cloud resources. Existing Toolbox-path results do not prove the
new direct path. With consent, approve each changed binding separately and
mark only affected downstream evidence unmet; do not re-run unchanged setup,
baseline or Conversation tests merely to change the curriculum label.
Older direct-MCP results may be reused only when the exact retained
configuration, path, identity/scope and required assertions still match.
Keep CH01 at 07 and CH02 at 16; endpoint-only evidence cannot pass either.
Curriculum authoring neither migrates nor resumes a participant.
