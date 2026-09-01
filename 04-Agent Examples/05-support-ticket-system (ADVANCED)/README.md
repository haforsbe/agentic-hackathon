# Support Ticket System

Explore a complete IT support application that combines a browser interface, shared local
storage, a local MCP server, and a local Agent Framework agent. Unlike Examples 01-04,
this is an implemented reference system rather than a Foundry prompt-agent challenge.

## Before you begin

- Complete the repository setup in [Prereqs_Participant.md](../../Prereqs_Participant.md).
- From the repository root, move into this example folder:

  ```powershell
  Set-Location ".\04-Agent Examples\05-support-ticket-system (ADVANCED)"
  ```

- Install the dependencies from this folder with `pip install -r requirements.txt`.
- Sign in with `az login`; the local Agent Framework agent uses `AzureCliCredential` exclusively.
- Configure `AZURE_AI_PROJECT_ENDPOINT` and
  `AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME` in the repository root `.env` file.
- Use synthetic ticket data only. Tool calls update [tickets.json](tickets.json) immediately.

## What you will learn

- how a browser and MCP server can share one ticket store
- how MCP exposes application operations as agent tools
- how VS Code connects to a local MCP server over stdio
- how a local Agent Framework agent connects to a local MCP server over HTTP
- how to verify tool actions in both the terminal and browser

## 1. Explore the system

Review these files before running anything:

| File | Responsibility |
|------|----------------|
| [index.html](index.html) | Accessible ticket-management interface |
| [script.js](script.js) | Browser interactions and API requests |
| [web_server.py](web_server.py) | Static web server and ticket API on port 3000 |
| [ticket_store.py](ticket_store.py) | Validation and JSON persistence shared by both servers |
| [mcp_server.py](mcp_server.py) | MCP tools over stdio or streamable HTTP |
| [agent_with_mcp.py](agent_with_mcp.py) | Local interactive Agent Framework agent connected to MCP |
| [tickets.json](tickets.json) | Synthetic local ticket records |

The server exposes these tools:

| Tool | Description |
|------|-------------|
| `list_tickets` | List tickets, optionally filtered by status and priority |
| `get_ticket` | Get one ticket by numeric ID |
| `create_ticket` | Create a ticket with a title, description, priority, and assignee |
| `update_ticket` | Change a ticket's status or assignee |
| `close_ticket` | Mark a ticket as Closed |

Ask GitHub Copilot to trace one operation, such as closing a ticket, from the MCP tool to
the store and then to the browser API. Confirm that both interfaces use the same
`tickets.json` file.

**Checkpoint:** You can explain which process owns each port, where ticket data is stored,
and how an MCP tool changes data shown by the browser.

## 2. Run the web application

From this folder, start the web server:

```bash
python web_server.py
```

Open `http://localhost:3000`. Create a synthetic ticket, edit it, and close it. Reload the
page after each action to confirm the change persists.

No frontend build is required. Port 3000 is reserved for the web application so port 8000
remains available for the MCP server.

**Checkpoint:** The browser lists the sample tickets and can create, edit, and close a
ticket without errors.

## 3. Connect the MCP server to VS Code

Create or update `.vscode/mcp.json` in the repository root:

```json
{
  "servers": {
    "ticketing": {
      "command": "${workspaceFolder}/.venv/Scripts/python.exe",
      "args": ["${workspaceFolder}/04-Agent Examples/05-support-ticket-system (ADVANCED)/mcp_server.py"],
      "env": {}
    }
  }
}
```

On macOS or Linux, use `${workspaceFolder}/.venv/bin/python`. Reload the VS Code window,
open GitHub Copilot Chat in Agent mode, and confirm that the five ticket tools are available.

Test read operations first:

1. Ask for all open Critical tickets.
2. Ask for the details of one returned ticket ID.
3. Compare the result with the browser and [tickets.json](tickets.json).

Then test a write with synthetic data. Ask GitHub Copilot to create a Low-priority ticket named
`Workshop MCP verification`, inspect the exact tool arguments, and confirm the result in
the browser. MCP writes persist immediately; this local server does not implement its own
approval workflow.

**Checkpoint:** VS Code discovers all five tools, read results match the browser, and a
created ticket appears after the browser reloads.

## 4. Run the local Agent Framework agent

The agent process runs locally and uses the same local MCP tools over streamable HTTP.
Its model requests use the Foundry endpoint configured in `.env`. Keep the web server
running and use two more terminals from this folder.

Terminal 2:

```bash
python mcp_server.py --http
```

The MCP endpoint is now available at `http://localhost:8000/mcp`.

Terminal 3:

```bash
az account show
python agent_with_mcp.py
```

Try this sequence:

1. `List all open Critical tickets.`
2. `Create a Low-priority ticket called Agent verification with a synthetic description.`
3. `Assign the new ticket to Workshop Technician and move it to In Progress.`
4. `Close that ticket.`
5. `quit`

Reload the browser between actions. The agent should confirm each action and preserve the
conversation context when you refer to "that ticket."

**Checkpoint:** The local agent authenticates through the active Azure CLI session, calls
the local HTTP MCP server, and every confirmed mutation appears in the browser.

## 5. Extend it with GitHub Copilot

Choose one small extension:

- add a read-only tool that summarizes ticket counts by priority and status
- add a browser filter for assigned technician
- add a ticket history field and display it in the edit dialog
- add focused tests for invalid priorities, statuses, and missing required fields

Ask GitHub Copilot to identify the affected files before editing. Review the proposed data shape,
make one change at a time, and repeat the relevant checkpoint. Keep MCP tool descriptions
specific enough that an agent can select the correct tool without guessing.

Do not add real employee names, customer details, credentials, or production tickets.

**Checkpoint:** The extension works through every affected interface, existing ticket
operations still work, and its behavior is documented here.

## Project structure

```text
05-support-ticket-system (ADVANCED)/
|-- index.html       # Accessible browser interface
|-- styles.css       # Responsive styling
|-- script.js        # Browser behavior and API calls
|-- tickets.json     # Synthetic persistent ticket data
|-- ticket_store.py  # Shared validation and storage
|-- web_server.py    # Web application and API server
|-- mcp_server.py    # MCP server (stdio or streamable HTTP)
|-- agent_with_mcp.py # Local interactive Agent Framework agent
|-- requirements.txt # References the repository root requirements
`-- README.md        # Workshop instructions
```

## Done when

- The web application works at `http://localhost:3000`.
- VS Code discovers all five MCP tools over stdio.
- Read results match the shared ticket store.
- MCP and Agent Framework mutations appear in the browser after reload.
- The local Agent Framework agent authenticates only through Azure CLI.
- All test data remains synthetic.
