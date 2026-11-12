# Reusable Foundry tools and Toolboxes

This is the core tool-management path, not an optional extra lesson. Keep
participants in the GitHub Copilot app, with read-only Foundry inspection and
participant-run agent tests. VS Code is not required. The coach uses the
installed Foundry skill and currently supported APIs for approved operations.

## Explain the three objects

- A **tool** performs an operation: the Weather MCP server exposes
  `weather_forecast`, for example.
- A **configured Foundry tool connection** saves the remote server's address
  and connection settings in the participant's project for reuse. Registering
  it does not host the public server, attach it to every agent, or prove that
  any tool ran. An MCP server connection can expose several individual tools.
- A **Toolbox** is a versioned, centrally managed collection exposed through
  a Foundry MCP endpoint. An agent consumes that endpoint rather than wiring
  each upstream service separately. A **skill** is different: it guides how
  to perform a task and does not grant tool access.

The public upstream services in [MCP-SERVICES.md](MCP-SERVICES.md) need no
credentials. Foundry project connections and Toolbox endpoints still require
the appropriate Foundry permissions and authentication. Do not send a Foundry
bearer token to either public upstream endpoint.

## Explain the attachment before opening the picker

Before asking a participant to use an agent's tool-adding control, explain:

> We are connecting the agent to a Microsoft Foundry Toolbox, not directly
> to the public Weather MCP server. The route is agent -> pinned Toolbox
> version -> Weather MCP server -> `weather_forecast`. The Toolbox itself
> exposes an MCP endpoint, so its agent attachment can appear as an MCP tool,
> not as a separate Toolbox card. The saved URL and authentication connection
> distinguish the two routes; the display name alone does not.

| Saved agent setting | Direct upstream attachment | Intended Toolbox attachment |
|---------------------|----------------------------|-----------------------------|
| `server_url` | Public MCP server URL, such as `https://weather.datakoot.com/mcp` | Verified Microsoft Foundry project URL containing `/toolboxes/<name>/versions/<version>/mcp?api-version=v1` |
| `project_connection_id` | Upstream connection's verified project-local reference | Separate Toolbox-authentication connection's verified project-local reference |
| Allowed tools and approval | Must not be assumed from instructions or a connection name | Exact discovered qualified tool names and explicit per-call approval, verified in the saved candidate and later at runtime |

Supply the participant's actual approved values before any edit. Explain
which route the coach or participant will execute, what remains unchanged,
and what the independent read-back will prove. For Cultural Travel at 11,
give a short reminder of the same distinction using its own server, Toolbox
and exposed tool name; do not repeat the full lesson.

Do not assume **Add** offers a Toolbox selector. In a participant-guided
session on **2026-10-30**, the picker offered direct tools only. An earlier
save contained no tools; another saved the public upstream connection rather
than the intended Toolbox. A separately approved SDK operation then saved a
Toolbox-backed candidate, independently read back with its pinned URL,
authentication reference, forecast-only allowlist and approval-always setting.
The participant reported seeing the resulting Toolbox attachment in Tools.
These are observations from one project, not universal portal behavior or
runtime evidence.

An observed native Toolbox picker or a successful save does not resolve the
authentication preparation blocker below. Inspect approval settings at both
layers independently: an inner `always` setting does not establish that the
outer agent binding retained human approval. Stop before tests if either
effective setting is unsafe or unknown; an instruction to ask permission is
not a native approval request. Correcting a binding requires its own approved
candidate change and affected runtime checks, not an automatic retry or a
direct-upstream substitute.

If the picker only offers direct tools, explain that limitation immediately.
Do not ask the learner to hunt for a nonexistent option, select the upstream
as a substitute, or repeatedly save candidates to discover the UI behavior.
Use verified UI controls if available; otherwise explain and obtain separate
approval for the rehearsed, coach-executed SDK/API attachment route below.
No VS Code or participant-written client is required. After independent
read-back, guide one read-only inspection of the exact resulting agent version.
Configuration approval does not authorize a model request, tool execution or
publication.

## Incremental path

| Checkpoint | Current-step change | Observable evidence |
|------------|---------------------|---------------------|
| 04 | Register the Weather server once as a reusable project tool connection; reference it in a Weather-only Toolbox selecting only `weather_forecast`; authenticate and attach the Toolbox's verified version-specific endpoint to a new Weather candidate | Upstream connection and separate Toolbox-authentication connection read-back; one-tool Toolbox discovery; agent binding and runtime identity; actual approval, denial and forecast trace |
| 05 | Reuse the same upstream connection in a new Weather Toolbox version; expand its approved allowlist to forecast, geocode, current and alerts, and update the agent binding and reviewed skill | Same upstream connection identity; four selected tools at both layers; verified exposed-name mapping; S01 routing evidence |
| 07 | Verify the existing Weather Toolbox binding and dependencies before the first release tests; no planned Toolbox migration | No direct bypass; current runtime access and approval evidence; the already-required final regressions and P01-P03 cover this Toolbox-backed candidate/path |
| 11 | Register travel.art as a reusable project tool connection; explain Toolbox management more fully and apply the familiar pattern to a Cultural-only Toolbox version containing only `find_museum_guide`; attach its version-specific endpoint to Cultural | Connection and Toolbox read-back, runtime identity access, one-tool discovery, approval and C02 trace through the Toolbox |
| 12 | Create a reviewed Cultural Toolbox version exposing the four selected cultural tools; update only Cultural's candidate to that version and add its skill | New Toolbox version and agent binding; S02 proves routing without Weather access |
| 14 | Release Cultural after its final-path tests; verify both existing specialist releases and pinned dependencies for handoff | Cultural release evidence and current read-only Weather binding/version checks; no planned Weather migration or second Weather release cycle |

Weather's first release at 07 is already Toolbox-backed and stays unchanged
while Cultural is built. Introduce the Toolbox boundary, version and
approval requirements with the first tool at 04; deepen management and
independent practice at 11.
Finalize Weather's binding before running its already-required final suite,
so those tests cover the actual release path once. Earlier direct-path passes
do not pass the changed path. Share overlapping assertions in one approved
batch; do not test a direct candidate for release and then migrate it.
At 14 reuse valid evidence for the unchanged Weather release and verify current
metadata; perform the required two-agent comparison, not another full Weather
suite merely for handoff. A real dependency/version/identity change still
requires affected regressions. Formal orchestration and contracts start at 15.
Rehearse the full route within the core agenda before claiming time savings.

Use **two domain-scoped Toolboxes**, not one mixed collection with a prompt
telling each agent to ignore the other domain. Reuse the tool connection
across its initial integration and its Toolbox, not the other specialist's
weather/cultural capabilities. No third demo agent or extra model deployment
is needed to teach reuse.

## Prepare the supported route before teaching

**Authentication references rechecked 2026-11-03; no live operations performed
in that review.** Earlier 2026-10-30 evidence covers one project's saved-connection creation,
forecast-only Toolbox version, developer-authenticated `tools/list` and
SDK-created prompt-agent Toolbox binding have been independently read back.
The participant reported seeing that attachment in the agent's Tools area;
a portal Toolbox-add route has not been verified. Full prompt-runtime
approval/denial, forecast execution and an end-to-end curriculum rehearsal
remain unverified; do not describe configuration read-back or portal
visibility as runtime success.
The installed skill describes `RemoteTool`
project connections for custom MCP servers; current Microsoft documentation
supports Toolbox MCP integration for prompt agents. Neither is proof that a
specific participant's region, API, SDK, identity or portal supports the route.

**Preparation blocker:** a supported managed prompt-agent-to-Toolbox
authentication recipe has not been established. The
[user-delegation reference](https://learn.microsoft.com/azure/foundry/agents/how-to/configure-user-delegation#configure-userentratoken)
restricts `UserEntraToken` to its supported targets (or the documented A2A
compatibility path); it does not list a custom Toolbox endpoint. The
[MCP integration reference](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)
describes Microsoft Entra credentials for Toolbox access, but that and a
developer bearer-token sample do not establish token acquisition by a managed
prompt agent. Do not infer support from MCP compatibility, a pinned URL or an
audience of `https://ai.azure.com`. Nor does the custom-MCP
`AgentOnBehalfOfUser` guidance establish a working Toolbox-specific replacement.
Before offering any authentication connection write or agent attachment,
the facilitator must supply a current supported recipe for the exact
caller/runtime, target, auth type, audience/scopes and operation permissions,
then rehearse it under separate explicit approvals. If unavailable, explain
this blocker briefly, preserve existing evidence and leave T01-T03's affected
runtime gates incomplete. No role grants, speculative versions, paid diagnosis
or silent direct-MCP fallback are authorized by this document.

During facilitator preparation, record a supported, rehearsed recipe for:

1. Registering and reading back an anonymous custom MCP project connection.
   Discover the exact project resource ID and current connection schema;
   never guess IDs or copy a credential-bearing example. Check for an existing
   matching owned connection before proposing creation. Do not create a
   duplicate or mutate a shared connection to test availability.
2. Referencing that saved upstream connection inside the Weather Toolbox from
   checkpoint 04. Verify the supported reference semantics for anonymous
   connections; a copied URL beside an unused saved connection is not reuse.
3. Creating/reading Toolbox versions, obtaining the actual version-specific
   consumer endpoint, and attaching that endpoint to an ordinary prompt agent.
   Do not derive an endpoint or connection ID from a display name.
4. Authenticating the prompt agent's runtime identity to Foundry Toolbox.
   Developer access is not runtime access. Check exact operation permissions
   for connection management, Toolbox management and invocation separately.
   Role assignments are not included in an attachment approval; obtain a
   separate scope/approval or involve the facilitator if access is missing.
5. Restricting the **effective discovered and callable tools** at both layers:
   selected upstream tools inside the domain Toolbox and the supported agent
   binding. Discover actual exposed names; they may be qualified differently
   from upstream names. Check the skill's routing references against them.
6. Preserving human approval for each actual upstream invocation through
   Toolbox, including inspecting arguments and denying a request. Do not
   assume an outer `call_tool` approval covers arbitrary inner operations.
   The documented Toolbox `require_approval` setting is returned as tool
   metadata; the MCP endpoint itself does not block `tools/call`. The consuming
   runtime must enforce it. Verify this with the actual prompt-agent runtime,
   not merely by reading back `"always"`, and distinguish human approval from
   server-side authorization.
   Avoid tool search in the introductory route unless required by the
   supported runtime; if required, verify that it cannot discover or call
   excluded tools and make the specific upstream operation visible.

If any part is unsupported or unverified, record the exact blocker and stop
that gate. Do not turn a direct URL integration into a claimed reusable-tool
or Toolbox pass. A facilitator may agree an explicitly partial route, with
these learning gates still incomplete. Do not broaden roles, disable approvals,
or install a different runtime to conceal a failure.

## Attachment requirements and failure guards (not a verified auth recipe)

Keep the two connections distinct:

1. **Upstream connection:** the existing anonymous `RemoteTool` record points
   to the public Weather MCP server. The Toolbox's `MCPToolboxTool` references
   its verified project-local connection name, retains `server_url`, selects
   only the current lesson's upstream tools and requires approval.
2. **Toolbox-authentication connection:** a separate `RemoteTool` record points
   to the verified, version-specific Foundry Toolbox endpoint, **only after
   the preparation blocker above is resolved**. Do not prescribe
   `UserEntraToken` with audience `https://ai.azure.com` as a working recipe.
   If a supported route requires an audience, set and independently read back
   its actual authentication field, not just metadata. Metadata alone does not
   configure token acquisition: a previously observed metadata-only connection saved
   successfully but failed at invocation with "Missing required query parameter:
   audience". Fixing that field is not proof the target supports the auth type.
   Follow the current supported schema and establish whether the actor uses
   the caller's delegated identity or the agent's own identity; do not conflate
   them. Explain the verified identity behavior and obtain approval before
   creating it. Never reuse the anonymous upstream connection for
   this authenticated endpoint or forward a Foundry token to the public server.
3. **Agent binding:** replace the candidate's direct public-MCP binding with
   the Toolbox endpoint in `MCPTool.server_url`, plus the Toolbox-authentication
   connection's verified project-local name in `project_connection_id`.
   Discover the exact exposed names using authenticated `tools/list`; apply
   them to the agent allowlist and skill/instruction references. For example,
   the observed Toolbox exposes `weather_intelligence___weather_forecast`,
   not bare `weather_forecast`. Preserve all unrelated instructions/model
   settings and prior versions. Pin the verified version, not a mutable default.

`project_connection_id` does **not** replace an ordinary MCP routing field:
exactly one of `server_url`, `connector_id` or `tunnel_id` is required. Do not
generalize a connection-only CLI Toolbox recipe into a reference-only
`MCPTool`. SDK serialization and agent save/read-back can accept a definition
that invocation later rejects. Do not automatically convert an ARM resource
ID into the binding reference; follow the current API's verified name/ID
semantics and current official prompt-agent example.

Before any write, verify the actual caller, project access and current
operation permission. Inspect the agent's real runtime principal and its
required project access independently. A missing role is a separate approval,
not part of attachment. User-token passthrough also requires access for the
actual caller. Role read-back alone is not effective runtime access.
Check for matching existing owned connections/Toolboxes before creation;
never overwrite shared settings or create throwaway write probes.

Verify separate facts separately: connection creation, Toolbox definition,
authenticated effective discovery, agent definition, portal rendering and
prompt-runtime execution/approval. An empty portal Tools panel despite a
saved tool is an unresolved rendering/integration discrepancy, not proof of
runtime failure or success. Preserve failed attempts, stop speculative
version creation, and obtain separate paid-call approval for runtime diagnosis.
An audience repair and successful read-back establish configuration only:
do not claim runtime authentication, approval or forecast success until a
separately approved test produces that evidence.

For an approval-capable prompt-agent test, create and retain a managed
Conversation before the initial request and record its identifier alongside
the exact agent version, response and approval-request identifiers. Continue
the approved or denied tool request in that same Conversation using the
current supported API. A `store=false` response without a Conversation is not
a verified resumable approval context. If that context is missing, stop;
obtain separate approval for a replacement test rather than silently replaying
history, sending a new prompt or retrying the original call.

## Coach execution and inspection

Before each resource operation, follow COACH.md's CLI/sign-in, actual request
identity, direct project access and operation-permission checks. Use current
skill workflows and discover available tools; this guide is not an executable
API schema. The [shared runner](runner/README.md) only supports direct public
MCP definitions: it does **not** register connections, manage Toolboxes or
authenticate their endpoints. Use the rehearsed supported skill/API route for
these steps; never remove its URL validation or disguise Toolbox as a public
server to force a runner plan through.

Explain the current object, its name and project, scope of change, unchanged
agents/releases, external data flow and possible Foundry charges before one
bounded approval. Registering a connection, creating a Toolbox version,
changing an agent binding, granting a role and running tests are distinct
operations; approve only the current explained scope. Do not infer approval
for all of them from "connect the tool."

Teach the portal route once: start at https://ai.azure.com/, select the
participant's exact confirmed project, then use **Build > Tools** for the
configured connection. The installed skill describes **Connect a tool** there.
These are reference-based labels, not observed participant controls. The
facilitator must record the current Toolbox inspection route and labels before
delivery; do not invent a Toolbox tab or require a VS Code extension. If the
route differs, ask what the participant sees and offer the approved
service-returned read-back review instead, recording the portal limitation.
For the agent binding and runtime trace, use APP-GUIDE.md's agent route.

After each approved write, independently read back the connection, Toolbox
version and/or agent candidate actually changed. Guide one participant
inspection and collect one useful observation. Registration/listing alone
cannot pass runtime integration. Use [T01-T03](TESTS.md#foundry-tool-management)
alongside the existing C/S/P cases, sharing the same exchanges where possible.
Do not add calls just to demonstrate the same fact twice.

## Versioning, evidence and existing progress

Pin a tested Toolbox version-specific endpoint for each agent. Record the
connection ID/target, Toolbox name/version/returned endpoint, selected upstream
and exposed names, agent name/version/binding, runtime identity, approval
behavior, skill revision and evidence in ignored local progress. Do not store
credentials. A default endpoint can change behavior without changing agent
source; explain this risk rather than promoting defaults as a teaching demo.

Treat a connection target/settings change or Toolbox version/binding change as
a behavior change requiring applicable current-path regressions. Reusing an
unchanged saved connection does not reuse an old agent's runtime pass.
Stable-agent rollback alone does not undo a mutable shared dependency:
retain the tested dependency versions and review affected consumers before
updates or cleanup.

This tool-management path is retained in curriculum `two-specialists-workflow-v9`.
For earlier progress, ask before migration, preserve all historical attempts,
and record T01-T03 as unmet until evidenced. Do not reset the participant's
agents or automatically award new gates from direct-MCP evidence. Version 8
moves Weather Toolbox setup from 07 to 04 and expansion into that Toolbox at
05; 07 verifies the existing binding rather than creating it. Explain this
change and obtain migration approval for earlier progress. The
participant session paused during authoring stays paused and unchanged.
Version 9 additionally requires Weather and workflow channel publication/use
at 07/16; see PUBLISHING.md. These do not replace tool-management evidence.

## Official references

- [Toolbox concepts and supported integrations](https://learn.microsoft.com/azure/foundry/agents/concepts/toolbox-overview)
- [Create and manage Toolbox versions](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/toolbox)
- [MCP integration, including prompt-agent Toolbox examples](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)
- [Foundry project connection REST reference](https://learn.microsoft.com/rest/api/aiservices/accountmanagement/projects-connections)
