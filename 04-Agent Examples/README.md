# Agent Examples: Build with GitHub Copilot in VS Code

This lab contains three Microsoft Foundry prompt agents and one advanced MCP application.
Examples 01-03 follow the same beginner-friendly pattern:

1. use GitHub Copilot in VS Code to create reusable agent instructions
2. use the Python tasks in `01-microsoft-foundry-agents` as templates
3. create and chat with the prompt agent by running student-created Python scripts
4. connect a read-only MCP tool in a new agent version
5. inspect tool calls and results in traces
6. publish the tested MCP-backed version and use **Test in website**

The first Foundry version has instructions but no tools. This baseline verifies that the
agent respects its boundaries and refuses to invent live facts. Current data becomes
available only after the MCP tool is attached to a new agent version.

Examples 01-03 use Microsoft Foundry prompt agents, not Microsoft Agent Framework hosted
agents. Example 04 runs an Agent Framework agent and its MCP server locally.

## Two different learning paths

| Examples | Learning path |
|----------|---------------|
| 01-03 | Student-built Foundry prompt agents. Create the files with GitHub Copilot, create the agent from VS Code, connect a remote MCP tool in Foundry, and publish the tested agent. |
| 04 | Advanced implemented reference application. Run and extend a local web app, local MCP server, and local Agent Framework agent. |

Example 04 does **not** use the Lab 01 prompt-agent templates, create a Foundry prompt
agent, attach its MCP server in Foundry, or publish an Agent Application. The Agent
Framework process and MCP server run locally and connect directly over HTTP. Model
inference still uses the deployment and project endpoint configured in `.env`.

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

### [Support Ticket System (Advanced)](04-support-ticket-system%20ADVANCED/)

Run a complete IT support ticket application with a browser interface, shared local ticket
store, and MCP server. Agents can list, create, update, and close tickets while the web
interface reflects the same data.

Choose this example to explore an end-to-end MCP application with local persistence, a
working UI, and a local Agent Framework agent.

## Prerequisites

These shared prerequisites apply to Examples 01-03. Complete the earlier Foundry
quickstarts first, then confirm:

- Python dependencies from the root `requirements.txt` are installed
- the workspace virtual environment is active
- `az login` completed for the tenant containing the Foundry project
- `.env` contains `AZURE_AI_PROJECT_ENDPOINT`
- `.env` contains `AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME`
- `.env` contains a unique `AGENT_NAME` for the scenario
- you have `Foundry User` to create and test agents
- you have `Foundry Project Manager` to publish an Agent Application

No third-party account or API key is required for the three MCP tools. Microsoft Foundry
model usage and published Agent Applications can still incur Azure charges.

## Starter file in Examples 01-03

| File | Purpose |
|------|---------|
| `README.md` | Requirements and exact setup, test, tool, trace, and publishing steps. |

Each folder intentionally starts with only `README.md`. Students create the instruction
and Python files with GitHub Copilot in VS Code. Do not copy completed files from another
student or add starter implementations to these folders.

For every student-created task, first reason through the requirements and try your own
Copilot prompt. Only after that attempt, compare your approach with the supplied example
or use the example as is. The examples are a second option, not the starting point.

## Common journey for Examples 01-03

The steps in this section apply only to the three student-built Foundry prompt-agent
examples. They do not apply to the advanced support ticket system in Example 04.

### 1. Create the scenario files with GitHub Copilot

Open the scenario folder in VS Code and use GitHub Copilot Agent mode to create:

| Student-created file | Template or source |
|----------------------|--------------------|
| `agent-instructions.md` | The requirements in the scenario README |
| `02-quickstart-create-agent.py` | `01-microsoft-foundry-agents/02-quickstart-create-agent.py` |
| `03-quickstart-chat-with-agent.py` | `01-microsoft-foundry-agents/03-quickstart-chat-with-agent.py` |

Ask Copilot to preserve `AzureCliCredential`, the existing environment-variable names,
and the Microsoft Foundry SDK pattern from the templates. The creation script must load
the local instruction file instead of hard-coding instructions. The chat script must use
the scenario's acceptance prompts and send no fabricated tool data.

Review every generated change before running it. The files must not contain endpoint
values, credentials, current facts, or expected answers.

### 2. Create and test the first Foundry version from VS Code

In VS Code, select **Terminal > New Terminal**. Use the integrated PowerShell terminal that
opens at the repository root, the folder containing this README and `requirements.txt`.
Run `Get-Location` to check. If needed, run
`Set-Location "C:\path\to\agentic-hackathon"`, replacing the example path with the folder
where you cloned this repository.

Paste each command from the scenario README into that terminal and press **Enter**. Run
the creation command first; it creates the first prompt-agent version with instructions
and no tools. Then run the chat command to test the scenario boundary. A good response
clearly says that current data was not retrieved. If the model invents current facts,
improve `agent-instructions.md`, run the creation script again, and repeat the chat test.

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

### 5. Test from VS Code and publish

The Python chat template does not handle interactive tool approval. After inspecting the
allow-listed read operations in the playground, save a runtime version with approval set
to **Never** for only those operations. Rerun the student-created chat script and confirm
the trace contains the expected MCP results.

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

## Advanced journey for Example 04

Example 04 starts with an implemented application instead of an empty challenge folder.
Follow its own [Support Ticket System instructions](04-support-ticket-system%20ADVANCED/):

1. Review the browser, API, ticket store, MCP server, and local Agent Framework agent.
2. Run the local web application and verify ticket changes in the browser.
3. Connect the local MCP server directly to GitHub Copilot in VS Code.
4. Run the local Agent Framework agent and connect it to the local MCP server over HTTP.
5. Ask GitHub Copilot to implement and verify one extension across the affected interfaces.

There is no Foundry prompt-agent creation, MCP attachment in the Foundry portal, trace
approval exercise, or Agent Application publishing step in this advanced path. Only the
model request leaves the local machine for the configured Foundry model endpoint.

## Terms used in Examples 01-03

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

1. Read the complete terminal or portal error.
2. Compare generated code with its template in `01-microsoft-foundry-agents`.
3. Confirm the virtual environment, `az login`, and the three required `.env` values.
4. Repeat one chat question, not every acceptance prompt.
5. If baseline behavior is wrong, edit the instructions and create a new version.
6. If MCP fails, verify the exact endpoint, **Unauthenticated** selection, allow-list, and attached agent version.
7. Open the trace before guessing where a tool workflow failed.

## Completion checklist for Examples 01-03

- The first Foundry version passes its baseline prompts without tools.
- GitHub Copilot created the instruction, creation, and chat files from the stated tasks.
- The no-tool version remains available as a behavioral baseline.
- The second version has the correct unauthenticated MCP and read-only allow-list.
- The student-created chat script works against the MCP-backed runtime version.
- Playground traces prove that current claims use MCP results.
- Read-only and source-integrity boundaries still hold after tools are connected.
- The tested MCP-backed version is published and passes **Test in website**.