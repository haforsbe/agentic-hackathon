# Cultural Travel Planner

Build a Microsoft Foundry prompt agent that plans museum visits, art events, and cultural
layovers. Use GitHub Copilot in VS Code to create the agent files from the Foundry
quickstart tasks, then connect a public read-only MCP tool for current travel information.

## What you will build

The finished agent can:

- find current art events by country, date, or event type
- retrieve museum visitor guides and practical details
- find prepared cultural layover itineraries
- build a time-aware itinerary while separating facts from assumptions

It cannot search general flights or hotels, buy tickets, or make reservations.

## Before you begin

Complete the shared [Lab 04 prerequisites](../README.md#prerequisites). Confirm that the
virtual environment is active, `az login` has completed, and `.env` contains the project
endpoint, model deployment, and `AGENT_NAME=cultural-travel-planner-yourname`. The travel
MCP needs no account, key, or OAuth connection.

## Understand the two stages

| Stage | What the agent receives | Expected behavior |
|-------|-------------------------|-------------------|
| VS Code baseline | Student-created instructions and chat script, without tools | Explain its planning method and refuse invented current details or bookings. |
| Foundry | The same instructions plus travel MCP | Search the catalog before using current venue or event facts. |

There is no sample-data file. Data enters the agent only through the MCP tool after it is
connected in Foundry.

## 1. Create the instructions

In VS Code, open GitHub Copilot Chat in **Agent** mode. Ask it to create
`agent-instructions.md` in this folder with a role, tool boundary, planning workflow,
response format, and booking limitation.

Confirm the instructions require the agent to:

1. ask for a destination, date, and available time
2. keep tool facts separate from assumptions
3. include practical source links when returned
4. avoid overlapping activities
5. never claim a booking or purchase

Do not add venue hours, prices, or events to the instruction file.

**Checkpoint:** The instructions work for any supported destination and contain no static
travel data.

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
04-Agent Examples/02-cultural-travel-planner/02-quickstart-create-agent.py. Preserve the
template's Microsoft Foundry SDK, AzureCliCredential, model, endpoint, and AGENT_NAME
environment-variable pattern. Load instructions from agent-instructions.md beside the new
script instead of hard-coding them. Do not add tools or credentials.

Use 01-microsoft-foundry-agents/03-quickstart-chat-with-agent.py as a template to create
04-Agent Examples/02-cultural-travel-planner/03-quickstart-chat-with-agent.py. Keep the
agent-reference conversation pattern. Ask for a current art-focused Paris plan, the method
for a realistic six-hour itinerary, and a confirmed Louvre ticket booking. Do not provide
venue or event data in the script.
```

Review both generated files. They must read the existing `.env` values and contain no
endpoint, credential, current venue facts, expected answers, or MCP implementation.

## 3. Create and test the no-tool agent from VS Code

In VS Code, select **Terminal > New Terminal**. A PowerShell terminal should open at the
repository root, `agentic-hackathon`. Run `Get-Location` and confirm the displayed path
ends with `\agentic-hackathon`. If it does not, run the command below after replacing the
example path with the folder where you cloned this repository:

```powershell
Set-Location "C:\path\to\agentic-hackathon"
```

Paste the following commands into that terminal one at a time and press **Enter** after
each command:

```powershell
& .\.venv\Scripts\python.exe ".\04-Agent Examples\02-cultural-travel-planner\02-quickstart-create-agent.py"
& .\.venv\Scripts\python.exe ".\04-Agent Examples\02-cultural-travel-planner\03-quickstart-chat-with-agent.py"
```

Confirm the agent does not invent current details, explains a sound planning method, and
refuses to claim a booking. If a response fails, improve `agent-instructions.md`, rerun
the creation script to create a new version, and repeat the chat script.

**Checkpoint:** The student-created scripts run in VS Code, and the first immutable
Foundry version has instructions but no tools.

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

## 5. Test the MCP-backed agent from VS Code

The generated chat script cannot approve a tool call interactively. After inspecting the
three allow-listed read operations in the playground, edit the agent again, set approval
to **Never** for only those operations, and save a new runtime version.

Rerun `03-quickstart-chat-with-agent.py` from Step 3. Inspect the trace and confirm current
travel details come from MCP results while the booking request remains refused.

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

### A generated script fails before reaching Foundry

Compare it with the corresponding task in `01-microsoft-foundry-agents`. Confirm the
virtual environment is active, `az login` uses the intended tenant, and all three `.env`
values are present. Never paste `.env` contents into Copilot Chat.

### The baseline agent invents current museum information

Strengthen the tool-boundary section in `agent-instructions.md`, rerun the creation script,
and repeat the chat script. Do not add a sample-data file.

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

- GitHub Copilot created `agent-instructions.md` and both Python tasks in VS Code.
- The generated files contain no secrets, endpoints, travel facts, or expected answers.
- The no-tool and booking chat checks pass.
- A new Foundry version uses only the three allow-listed read operations.
- The student-created chat script works with the MCP-backed runtime version.
- Traces show MCP results before current travel claims.
- The published Agent Application passes the same tests.