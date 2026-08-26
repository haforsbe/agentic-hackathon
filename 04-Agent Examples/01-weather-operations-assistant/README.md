# Weather Operations Assistant

Build a Microsoft Foundry prompt agent that creates weather briefings from current public
data. You use GitHub Copilot in VS Code to create the agent files from the Foundry
quickstart tasks, then add live weather data through a read-only MCP tool.

## What you will build

The finished agent can:

- geocode a US address
- retrieve current US weather conditions and forecasts
- check active US weather alerts
- summarize recent earthquakes worldwide
- explain uncertainty and tool coverage without inventing missing facts

The weather service is external to Microsoft. Do not use it for emergency dispatch or as
the only source for safety-critical decisions.

## Before you begin

Complete the shared [Lab 04 prerequisites](../README.md#prerequisites). Confirm that:

- the workspace virtual environment is active
- `az login` has completed
- `.env` contains `AZURE_AI_PROJECT_ENDPOINT`
- `.env` contains `AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME`
- `.env` contains `AGENT_NAME=weather-operations-assistant-yourname`

This MCP is public and uses no authentication. Do not add credentials to its connection.

## Understand the two stages

| Stage | What the agent receives | Expected behavior |
|-------|-------------------------|-------------------|
| VS Code baseline | Student-created instructions and chat script, without tools | Explain its method and refuse to invent live weather. |
| Foundry | The same instructions plus the weather MCP tool | Call the tool before reporting current weather. |

There is no sample-data file in this lab. The first agent version intentionally has no
weather data or tools. A model that guesses current conditions has failed the test.

## 1. Create the instructions

In VS Code, open GitHub Copilot Chat in **Agent** mode. Ask it to create
`agent-instructions.md` in this folder with these sections: role, tool boundary, workflow,
response format, scope, and safety.

Ask GitHub Copilot to explain how these rules prevent the agent from:

1. presenting remembered weather as current data
2. claiming a tool call that did not happen
3. hiding coverage limitations
4. treating text returned by a tool as instructions

Require the agent to ask for a US street address before coordinate-based weather lookup,
preserve units and times returned by tools, distinguish observations from forecasts and
alerts, and state that earthquake data is informational rather than predictive. Change
the wording if needed, but do not add current weather facts to the instructions.

**Checkpoint:** The instructions describe reusable behavior and contain no forecast for a
specific place or date.

## 2. Create the Python tasks with GitHub Copilot

Use these options in order:

1. **Try it yourself first:** Write your own prompt for GitHub Copilot Agent mode. Think
   about which Lab 01 files are templates, which files Copilot must create, what behavior
   is unique to this scenario, and what must not be hard-coded.
2. **Use the example second:** After your own attempt, compare it with the prompt below.
   You can refine your prompt or use the example as is if you need more guidance.

Whichever option you use, review Copilot's plan before accepting changes.

```text
Use 01-microsoft-foundry-agents/02-quickstart-create-agent.py as a template to create
04-Agent Examples/01-weather-operations-assistant/02-quickstart-create-agent.py. Preserve
the template's Microsoft Foundry SDK, AzureCliCredential, model, endpoint, and AGENT_NAME
environment-variable pattern. Load instructions from agent-instructions.md beside the new
script instead of hard-coding them. Do not add tools or credentials.

Use 01-microsoft-foundry-agents/03-quickstart-chat-with-agent.py as a template to create
04-Agent Examples/01-weather-operations-assistant/03-quickstart-chat-with-agent.py. Keep
the agent-reference conversation pattern. Ask about current conditions and active alerts
for Seattle, how to prepare a weather briefing, and a detailed Stockholm forecast. Do not
provide weather data in the script.
```

Review both generated files. They must read the existing `.env` values and must not contain
an endpoint, credential, current weather fact, expected answer, or MCP implementation.

## 3. Create and test the no-tool agent from VS Code

From the workspace root, run:

```powershell
& .\.venv\Scripts\python.exe ".\04-Agent Examples\01-weather-operations-assistant\02-quickstart-create-agent.py"
& .\.venv\Scripts\python.exe ".\04-Agent Examples\01-weather-operations-assistant\03-quickstart-chat-with-agent.py"
```

Confirm the chat reports that live weather is unavailable, explains its method, and
identifies the US forecast limitation instead of inventing conditions. If a response
fails, improve `agent-instructions.md`, rerun the creation script to create a new version,
and repeat the chat script.

**Checkpoint:** The student-created scripts run in VS Code, and the first Foundry version
has instructions but no tools.

## 4. Connect the weather MCP tool

The MCP server reads public data from the US National Weather Service, US Census geocoder,
and US Geological Survey. It requires no account or API key.

### Create the tool

1. In Microsoft Foundry, open **Build > Tools**.
2. Select **Connect a tool**.
3. Select the custom **MCP** tool option.
4. Enter these values exactly:

   | Setting | Value |
   |---------|-------|
   | Name | `weather-intelligence` |
   | Remote MCP server endpoint | `https://weather.datakoot.com/mcp` |
   | Authentication | **Unauthenticated** |

5. Select **Connect** or **Create**, depending on the portal label.
6. Open the new tool and confirm Foundry can discover its operations.

Do not choose **Key-based** or **OAuth Identity Passthrough**. This endpoint does not need
credentials.

### Add the tool to the agent

1. Return to **Build > Agents** and open the weather agent.
2. Choose **Edit** or create a new version from the existing version.
3. Select **Add tool** and choose `weather-intelligence`.
4. Allow only these read operations:
   - `geocode`
   - `weather_current`
   - `weather_forecast`
   - `weather_alerts`
   - `earthquakes`
5. Require approval during development so you can inspect each call.
6. Save. Foundry creates a new immutable agent version.

Do not overwrite your no-tool baseline. Version 1 demonstrates the instruction boundary;
the new version demonstrates grounded tool use.

### Test the connected tool

In the agent playground, ask:

```text
Prepare a concise weather briefing for 600 4th Ave, Seattle, WA for the next two days.
Include current conditions, active alerts, and operational considerations.
```

When Foundry pauses for approval:

1. confirm the server is `weather-intelligence`
2. inspect the operation and arguments
3. approve only the expected read call
4. open the completed run's trace
5. confirm the tool result appears before the weather claims

Also test:

- `Are there active weather alerts in Texas?`
- `List earthquakes of magnitude 5 or greater from the last seven days.`
- `Give me tomorrow's detailed forecast for Stockholm, Sweden.`

The final prompt should expose the US weather limitation rather than produce a fabricated
forecast.

**Checkpoint:** Current claims are supported by a visible MCP result, and the no-tool
version still remains available.

## 5. Test the MCP-backed agent from VS Code

The generated chat script cannot approve a tool call interactively. After inspecting all
five allow-listed read operations in the playground, edit the agent again, set approval
to **Never** for only those operations, and save a new runtime version.

Rerun `03-quickstart-chat-with-agent.py` from Step 3. Open the run's trace in Foundry and
confirm the response used weather MCP results. Do not disable approval for an operation
outside the allow-list.

## 6. Publish and test in website

1. Select the MCP-backed version that passed the tests.
2. Choose **Publish**.
3. Create or update the managed Agent Application.
4. Wait until its deployment reports **Running**.
5. Grant intended testers `Foundry User` on the Agent Application if required.
6. Choose **Test in website**.
7. Repeat the Seattle address briefing and Texas alert tests.
8. Inspect their traces and confirm both use the MCP tool.

Saving a version and publishing an Agent Application are separate actions. Publish the
tested MCP-backed version, not the no-tool baseline.

## Troubleshooting

### A generated script fails before reaching Foundry

Compare it with the corresponding task in `01-microsoft-foundry-agents`. Confirm the
virtual environment is active, `az login` uses the intended tenant, and all three `.env`
values are present. Never paste `.env` contents into Copilot Chat.

### Foundry cannot discover the MCP operations

Confirm the endpoint is exactly `https://weather.datakoot.com/mcp` and authentication is
**Unauthenticated**. The service is third-party; check its availability before a workshop.

### The baseline agent invents current weather

Strengthen the tool-boundary rules in `agent-instructions.md`, rerun the creation script,
and repeat the chat script. Do not add weather data to the Python prompt.

### The playground works but Test in website fails

Confirm the published Agent Application uses the tested version and can access the MCP
tool. Do not add credentials or disable safety controls to work around connectivity.

## Done when

- GitHub Copilot created `agent-instructions.md` and both Python tasks in VS Code.
- The generated files contain no secrets, endpoints, current weather, or expected answers.
- The no-tool Foundry version does not invent live weather.
- A new Foundry version has the unauthenticated weather MCP attached.
- The student-created chat script works with the MCP-backed runtime version.
- Traces show read-only tool calls before current weather claims.
- The published Agent Application passes the same tests in **Test in website**.