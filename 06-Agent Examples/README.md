# Agent Examples: From Idea to Foundry

This final lab contains three open Microsoft Foundry **prompt-agent** challenges and one
implemented MCP application. Examples 01-03 provide instructions and synthetic data for
an agent that you design and build yourself. Example 04 is a complete support-ticket
reference system that you run, inspect, test, and extend with GitHub Copilot.

Examples 01-03 do not use Microsoft Agent Framework or hosted-agent code deployment.
Example 04 uses Agent Framework locally to demonstrate an MCP-backed application; it is
not deployed as a Foundry prompt agent.

## Choose an example

### [Customer Request Coordinator](01-customer-request-coordinator/)

Turn a queue of customer requests into a clear, defensible action plan. This agent finds
the cases that need attention first, explains its priority decisions, identifies missing
information, and prepares professional customer responses. By connecting Notion MCP, the
agent moves from a static demonstration to working with a live request database while
keeping people in control of assignments and status changes.

Choose this example if your company works with customer support, partner service, account
management, warranty cases, or any process where important requests compete for attention.

### [Daily Operations Planner](02-daily-operations-planner/)

Transform an overloaded task list into a realistic day. This agent weighs deadlines,
business impact, dependencies, and available time to recommend what should happen now,
what should move, and what is blocked. Todoist MCP supplies current tasks, while optional
Code Interpreter makes capacity and scheduling calculations transparent and repeatable.

Choose this example if your teams struggle with competing priorities, missed commitments,
context switching, or plans that contain more work than the day can hold.

### [Market Opportunity Researcher](03-market-opportunity-researcher/)

Move from broad market curiosity to evidence-backed opportunities. This agent searches
current sources, compares supporting and contradictory evidence, ranks opportunities, and
makes assumptions visible. Tavily MCP provides live web research, while optional Code
Interpreter supports consistent scoring and transparent financial scenarios.

Choose this example if your company explores new markets, builds partner propositions,
prepares customer conversations, monitors competitors, or evaluates where to invest next.

### [Support Ticket System](04-support-ticket-system/)

Run a complete IT support ticketing application with a browser interface, shared local
ticket store, and MCP server. Agents can list, create, update, and close tickets through
stdio or streamable HTTP while the web interface reflects the same data.

Choose this example to explore an end-to-end MCP application with a working user interface,
local persistence, and an Agent Framework client.

The examples are starting points, not fixed assignments. Change the target user,
instructions, tools, scoring rules, and test prompts to fit your company.

## How to work with GitHub Copilot in this lab

You are not expected to write every line from memory. You are expected to direct GitHub
Copilot, understand the proposed changes, and verify the result.

For examples 01-03:

1. Open the referenced quickstart and ask Copilot to explain it before changing anything.
2. Copy the quickstart into your selected scenario folder. Do not edit the original example.
3. In Copilot Chat, select **Agent** mode and describe one small change at a time.
4. Review the proposed file changes. Ask Copilot about any line you do not understand.
5. Run the script and read the complete output. Do not continue while it has an error.
6. Compare the result with the checkpoint in the scenario README.

Copilot can make plausible but incorrect changes. A successful run and the expected agent
behavior are both required; generated code alone is not completion.

## Terms used in this lab

- **Prompt agent:** A Foundry-managed agent defined by its model, instructions, and tools.
- **Instructions:** The persistent rules that define the agent's role and behavior.
- **MCP server:** A service that exposes external data and actions as tools for an agent.
- **Tool call:** A request from the agent to use one of those external capabilities.
- **Approval:** A pause that lets a person inspect and accept or deny a tool call.
- **Trace:** The execution details in Foundry showing prompts, tool calls, and results.
- **Agent playground:** The test experience inside the Microsoft Foundry portal.
- **Project connection:** A Foundry-managed connection that stores authentication for an
   external service without putting credentials in agent code or instructions.
- **Allow-list:** The small, explicit set of MCP tools that an agent is permitted to use.
- **Immutable version:** A saved agent version that does not change. Editing instructions or
   tools creates another version, so a tested version can always be identified.
- **Agent Application:** The published Azure resource that exposes a selected agent version
   through a stable endpoint and its own identity.
- **Code Interpreter:** An optional Foundry tool that runs Python for calculations and data
   analysis in a managed environment.
- **SLA:** A service-level agreement that defines a response or resolution commitment.
- **Prompt injection:** Instructions hidden inside external data that try to override the
   agent's real instructions.
- **Interruption buffer:** Time intentionally left unscheduled for unexpected work.
- **Authoritative source:** The system treated as the current source of truth. After an MCP
   connection is enabled, its live data replaces the local sample file for current status.

After a response in the agent playground, open its trace or run details and expand the tool
call. Inspect the server, tool name, arguments, result, and approval decision.

## Common journey

1. **Create in VS Code.** Copy and adapt the referenced Foundry quickstarts using
   GitHub Copilot Agent mode. Review every generated change.
2. **Test locally.** Adapt the Responses quickstart and test the instructions against
   the model in your Foundry project before creating a persistent agent.
3. **Deploy to Foundry.** Adapt the Create Agent quickstart to create an immutable
   prompt-agent version in the project.
4. **Tweak and add tools.** Open the version in the Microsoft Foundry portal, refine
   the instructions, add the suggested MCP connection, restrict the exposed tools,
   and test approvals in the agent playground. Saving changes creates a new version.
5. **Test in website.** Publish the selected version, choose **Test in website**,
   and repeat the supplied acceptance tests in the browser experience.

## Prerequisites

This final lab assumes you completed the earlier examples. Your Python environment,
dependencies, Azure sign-in, `.env` file, Foundry V2 project, and model deployment should
already be ready.

Before starting, confirm that the existing examples in
[02-microsoft-foundry-agents](../02-microsoft-foundry-agents/) still run. You also need:

- a unique `AGENT_NAME` for your new prompt agent
- `Foundry User` to create and test agents
- `Foundry Project Manager` on the Foundry resource to publish an agent
- a free workshop account for Notion, Todoist, or Tavily, depending on your choice

Use synthetic workshop data and keep API keys, OAuth tokens, customer records, and other
secrets out of source control.

## If you get stuck

1. Read the complete error, including the first line that names your own file.
2. Ask Copilot to explain the error before asking it to make changes.
3. Compare your copy with the original quickstart to find what changed.
4. Check that the virtual environment is active and the required `.env` values still exist.
5. Make one correction and rerun the same test. Avoid changing several things at once.

Never paste credentials, access tokens, or the contents of `.env` into Copilot Chat.

## What "local" and "deploy" mean

Prompt agents are managed by Foundry. Your local test runs code on your computer,
but model inference still occurs in Azure. Deployment creates an immutable
prompt-agent version; it does not upload or host your Python scripts. Those scripts
are development and test clients for the managed agent.

## Tool safety

- Use synthetic workshop data only.
- Prefer read-only MCP tools.
- Allow-list only the tools needed by the scenario.
- Require approval for every operation that creates, edits, sends, or deletes data.
- Inspect the server, tool name, and arguments before approving a call.
- Store provider credentials in a Foundry project connection, never in source.
- Confirm the provider's terms, data handling, endpoint, and free-tier limits.

## Publish and Test in website

After the agent works in the Microsoft Foundry agent playground:

1. Select the version you tested and choose **Publish**.
2. Create or update the managed Agent Application when prompted.
3. Wait until its deployment reports **Running**.
4. Assign intended testers the `Foundry User` role on the Agent Application.
5. Choose **Test in website** and run the example's tests.

Publishing gives the agent application its own identity. If a tool succeeds in
the project playground but fails after publishing, check the application
identity, project connection, and downstream permissions. **Test in website** is
a Foundry validation surface; it is not a separately owned production web app.

Third-party MCP services are operated outside Microsoft. Microsoft Foundry model
usage and published resources can incur Azure charges even when an MCP service
has a free plan.