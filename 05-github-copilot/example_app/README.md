# IT Support Ticketing System

A demo web application for managing IT support tickets — create, edit, and close tickets with priority levels and technician assignments.

## Features

- **Create tickets** with title, description, priority (Low / Medium / High / Critical), and assigned technician
- **Edit tickets** — update any field via a modal dialog
- **Close tickets** — mark tickets as Closed with one click
- **Sample data** — pre-populated with 7 realistic tickets
- **Responsive design** — works on desktop, tablet, and mobile
- **Accessible** — semantic HTML, ARIA attributes, keyboard navigation

## Running Locally

No build tools or dependencies are required — just a web browser.

Using Python (built-in):

```bash
# Python 3 — use port 3000 so it doesn't conflict with the MCP server on port 8000
python -m http.server 3000

# Then open http://localhost:3000 in your browser
```

## MCP Server

The app includes an MCP (Model Context Protocol) server that exposes the ticketing system as tools via streamable HTTP. This lets AI agents (like GitHub Copilot) create, query, and update tickets programmatically.

### Tools exposed

| Tool | Description |
|------|-------------|
| `list_tickets` | List all tickets, with optional `status` and `priority` filters |
| `get_ticket` | Get details of a specific ticket by ID |
| `create_ticket` | Create a new ticket with title, description, priority, and assignee |
| `update_ticket` | Update a ticket's status or assignee |
| `close_ticket` | Close a ticket by ID |

### Starting the MCP server

1. Install dependencies (one time):

   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:

   ```bash
   # For VS Code integration (stdio transport — used by .vscode/mcp.json):
   python mcp_server.py

   # For HTTP access (used by agent_with_mcp.py or external clients):
   python mcp_server.py --http
   ```

   With `--http`, the server starts on `http://localhost:8000/mcp` using streamable HTTP transport.

   > **Note:** Port 8000 is reserved for the MCP server. If you also want to serve the web app locally, use a different port (e.g. `python -m http.server 3000`).

### Configuring in VS Code

Create or update `.vscode/mcp.json` in your workspace root:

```json
{
  "servers": {
    "ticketing": {
      "command": "${workspaceFolder}/.venv/Scripts/python.exe",
      "args": ["${workspaceFolder}/05-github-copilot/example_app/mcp_server.py"],
      "env": {}
    }
  }
}
```

> **Note:** On macOS/Linux, use `.venv/bin/python` instead. The command must point to the venv where `mcp` is installed — using bare `python` will fail if it resolves to the system Python.

Then restart VS Code or reload the window. The ticketing tools will be available to any agent in the Chat view.

## Project Structure

```
example_app/
├── index.html       # Markup (semantic HTML5)
├── styles.css       # Styling (modern CSS, responsive)
├── script.js        # Application logic (vanilla JS)
├── mcp_server.py    # MCP server (Python, streamable HTTP)
├── requirements.txt # Python dependencies for MCP server
└── README.md        # This file
```
