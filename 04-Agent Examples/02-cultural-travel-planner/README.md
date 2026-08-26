# Cultural Travel Planner

Build a Microsoft Foundry prompt agent that plans museum visits, art events, and cultural
layovers. First test its instructions without data. Then connect a public read-only MCP
tool in Foundry for current cultural travel information.

## What you will build

The finished agent can:

- find current art events by country, date, or event type
- retrieve museum visitor guides and practical details
- find prepared cultural layover itineraries
- build a time-aware itinerary while separating facts from assumptions

It cannot search general flights or hotels, buy tickets, or make reservations.

## Before you begin

Complete the shared [Lab 04 prerequisites](../README.md#prerequisites). Confirm that the
virtual environment is active, `az login` has completed, and `.env` contains:

```dotenv
AZURE_AI_PROJECT_ENDPOINT=your-project-endpoint
AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME=your-model-deployment
AGENT_NAME=cultural-travel-planner-yourname
```

Keep your real values private. The travel MCP needs no account, key, or OAuth connection.

## Understand the two stages

| Stage | What the agent receives | Expected behavior |
|-------|-------------------------|-------------------|
| Local test | Instructions and one question | Explain its planning method and refuse invented current details or bookings. |
| Foundry | The same instructions plus travel MCP | Search the catalog before using current venue or event facts. |

There is no sample-data file. Data enters the agent only through the MCP tool after it is
connected in Foundry.

## 1. Review the instructions

Open [agent-instructions.md](agent-instructions.md). Ask GitHub Copilot to explain the
tool boundary, planning workflow, response format, and booking limitation.

Confirm the instructions require the agent to:

1. ask for a destination, date, and available time
2. keep tool facts separate from assumptions
3. include practical source links when returned
4. avoid overlapping activities
5. never claim a booking or purchase

Do not add venue hours, prices, or events to the instruction file.

**Checkpoint:** The instructions work for any supported destination and contain no static
travel data.

## 2. Test only the instructions locally

[local_test.py](local_test.py) loads only the instruction file and a selected prompt. Run:

```powershell
& .\.venv\Scripts\python.exe ".\04-Agent Examples\02-cultural-travel-planner\local_test.py" --test no-tool
```

The response should not invent current Paris exhibitions, opening hours, or prices. It
should state that live cultural travel data is unavailable without the tool.

Run two more tests:

```powershell
& .\.venv\Scripts\python.exe ".\04-Agent Examples\02-cultural-travel-planner\local_test.py" --test method
& .\.venv\Scripts\python.exe ".\04-Agent Examples\02-cultural-travel-planner\local_test.py" --test booking
```

The booking test must explain that the agent cannot buy or reserve tickets. Use `--test
all` to run every prompt.

If a response fails, improve `agent-instructions.md` and rerun the same test. Do not add
sample travel facts or hard-coded answers to Python.

**Checkpoint:** The local agent explains a sound planning process, identifies missing
live data, and refuses to claim a reservation.

## 3. Create the prompt agent in Foundry

1. Set a unique `AGENT_NAME` in the root `.env`.
2. Run:

   ```powershell
   & .\.venv\Scripts\python.exe ".\04-Agent Examples\02-cultural-travel-planner\02-quickstart-create-agent.py"
   ```

3. Record the printed agent name and version.
4. Open **Microsoft Foundry > Build > Agents**.
5. Select the agent and confirm its instructions match
   [agent-instructions.md](agent-instructions.md).
6. Ask for current museum hours once. Confirm it still reports that no live tool is
   available.

**Checkpoint:** The first immutable version exists with instructions and no tools.

## 4. Connect the cultural travel MCP

The travel.art MCP exposes a public cultural travel catalog over Streamable HTTP. It is a
third-party service, so verify availability before using this lab in a workshop.

### Create the tool

1. In Microsoft Foundry, open **Build > Tools**.
2. Select **Connect a tool**.
3. Select the custom **MCP** tool option.
4. Enter:

   | Setting | Value |
   |---------|-------|
   | Name | `cultural-travel` |
   | Remote MCP server endpoint | `https://mcp.travel.art/` |
   | Authentication | **Unauthenticated** |

5. Select **Connect** or **Create**.
6. Open the tool and confirm Foundry discovers its operations.

Do not choose **Key-based** or **OAuth Identity Passthrough**. Do not place anything after
the endpoint URL.

### Add the tool to a new agent version

1. Return to **Build > Agents** and open your cultural travel agent.
2. Choose **Edit** or create a new version from the existing version.
3. Select **Add tool** and choose `cultural-travel`.
4. Allow only these read operations:
   - `find_art_events`
   - `find_museum_guide`
   - `find_layover_itinerary`
5. Require approval during development.
6. Save the configuration as a new immutable version.

Keep the original no-tool version. It is your baseline for comparing behavior.

### Test the connected tool

In the agent playground, ask:

```text
Plan an art-focused visit to Paris on Saturday, October 10, 2026, using current museum
information. I have six hours, prefer a relaxed pace, and want practical details and
source links.
```

When approval appears, verify the MCP server, operation, and arguments before approving.
After the answer completes, open the trace and confirm the catalog result appears before
the itinerary uses current details.

Also test:

- `Find art events in Italy in October 2026.`
- `Create a cultural plan for a six-hour Rome layover.`
- `Book two museum tickets and confirm the purchase.`

The final request must still be refused because the tool is read-only.

**Checkpoint:** The response uses visible MCP results, labels assumptions, fits the stated
time, and never claims a booking.

## 5. Test with the Python chat client

The Python script cannot display Foundry's interactive approval prompt. After you have
inspected all three read operations in the playground, edit the agent, keep only those
allow-listed operations, change their approval setting to **Never**, and save a new runtime
version. The MCP exposes no booking operation to this agent.

[03-quickstart-chat-with-agent.py](03-quickstart-chat-with-agent.py) sends only a travel
question. It does not supply venue data.

Confirm `AGENT_NAME` names the MCP-backed agent, then run:

```powershell
& .\.venv\Scripts\python.exe ".\04-Agent Examples\02-cultural-travel-planner\03-quickstart-chat-with-agent.py"
```

Open the run trace in Foundry. Confirm it contains a travel MCP call and returned sources.
If it does not, verify that the tool is attached to the latest agent version.

## 6. Publish and test in website

1. Select the tested MCP-backed version and choose **Publish**.
2. Create or update the managed Agent Application.
3. Wait until the deployment reports **Running**.
4. Grant intended testers `Foundry User` if required.
5. Choose **Test in website**.
6. Repeat the Paris itinerary and booking-refusal tests.
7. Confirm current details still have traceable MCP results and links.

Publishing and saving a version are separate actions. Publish only the version that passed
the playground tests.

## Troubleshooting

### The local test invents current museum information

Strengthen the tool-boundary section in `agent-instructions.md` and rerun `--test no-tool`.
Do not add a sample-data file.

### Foundry cannot discover tools

Confirm the endpoint is exactly `https://mcp.travel.art/`, including the final slash, and
authentication is **Unauthenticated**. Because this is a third-party service, an outage
must be resolved by the provider or handled by choosing another lab.

### The agent says it booked tickets

Confirm the read-only boundary remains in the saved agent version. Rerun the booking test
in both the playground and website.

### Playground works but Test in website fails

Confirm the Agent Application uses the tested version and can reach the MCP endpoint. Do
not add credentials or weaken the agent boundaries.

## Done when

- Local tests contain no travel data.
- The no-tool and booking tests pass.
- A new Foundry version uses only the three allow-listed read operations.
- Traces show MCP results before current travel claims.
- The published Agent Application passes the same tests.