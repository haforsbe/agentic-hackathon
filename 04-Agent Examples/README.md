# Agent Examples: Instructions First, Tools in Foundry

This lab contains three Microsoft Foundry prompt agents and one advanced MCP application.
Examples 01-03 follow the same beginner-friendly pattern:

1. review reusable agent instructions
2. test only those instructions locally
3. create a prompt-agent version in Foundry
4. connect a read-only MCP tool in Foundry
5. inspect tool calls and results in traces
6. publish the tested version and use **Test in website**

The local tests do not load sample data and do not connect to MCP. This is intentional:
they verify that the agent explains its method, respects its boundaries, and refuses to
invent live facts. Current data becomes available only after the MCP tool is attached to
a new agent version in Foundry.

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

- Python dependencies from the root `requirements.txt` are installed
- the workspace virtual environment is active
- `az login` completed for the tenant containing the Foundry project
- a compatible model is deployed in the project
- `.env` exists in the workspace root and is not committed
- you have `Foundry User` to create and test agents
- you have `Foundry Project Manager` to publish an Agent Application

The root `.env` needs these values:

```dotenv
AZURE_AI_PROJECT_ENDPOINT=your-project-endpoint
AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME=your-model-deployment
AGENT_NAME=a-unique-agent-name
```

Change `AGENT_NAME` when moving between examples. Never paste real `.env` values into a
README, prompt, or chat message.

No third-party account or API key is required for the three MCP tools. Microsoft Foundry
model usage and published Agent Applications can still incur Azure charges.

## Files in each prompt-agent example

| File | Purpose |
|------|---------|
| `agent-instructions.md` | Persistent role, workflow, output, grounding, and safety rules. |
| `local_test.py` | Sends the instructions and one test question directly to the deployed model. No MCP or data is attached. |
| `02-quickstart-create-agent.py` | Creates an immutable prompt-agent version from the tested instruction file. |
| `03-quickstart-chat-with-agent.py` | Invokes the named prompt agent after its MCP tool is connected in Foundry. |
| `README.md` | Exact setup, test, tool, trace, publishing, and troubleshooting steps. |

The Python files are already complete. Students should read them with GitHub Copilot,
change the instructions thoughtfully, run the tests, and inspect behavior rather than
retyping boilerplate.

## Common journey

### 1. Test the instructions locally

The local runner sends the contents of `agent-instructions.md` as model instructions and
one fixed acceptance prompt as user input. It sends no external data and gives the model
no tools.

Run a scenario's `no-tool` test first. A good response clearly says that live data was not
retrieved. If the model invents live facts, improve the instructions and rerun the same
test.

Local means the Python client runs on your computer. Model inference still occurs in your
Microsoft Foundry project.

### 2. Create the first Foundry version

Set a unique `AGENT_NAME`, run the scenario's `02-quickstart-create-agent.py`, and record
the printed version. This first version contains only the tested instructions.

Open **Microsoft Foundry > Build > Agents** and verify the displayed instructions. Run a
no-tool prompt in the playground before adding MCP. This gives you a clean behavioral
baseline.

### 3. Connect MCP in Foundry

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

### 4. Inspect approvals and traces

When a tool call pauses for approval, inspect the MCP server name, operation name,
arguments, and whether the operation is expected and read-only.

After the run completes, open its trace and confirm the tool result appears before the
response makes current factual claims. A fluent answer is not proof that a tool ran.

The included Python chat clients do not handle interactive approvals. After you have
inspected every allow-listed operation in the playground, create a runtime version with
approval set to **Never** for only those read operations. Never use this shortcut for a
write operation or a broader, unreviewed allow-list.

### 5. Publish and test

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

1. Read the complete error, including the first line naming your file.
2. Confirm the virtual environment is active.
3. Confirm `az login` and `az account show` use the intended tenant and subscription.
4. Confirm the required root `.env` values exist without sharing them.
5. Rerun one test, not every test.
6. If local behavior is wrong, edit the instructions rather than hard-coding an answer.
7. If MCP fails, verify the exact endpoint, **Unauthenticated** selection, allow-list, and attached agent version.
8. Open the trace before guessing where a tool workflow failed.

## Completion checklist

- The local `no-tool` test passes without sample data or MCP.
- The first Foundry version preserves the instruction-only baseline.
- The second version has the correct unauthenticated MCP and read-only allow-list.
- Playground traces prove that current claims use MCP results.
- Read-only and source-integrity boundaries still hold after tools are connected.
- The tested MCP-backed version is published and passes **Test in website**.