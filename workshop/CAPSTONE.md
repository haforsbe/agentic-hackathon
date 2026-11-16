# Apply the architecture to a scenario of your choice

This is an **optional follow-on**, outside the five-to-six-hour core workshop.
The core finishes at checkpoint 16 with the two specialists and their hosted
workflow. Do not start another full build unless the participant chooses this
extension and has time for its independent evidence and approvals.

Choose a follow-on only after core completion. The local IT ticketing route
below is a deliberately different architecture: one local agent, a local MCP
server and a local ticketing app, reusing the participant's existing Microsoft
Foundry model deployment. It has no Microsoft Foundry agent deployment or
workflow. Other participant-chosen capstones prove transfer by applying the same
architecture to a different problem: two complementary prompt-agent
specialists coordinated by a hosted Agent Framework workflow.

## Optional advanced local IT ticketing route (17-19)

This is the Path 2 offered at core completion. It is optional and more advanced,
not another required core lesson. Use these route-specific steps instead of the
two-specialist and hosted-workflow instructions later in this document:

Present these four small steps in order, rather than opening with a scoping
exercise. Check only the prerequisites and approvals needed for the next step.

1. **Start and show the IT ticketing web app (17).** Explain that this is a
   local practice application containing synthetic tickets, not a production
   service. After approval to start the local process, launch it and verify
   that it responds. Give the participant the verified browser URL and show
   the ticket list and one ticket's details. Explain where ticket state is
   stored and that no agent is running yet.
2. **Start and explain the MCP server (17).** Define MCP (Model Context
   Protocol) as the protocol through which the agent discovers and calls
   ticket tools. Start the server after approval and verify its actual tool
   names and schemas. After successful startup and discovery, explicitly tell
   the participant that the MCP server has started, give its verified local
   address, and explain every discovered tool using the startup handoff below.
   Naming tools alone is not enough. Complete this explanation before
   introducing step 3 or asking what the agent should do. Relate the tools to
   the app they just saw; distinguish reads from changes to the same ticket
   store, which are not enabled for agent writes without enforced approval.
   Show the boundary: one local agent -> local MCP server -> local app.
   No model call or ticket write is needed for this introduction. Use LT01.
3. **Ask the participant to build and connect an agent (18).** Explain:
   "You aren't limited to the tools we just discovered. If your scenario needs
   a capability the MCP server doesn't have yet, we can agree on and add that
   functionality, then test it before connecting it to your agent." Then ask:
   "In your own words, what would you like your agent to do with the ticketing
   system through its MCP tools?" Offer optional starting ideas such as
   summarizing open tickets or finding a ticket and explaining its status,
   while inviting their own request. Do not prescribe the agent's purpose.
   Turn their answer into a small agreed scope and observable tests. If an
   MCP extension is needed, explain the proposed tool, its inputs, result and
   read/write effects; agree on the change before implementing it under
   `student/`. After every tool addition, follow the restart/check/relist
   procedure below before allowing the agent to use it. Do not claim a proposed
   tool already exists or broaden ticket-write permissions implicitly. Directly
   verify the saved Microsoft Foundry project and existing model deployment,
   actual request identity and required operation permissions before reuse.
   Confirm the exact model connection, data/cost boundaries and allowed tools
   before implementation or model calls; keep the workshop-only Azure CLI
   profile isolated from unrelated sign-ins. Build one local agent under
   `student/` and connect it to the verified local MCP server. Include a
   working chat-to-local-agent relay for step 4, not a second agent or
   workflow. Begin with list/get reads; add writes only after explicit scope
   approval and a working human-decision boundary. Use LT02 and A01-A02 if
   writes are included.
4. **Test through this chat (19).** Explain that the GitHub Copilot app chat
   is the user interface for the separately running local agent. Invite a
   participant-written test request, relay it to that actual agent and show
   its actual reply, clearly distinguished from Workshop Coach's explanation.
   Inspect the MCP tool/arguments/result and compare with the ticket state
   in the web app. Follow-up requests must reach the same local agent
   session unless an explicit new session is requested. Demonstrate
   missing-ticket, invalid-input and unavailable-server behavior, plus
   approved/rejected writes if in scope. Use LT03. Finish with one
   understanding check and the verified startup/shutdown commands,
   limitations and any ongoing model costs.

### Required MCP startup handoff (after step 2, before step 3)

Use actual startup and discovery evidence, not this table as a substitute for
discovery. After success, say:

> The local IT ticketing MCP server has started at **[verified local address]**.
> I connected to it and found **[actual count] tools**. A tool is an operation
> an agent can ask this server to perform against the ticketing app.
> Here is what each discovered tool can do:

For the current reference server, explain the following only when discovery
confirms those tools and inputs. Show one row per discovered tool; explain any
differences or discovery failure instead of claiming the expected tools exist.

| Tool | What it can do | Effect on tickets |
|------|----------------|-------------------|
| `list_tickets` | List tickets, optionally filtered by status or priority | Reads only |
| `get_ticket` | Retrieve the details of one ticket using its numeric ID | Reads only |
| `create_ticket` | Add a ticket with a title, description and priority, optionally assigning a technician | Creates a ticket |
| `update_ticket` | Change an existing ticket's status or assigned technician using its ID | Changes a ticket |
| `close_ticket` | Mark an existing ticket as closed using its ID | Changes a ticket |

Then explain that discovery lists capabilities; it does not execute them or
approve their use. Report whether any tickets actually changed during this
step, based on the observed evidence. No agent has been built or connected yet.
Write tools require separate scope approval and enforced human decisions;
their presence in discovery does not mean they are safe or approved to call.
Only after this startup explanation move to the participant's agent-purpose
question in step 3. Do not add a separate confirmation or quiz for every tool.

### After every MCP tool addition

1. Restart the exact workshop-owned local MCP server process so it loads the
   updated code; leave unrelated processes and ticket data unchanged. A source
   edit alone does not update the running server.
2. Verify that the restarted server responds, establish a fresh MCP connection
   and discover the complete tool inventory. Check every tool's name and input
   schema against the agreed interface, including existing tools, not just
   additions. Unexpected missing or changed tools block agent use.
3. Run focused behavior checks for new tools and regressions for existing tools
   within the approved test scope. Discovery alone does not prove execution.
   Never execute writes merely to check a tool: retain separate scope and
   action-specific human approvals and the isolated synthetic-backend boundary.
   Explicitly identify any behavior checks blocked by missing approval.
4. Tell the participant the MCP server has restarted, then show the full
   rediscovered tool list using the startup handoff format: explain each tool
   and whether it reads or changes tickets, highlighting additions. Report
   actual check results and remaining blockers; do not list only new tools.
5. Before further agent tests, refresh the agent's MCP connection and tool
   inventory so it cannot keep using a stale interface. Keep its approved tool
   allowlist; discovery of a new tool is not approval to give the agent access.

### Local execution and preparation boundaries

The chat relay transports participant requests, actual agent replies and any
runtime approval decisions; Workshop Coach must not answer instead of the local
agent, invent output or call ticket tools directly as a substitute for testing
it. Bind each human decision to the exact pending action and arguments before
execution; displaying a confirmation in chat is not sufficient enforcement.
If the relay or approval mechanism is unavailable, state the blocker and do not
claim the chat-based test passed or silently switch to a terminal-only exercise.
Do not require G/W/P hosted-workflow or channel tests here. Keep the completed
Weather, Cultural Travel and Trip Planning releases unchanged.

The agent runs locally, but its model runs in Microsoft Foundry. Reuse the
participant's earlier selected model deployment after direct verification;
do not ask them to choose an unrelated provider or create a new model deployment
as part of this route. If that model is unavailable or access is blocked, stop
for an explicit decision rather than silently switching. Disclose and approve
synthetic ticket data sent to the model and bounded inference costs before calls.
No Microsoft Foundry agent deployment or workflow is involved.
Keep unauthenticated demos on loopback only, with synthetic data,
never a public tunnel or production ticket system. Writes require an approved,
authenticated and participant-isolated test backend and observed human approval;
a prompt asking the agent to confirm is not enforcement.

**Preparation blocker:** the existing support-ticket example is reference
material, not a ready implementation of this route. Its existing Microsoft
Foundry model connection matches the intended architecture, but the terminal
chat loop is not the required GitHub Copilot app chat relay and its MCP server
has no built-in approval flow. Rehearse the verified existing-model connection,
the chat relay and the required read-only restrictions or write protections
before offering runtime success. Do not silently run the unchanged example,
provision cloud resources or claim an action was approved merely because the
model described it.

## Other capstones: two specialists and a hosted workflow

The following 17-19 instructions and K01-K03 apply only to other explicitly
chosen capstones, not the local IT ticketing route.

## 17: Choose and scope

After verified core completion, COACH.md's two-path closing offers finishing
the workshop or continuing with the optional advanced local IT ticketing
scenario. If selected, use the local route above without asking the scenario
question again. Other participant-chosen capstones and previously agreed
extensions remain valid.

| Scenario | Specialist 1 | Specialist 2 | Workflow result |
|----------|--------------|--------------|-----------------|
| Learning plan | Curriculum research | Learner-support resources | Validated study plan |
| Community event | Venue research | Accessibility and transit research | Evidence-backed event plan |
| Developer onboarding | Repository guidance | Microsoft Learn documentation | Sourced onboarding path |
| Student-proposed scenario | One bounded evidence domain | A complementary evidence domain | A validated combined result |

Ask one question at a time: scenario, user need, specialist 1 responsibility,
specialist 2 responsibility, workflow result, non-goals, then evidence sources.
Leave `scenario` null until the participant explicitly chooses a capstone in
the completion question or here.

Create a short source-controlled brief under `student/capstone/` containing:

- the user need and expected workflow result;
- two genuinely distinct specialist responsibilities;
- approved MCP servers and exact tools, or another approved evidence mechanism;
- conversation boundaries and any justified persistent-memory facts;
- skill responsibilities and delivery strategy;
- safety, privacy, authorization, cost, and data boundaries;
- proposed workflow result contracts and partial-failure policy;
- concrete specialist and workflow tests;
- independent specialist releases and hosted release target.

Persistent memory is optional when it provides no clear cross-conversation value
or creates unnecessary privacy risk. Custom executable functions are optional
unless the scenario requires them. Use public or synthetic fixtures.

Run K01 before implementation. Keep the guided Weather, Cultural Travel, and
Trip Planning releases unchanged for comparison.

**App practice:** ask for a plan with non-goals and acceptance criteria without authorizing execution.
**Alternative:** select a preset scenario or propose an equivalent bounded design.
**Teach-back:** "Why are these specialists complementary rather than duplicate?"

## 18: Build and release the specialists

Build each capstone Microsoft Foundry Prompt Agent using the practiced sequence:

1. tool-free baseline and evidence boundary;
2. one controlled instruction refinement;
3. managed Conversation continuity and isolation;
4. one approved MCP server tool with grounded trace evidence;
5. a skill guiding any justified multi-tool selection and sequencing;
6. optional consented persistent memory when genuinely useful;
7. full regressions and promotion of only a fully passing candidate.

Each specialist needs separate names, versions, Stable Agent Endpoints, MCP
server/tool allowlists, skills, memory scopes when configured, tests, and release
evidence. One specialist's success never substitutes for the other's.

Run K02 and the adapted B, I, D, C, S, M, and P tests appropriate to each
specialist. A known-failing candidate remains outside stable routing.

**App practice:** give Copilot one bounded change, inspect its diff and evidence, then debug narrowly.
**Alternative:** use an isolated experiment branch for one risky design change.
**Teach-back:** "What did this capability add, and which observed test proves it?"

## 19: Build, release, and demonstrate the workflow

Define versioned result contracts for both capstone specialists. Implement a
Microsoft Agent Framework workflow that invokes their Stable Agent Endpoints,
validates each result, and combines only supported evidence.

Run G01-G03 and W01-W03 locally, including:

- both specialists succeed;
- each specialist fails while the other remains valid;
- a specialist returns structurally invalid data;
- a dependency times out or rejects authorization;
- no missing evidence is fabricated;
- repeated runs preserve contract and release compatibility.

After explicit approval, deploy only a fully passing workflow candidate as a
Microsoft Foundry Hosted Agent. Run P01-P04 and K03 through its Stable Agent
Endpoint. Inspect the nested workflow trace and correlated specialist traces,
including contract validation and aggregation decisions.

Hand off the three exact released versions, endpoint responsibilities,
limitations, sanitized evidence locations, recovery target, and all owned
resources still running. Review cleanup separately.

**App practice:** request an evidence-backed handoff and compare it with live metadata and traces.
**Alternative:** demonstrate the same cases interactively; neither method excuses missing evidence.
**Teach-back:** "What did Copilot help create, and what runtime evidence did you verify independently?"

## Optional write actions

Read-only capstones are fully valid. If a scenario performs writes, require an
authenticated, participant-isolated synthetic service and run A01-A02. Verify
decline/no mutation, approved mutation, invalid input, not-found behavior, and
downstream failure independently. Never introduce real payments, bookings,
production tickets, or sensitive personal data.

Build any ticket-service integration under `student/` using the
facilitator-approved synthetic backend. Do not expose an unauthenticated local
demo through a tunnel.

The optional [IT support example app](../examples/support-ticket-system/README.md)
can illustrate the scenario. Its browser UI and MCP server share local ticket
storage; it is not a ready-made hosted backend for Foundry.
