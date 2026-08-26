# Weather Operations Assistant

Build a Microsoft Foundry prompt agent that creates weather briefings from current public
data. You first test only its instructions. You add live weather data later by connecting
a read-only MCP tool in Microsoft Foundry.

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

Do not put weather data, MCP credentials, or MCP URLs in `.env`. This MCP is public and
uses no authentication.

## Understand the two stages

| Stage | What the agent receives | Expected behavior |
|-------|-------------------------|-------------------|
| Local test | Instructions and a test question only | Explain its method and refuse to invent live weather. |
| Foundry | The same instructions plus the weather MCP tool | Call the tool before reporting current weather. |

There is no sample-data file in this lab. The local test intentionally has no weather
data. A model that guesses current conditions has failed the test.

## 1. Create the instructions

Create `agent-instructions.md` in this folder. Ask GitHub Copilot to draft it with these
sections: role, tool boundary, workflow, response format, scope, and safety.

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

## 2. Test only the instructions locally

[local_test.py](local_test.py) loads `agent-instructions.md` and sends one question to the
model. It does not load sample data and does not connect to MCP.

From the workspace root, run:

```powershell
& .\.venv\Scripts\python.exe ".\04-Agent Examples\01-weather-operations-assistant\local_test.py" --test no-tool
```

The response should say that live weather is unavailable in the session. It should not
invent Seattle conditions or claim to have checked alerts.

Run the remaining tests:

```powershell
& .\.venv\Scripts\python.exe ".\04-Agent Examples\01-weather-operations-assistant\local_test.py" --test method
& .\.venv\Scripts\python.exe ".\04-Agent Examples\01-weather-operations-assistant\local_test.py" --test scope
```

Use `--test all` to run all three. Improve the instructions if a response guesses live
facts, hides limitations, or claims tool access. Do not hard-code an expected answer in
Python.

**Checkpoint:** The agent explains how it would work, refuses unsupported live claims,
and identifies that detailed weather coverage is primarily US-focused.

## 3. Create the prompt agent in Foundry

1. Open **Microsoft Foundry > Build > Agents**.
2. Select **Create agent** and choose your deployed model.
3. Name the agent `weather-operations-assistant-yourname`.
4. Paste the complete contents of your `agent-instructions.md` into **Instructions**.
5. Save the first version without adding a tool.
6. Ask for current Seattle weather in the playground. Confirm the agent reports that live
   weather is unavailable instead of inventing conditions.

At this point, asking for current weather should still produce the no-tool limitation.

**Checkpoint:** Version 1 exists in Foundry and has instructions but no tools.

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

## 5. Publish and test in website

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

### The local test reports missing environment variables

Confirm `.env` is in the workspace root and contains the three values listed under
**Before you begin**. Never paste the contents of `.env` into chat.

### The local test cannot authenticate

Run `az login`, select the correct tenant and subscription, and rerun the same test.

### Foundry cannot discover the MCP operations

Confirm the endpoint is exactly `https://weather.datakoot.com/mcp` and authentication is
**Unauthenticated**. The service is third-party; check its availability before a workshop.

### The agent invents current weather locally

Strengthen the tool-boundary rules in `agent-instructions.md`, then rerun `--test no-tool`.
Do not fix this by adding weather data to the prompt.

### The playground works but Test in website fails

Confirm the published Agent Application uses the tested version and can access the MCP
tool. Do not add credentials or disable safety controls to work around connectivity.

## Done when

- Local tests use instructions and questions only.
- The student-created `agent-instructions.md` remains in the local working copy only.
- The no-tool test does not invent live weather.
- A new Foundry version has the unauthenticated weather MCP attached.
- Traces show read-only tool calls before current weather claims.
- The published Agent Application passes the same tests in **Test in website**.