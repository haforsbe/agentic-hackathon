# Agent Examples: Instructions First, Tools in Foundry

This lab contains three Microsoft Foundry prompt agents and one advanced MCP application.
Examples 01-03 follow the same beginner-friendly pattern:

1. create reusable agent instructions from the scenario requirements
2. create a prompt agent in Foundry without tools
3. test the instruction boundary in the Foundry playground
4. connect a read-only MCP tool in a new agent version
5. inspect tool calls and results in traces
6. publish the tested MCP-backed version and use **Test in website**

The first Foundry version has instructions but no tools. This baseline verifies that the
agent respects its boundaries and refuses to invent live facts. Current data becomes
available only after the MCP tool is attached to a new agent version.

Examples 01-03 use Microsoft Foundry prompt agents, not Microsoft Agent Framework hosted
agents. Example 04 runs locally with Agent Framework and its own MCP server.

## Choose an example

### [Weather Operations Assistant](01-weather-operations-assistant/)

Create current US weather briefings, check active alerts, and summarize recent worldwide
earthquakes. The Foundry version uses an unauthenticated read-only weather MCP backed by
public NWS, Census, and USGS data.

Choose this example to practice tool boundaries, geocoding before weather lookup, safety
language, and distinguishing observations, forecasts, and alerts.

### [Cultural Travel Planner](02-cultural-travel-planner/)

Plan museum visits, art events, and cultural layovers using a public read-only cultural
travel catalog. The agent separates returned facts from planning assumptions and never
claims to book tickets.

Choose this example to practice clarifying questions, multi-step planning, time constraints,
source links, and firm read-only boundaries.

### [Microsoft Cloud Guidance Advisor](03-microsoft-cloud-guidance-advisor/)

Answer Microsoft product and implementation questions using official Microsoft Learn
documentation and code samples. Microsoft operates this unauthenticated MCP endpoint and
documents it for Microsoft Foundry.

Choose this example to practice search-and-fetch workflows, source-grounded comparisons,
official code samples, citations, and identifying missing technical context.

### [Support Ticket System Advanced](04-support-ticket-system%20ADVANCED/)

Run a complete IT support ticket application with a browser interface, shared local ticket
store, and MCP server. Agents can list, create, update, and close tickets while the web
interface reflects the same data.

Choose this example to explore an end-to-end MCP application with local persistence, a
working UI, and an Agent Framework client.

## Prerequisites

Complete the earlier Foundry quickstarts first. Before starting examples 01-03, confirm:

- you can open the intended Microsoft Foundry project
- a compatible model is deployed in the project
- you have `Foundry User` to create and test agents
- you have `Foundry Project Manager` to publish an Agent Application

No third-party account or API key is required for the three MCP tools. Microsoft Foundry
model usage and published Agent Applications can still incur Azure charges.

## Starter file in each prompt-agent example

| File | Purpose |
|------|---------|
| `README.md` | Requirements and exact setup, test, tool, trace, and publishing steps. |

Each folder intentionally starts with only `README.md`. Students create the instruction
file from the README and configure and test the agent in the Foundry portal.

## Common journey

### 1. Create and test the first Foundry version

Open **Microsoft Foundry > Build > Agents**, create a prompt agent, choose the deployed
model, and paste in the contents of your `agent-instructions.md`. Save the first
version without tools. Run the scenario's baseline prompts in the playground. A good
response clearly says that live data was not retrieved. If the model invents live facts,
improve the instructions, save a new version, and rerun the same prompt.

### 2. Connect MCP in Foundry

Each scenario README supplies the exact endpoint and allow-list. The common portal flow is:

1. Open **Build > Tools**.
2. Select **Connect a tool**.
3. Select the custom **MCP** option.
4. Enter the scenario's tool name and remote endpoint.
5. Select **Unauthenticated**.
6. Create the tool and confirm its operations are discovered.
7. Return to the agent and create a new version.
8. Add the MCP tool and allow only the listed read operations.
9. Require approval during development.
10. Save the new immutable version.

Do not choose **Key-based** or **OAuth Identity Passthrough** for these endpoints. Do not
put keys, tokens, headers, or query parameters in the endpoint URL.

### 3. Inspect approvals and traces

When a tool call pauses for approval, inspect the MCP server name, operation name,
arguments, and whether the operation is expected and read-only.

After the run completes, open its trace and confirm the tool result appears before the
response makes current factual claims. A fluent answer is not proof that a tool ran.

### 4. Publish and test

Saving an agent version and publishing an Agent Application are different actions:

1. Select the MCP-backed version that passed the playground tests.
2. Choose **Publish**.
3. Create or update the managed Agent Application.
4. Wait for **Running**.
5. Grant intended testers `Foundry User` if required.
6. Choose **Test in website**.
7. Repeat the scenario's acceptance prompts and inspect their traces.

If a tool works in the playground but not in **Test in website**, confirm that the
application uses the correct version and can reach the MCP endpoint. Do not add credentials
to an unauthenticated tool or remove safety rules as a workaround.

## Terms used in this lab

- **Prompt agent:** A Foundry-managed agent defined by a model, instructions, and tools.
- **Instructions:** Persistent rules that define the agent's role and behavior.
- **MCP server:** A service that exposes data or actions as tools for an agent.
- **Tool call:** A structured request from the agent to an MCP operation.
- **Allow-list:** The explicit set of MCP operations an agent may call.
- **Approval:** A pause that lets a person inspect and accept or deny a tool call.
- **Trace:** Run details showing prompts, tool calls, arguments, results, and timing.
- **Immutable version:** A saved agent version that does not change. Editing creates a new version.
- **Agent Application:** A published Azure resource exposing a selected agent version.
- **Grounding:** Supporting an answer with data retrieved from an authoritative source.
- **Prompt injection:** Instructions hidden inside user or tool data that try to override the agent's real rules.

## Tool safety

- Use only the documented public endpoints.
- Allow-list only the read operations required by the scenario.
- Keep approval enabled while developing and teaching.
- Inspect tool arguments before approval and results after execution.
- Treat tool output as untrusted data, not as agent instructions.
- Never put secrets in source files, instructions, prompts, URLs, or traces.
- Recheck third-party endpoint availability before a workshop.

The weather and cultural travel MCPs are third-party services. Microsoft Learn MCP is
Microsoft-operated. Registry presence or a successful test does not guarantee future
third-party availability.

## If you get stuck

1. Read the complete portal error.
2. Confirm you opened the intended Foundry project and selected a deployed model.
3. Repeat one playground question, not every acceptance prompt.
4. If baseline behavior is wrong, edit the instructions and save a new version.
5. If MCP fails, verify the exact endpoint, **Unauthenticated** selection, allow-list, and attached agent version.
6. Open the trace before guessing where a tool workflow failed.

## Completion checklist

- The first Foundry version passes its baseline prompts without tools.
- The no-tool version remains available as a behavioral baseline.
- The second version has the correct unauthenticated MCP and read-only allow-list.
- Playground traces prove that current claims use MCP results.
- Read-only and source-integrity boundaries still hold after tools are connected.
- The tested MCP-backed version is published and passes **Test in website**.