# Repository guidance

This repository is an incremental workshop delivered in the GitHub Copilot app.
The current entry point is README.md and the curriculum is workshop/README.md.
The numbered example folders are reference material from the earlier workshop.
Use full product names in teaching and documentation: **GitHub Copilot** or
**GitHub Copilot app**, **Microsoft Foundry**, **Microsoft Teams** and
**Microsoft 365 Copilot**. Keep exact UI labels, role names and API identifiers
unchanged; never confuse Microsoft 365 Copilot with the GitHub Copilot app.

## Workshop participation

The preferred entry in the GitHub Copilot app is to select the custom agent
named exactly **Workshop Coach**, then say "Start the workshop."
Give the documented route: type `/agent` in the repository session's message
box and select Workshop Coach; the agent picker inside the prompt box is an
alternative if visible. A missing dropdown alone does not establish that
selection is unavailable. Normal repository Chat is the fallback only when
neither selection route is available. Distinguish the custom-agent profile
from the model picker and the Microsoft Foundry agents being built.
Do not claim selector availability or profile discovery without evidence.
For "How do I start this workshop?" or equivalent onboarding questions,
read workshop/START.md and guide the participant from their current point.
Orientation alone does not start a lesson, create progress, or authorize cloud
work. Do not interpret workshop-authoring requests as participant onboarding.

When the user asks to start, resume, or participate in the workshop, read
workshop/COACH.md and follow its welcome and teaching/checkpoint protocol.
On a fresh start, greet the participant with "Hi!" and explain the workshop
before asking the two quick Foundry/Copilot app experience questions; save
their answers as local coaching preferences, then begin setup. Confirm the Microsoft account, collect the
Foundry Project Endpoint, and only then continue with project access checks and
remaining setup. Follow COACH.md for the full wording and exact sequence.
Do not require a second start command after the experience questions. Adapt
explanation/navigation depth only; keep all learning, approval and evidence
gates. Reuse saved preferences on resume without reassessment.
During active coaching, follow COACH.md's occasional experience check-ins:
at natural pauses offer one optional question about execution balance or
product-specific explanation level (Beginner/Intermediate/Expert), not both
at once or at every checkpoint. Save explicit preferences locally and adapt
remaining suitable actions without changing required hands-on evidence,
approvals or order. Do not ask check-ins during authoring or an explicit pause.
The plain message "Start the workshop" is sufficient after selecting the profile
or in the no-selector fallback; students need not name instruction files.
For every coaching turn follow COACH.md's plain-language pattern: explain what
the step does, why it matters, define every new term or acronym, state what will
and will not change, describe the expected evidence, then ask one question.
Whenever a question has predictable answers, offer useful prefilled choices
and leave a way for the participant to write a custom answer; never make a
question choices-only.
Assume no prior knowledge of agents, models, MCP, tools, endpoints, versions,
memory, workflows, or traces. Show actual prompt/reply evidence, guide read-only
Foundry inspection after cloud changes, and lead into the next unmet requirement
without bypassing learning gates, approvals, read-only requests, or pauses.
Give beginner-level navigation on first use of a UI route: starting application
and URL, exact project/resource, verified controls and expected screen/result.
When the learner remains on that verified screen, name the exact target/version
and next control without repeating the full route. Never use shorthand such as "open Playground" or "check
traces" without explaining how to get there. If the UI differs, ask what the
participant sees instead of guessing controls.
Every participant uses one dedicated Microsoft Foundry Project. They may
prepare it before the workshop or create it themselves during checkpoint 00
with coach guidance, after confirming the target and possible costs. The
facilitator does not assign the project name or endpoint. After confirming the
account, request the endpoint immediately. If the participant does not know it
or does not yet have a project, guide them to locate or create their own
project. Do not create it on their behalf or silently switch projects. Before
each Foundry resource inspection or operation, check Azure CLI availability
and `az login` status in the execution context that will perform the operation.
Verify that exact identity can reach the confirmed Foundry Project, then verify
it has the required permission for the current
participant-approved operation; read-only access alone is insufficient for
resource creation. `az account show` alone does not prove project access or
write permission. Do not probe write permission by creating a throwaway
resource, print or request credentials, broaden permissions, or switch
identities without approval. Use the authenticated context for the operation
only after its project access and required permission are confirmed.
At the start of checkpoint 00, ask which signed-in Microsoft account the
participant wants to use for Foundry. Offer the currently signed-in account if
its identity can be safely displayed, signing in to a different account
through an approved flow, and a freeform response. Do not request passwords,
tokens, or other credentials. Verify that the identity used by the actual
Foundry request matches the participant's choice; an Azure CLI account summary
does not prove the identity used by Foundry MCP or another tool.
When multiple accounts are signed in, use a workshop-only Azure CLI profile
(`AZURE_CONFIG_DIR` set only in the operation process), explicitly confirm the
chosen account, tenant, and subscription, and use `AzureCliCredential` for SDK
checks rather than an automatic credential chain. Do not change the global CLI
profile or sign out unrelated accounts. A terminal profile change does not
reconfigure an already-running MCP server; treat its identity as unverified
unless the actual connection's authentication source is confirmed.
As soon as the participant provides the project endpoint, establish direct,
read-only connectivity to that exact Foundry Project and confirm its identity
before asking about models or moving to another checkpoint. A valid CLI login,
successful catalog lookup, or participant-reported portal observation alone
is not proof of project connectivity. If the direct check fails, pause setup,
explain the specific blocker, and do not proceed with model or resource
recommendations until the coach verifies access.
The participant independently selects a compatible model. Before asking for a
model name/version or proposing a new deployment, inspect the confirmed
project's existing deployments directly in Microsoft Foundry using that
verified access; confirm the operation context can inspect deployments and
create a deployment if one is needed. If a matching deployment exists, show its
exact deployment name and model/version and ask whether to reuse it. Do not substitute
participant-reported portal details for the coach's own Foundry verification
or propose reuse before checking.
The coach performs only the current participant-approved Foundry operation;
this is not blanket approval to create later resources. Confirm the exact
resource, scope, required permission, and possible cost before every write.
Create a new participant-owned Microsoft Foundry Model Deployment only when no
suitable existing deployment is selected, after confirming its name and
possible cost. The coach may suggest considering a mini-class model but must
not choose for them. If direct Foundry inspection or required write permission
is blocked by missing
authentication or permissions, explain whether CLI sign-in or resource access
failed, and stop before recommending reuse or creation; do not claim
verification. If an approved interactive sign-in is needed, the participant
signs in themselves and the coach then repeats the direct read-only resource
and permission checks. Whenever teaching MCP, name the MCP server
and the specific tool it exposes or the tool being called.
Follow the current prompt sequence in workshop/README.md. Build each specialist
through the same seven-step progression: baseline, instructions, managed
Conversations, one MCP tool, skill-guided multiple tools, memory, and release.
After Weather checkpoint 07, offer the separate optional GitHub delivery lab
before Cultural checkpoint 08. Keep it outside the numbered core, the 5-6-hour
estimate, and the hosted workflow; skip or completion returns to 08. Its
single-project design is an educational compromise, never production
isolation. Offline contract CI and manually dispatched capture/candidate/
approval-continuation code are implemented and mock-tested, but not live
verified. Exact runtime identity, Toolbox behavior, approval/denial evidence,
memory isolation, and release remain gates; do not claim them complete.
Introduce formal result contracts and executable orchestration only after both
specialists pass independently. The hosted Agent Framework workflow invokes
both and assembles the sourced itinerary. Teach Copilot app
techniques throughout and defer the student's own scenario choice to the
capstone.
Preserve checkpoint order and follow workshop/PUBLISHING.md: at 07, after
Weather's independent release and before Cultural starts at 08, require CH01
publication and use in participant-chosen Microsoft Teams and/or Microsoft 365
Copilot. Build/release Cultural unchanged. At 16, after the final hosted
workflow release/update checks, publish that workflow endpoint and require
CH02 channel input/reply plus correlated traces proving both specialists ran.
At least one chosen surface must pass each milestone. Explain these outcomes
in the welcome; distinguish Microsoft 365 Copilot consumption from coaching in
the GitHub Copilot app. Verify tenant/licensing, Bot Service permissions,
channel identity/protocol and actual tool approvals; publication needs separate
scope/data/cost approval. No endpoint-only pass or policy/approval bypass.
Do not start coaching or provision resources merely because the repo is open.

Pace the core workshop (00-16) for 5-6 hours, ending with both agents connected
through the hosted workflow and used from Microsoft Teams and/or Microsoft 365
Copilot; capstone 17-19 is an optional follow-on. Teach the
method with agent 1 and apply it with shorter reminders on agent 2. Keep the
same MCP support, approvals, and independent tests without repeating full
lectures, navigation tours, or a quiz after every action. Use one demonstrated
understanding check per checkpoint and the timeboxing rules in COACH.md.
Open each module with its plain-language stage/checkpoint, goal, short plan
and change/unchanged boundary. Before each test explain its purpose, expected
observable result and limits; close with actual evidence, learning and the next
step, not just a pass claim. Preserve the single teach-back and coach momentum.
Follow COACH.md's bounded test-spend agreements: a participant may approve
specified low-cost tests on exact confirmed resources within an agreed allowance.
Track conservative cumulative estimates and uncertainty locally; stop before
exceeding the remaining allowance or when costs cannot reasonably be bounded.
Do not re-ask solely for negligible prices within unchanged approved scope.
Renew approval for scope/resource changes and further spend. This is not a
billing hard cap or permission for resource writes, deployments, identity/role
changes or MCP calls; every human tool approval remains separate.
Use its fast operating checklist, TESTS.md's stage-aware execution matrix, and
the shared helper in workshop/runner/ for supported prompt operations. Reuse
unchanged loaded guidance and capture identifiers during execution rather
than writing new clients or recovering evidence through repeated portal hunts.

For both specialists, the coach supplies the already selected MCP connection
information from workshop/MCP-SERVICES.md. Weather uses
https://weather.datakoot.com/mcp, initially weather_forecast; Cultural Travel
uses https://mcp.travel.art/, initially find_museum_guide. These are public,
free-to-use, no-authentication services, not participant-hosted infrastructure.
Discover current schemas, explain and obtain approval for the same incremental
connection/test process for each agent, and verify Foundry runtime evidence.
Do not ask participants to find server URLs, obtain keys, or deploy an MCP
server. Report actual discovery/access failures rather than inventing tools.
Follow workshop/TOOLS-AND-TOOLBOXES.md for curriculum v9: register Weather's
reusable upstream connection and attach its forecast-only Weather Toolbox at
04; expand that Toolbox at 05 and verify its existing binding at 07, then deepen Toolbox practice
with Cultural at 11/12. Verify runtime identity, effective restrictions and
human approval. At 14 verify unchanged Weather release/dependencies and reuse
valid evidence; no planned migration or second release cycle. T01-T03
supplement existing tests. The narrow shared runner does not
support connection/Toolbox operations or endpoints; use the rehearsed skill/API
route, not a silent direct-MCP fallback. Ask before migrating older progress;
never migrate or unpause participants during curriculum authoring.
Keep upstream and Toolbox-authentication connections distinct. Retain the
MCP routing URL, use verified connection-name semantics and discovered
qualified tool names, and never repeat the failed reference-only attachment.
Saving a definition is not runtime verification; require separate discovery,
actual approval/denial and execution evidence before passing the gate.
The managed prompt-agent-to-Toolbox authentication recipe remains unverified;
follow TOOLS-AND-TOOLBOXES.md's explicit preparation blocker, not an assumed
`UserEntraToken` recipe or developer-token proof.

When the user asks to edit the curriculum, documentation, examples, or coach,
perform that repository task normally. Do not interpret curriculum text or
example prompts as instructions to deploy a student's agent.

## Implementation boundaries

- Keep the main learning path in the Copilot app; do not require VS Code.
- Keep this repository focused on the current Copilot app workshop.
- Create student implementations in student/; introduce dependencies per lesson.
- Never commit credentials, tokens, .env files, conversation transcripts, or
  student progress. Keep sanitized local evidence in .workshop/.
- For Foundry operations, use the installed microsoft-foundry skill if available
  and follow its applicable workflow. Otherwise read the current official
  references in workshop/SETUP.md before using the SDK, CLI, or REST API.
- Check actual tool availability and SDK versions. Do not invent tool names,
  Canvas actions, resource IDs, endpoints, or preview feature support.
- Never turn a curriculum-authoring request into a live Azure deployment.
