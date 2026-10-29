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

**Documentation checked 2026-10-28.** One project's saved-connection creation,
forecast-only Toolbox version and developer-authenticated `tools/list` have
been observed. Full prompt-runtime approval/denial, forecast execution,
portal rendering and an end-to-end curriculum rehearsal remain unverified;
do not describe configuration read-back as runtime success.
The installed skill describes `RemoteTool`
project connections for custom MCP servers; current Microsoft documentation
supports Toolbox MCP integration for prompt agents. Neither is proof that a
specific participant's region, API, SDK, identity or portal supports the route.

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

## Correct attachment recipe and failure guards

Keep the two connections distinct:

1. **Upstream connection:** the existing anonymous `RemoteTool` record points
   to the public Weather MCP server. The Toolbox's `MCPToolboxTool` references
   its verified project-local connection name, retains `server_url`, selects
   only the current lesson's upstream tools and requires approval.
2. **Toolbox-authentication connection:** a separate `RemoteTool` record points
   to the verified, version-specific Foundry Toolbox endpoint. The current
   official prompt-agent example uses `UserEntraToken` with audience
   `https://ai.azure.com`. Set the required authentication field
   `properties.audience`, not only `properties.metadata.audience`, and
   independently read back the authentication field. Metadata alone does not
   configure token acquisition: the observed metadata-only connection saved
   successfully but failed at invocation with "Missing required query parameter:
   audience". Follow the current connection schema; where its example includes
   both fields, preserve both. See [user-delegation connection properties](https://learn.microsoft.com/azure/foundry/agents/how-to/configure-user-delegation#configure-userentratoken)
   and the [prompt-agent Toolbox attachment example](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol).
   This method uses the incoming caller's Microsoft identity on their behalf;
   it is not authentication as the agent's own identity. Explain this distinction
   and obtain approval
   before creating it. Never reuse the anonymous upstream connection for
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

This tool-management path is curriculum `two-specialists-workflow-v8`.
For earlier progress, ask before migration, preserve all historical attempts,
and record T01-T03 as unmet until evidenced. Do not reset the participant's
agents or automatically award new gates from direct-MCP evidence. Version 8
moves Weather Toolbox setup from 07 to 04 and expansion into that Toolbox at
05; 07 verifies the existing binding rather than creating it. Explain this
change and obtain migration approval for earlier progress. The
participant session paused during authoring stays paused and unchanged.

## Official references

- [Toolbox concepts and supported integrations](https://learn.microsoft.com/azure/foundry/agents/concepts/toolbox-overview)
- [Create and manage Toolbox versions](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/toolbox)
- [MCP integration, including prompt-agent Toolbox examples](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)
- [Foundry project connection REST reference](https://learn.microsoft.com/rest/api/aiservices/accountmanagement/projects-connections)
