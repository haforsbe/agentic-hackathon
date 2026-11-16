# Support Ticket System

Optional local example for an IT support capstone, not a prerequisite for the
[coached workshop](../../workshop/START.md). The browser UI and MCP (Model
Context Protocol) server share a synthetic ticket store in `tickets.json`.
The local agent calls a model in Microsoft Foundry; it is not a deployed
Microsoft Foundry agent.

**Workshop Path 2:** the optional advanced local IT ticketing route requires
one local agent, a local MCP server and this local app, reusing the participant's
existing Microsoft Foundry model deployment. There is no Microsoft Foundry agent
deployment or workflow. The current `agent_with_mcp.py` is reference material,
not that finished route: it uses a terminal chat loop instead of the required
GitHub Copilot app chat relay. Its MCP server also does not enforce human approval
for writes or a read-only agent boundary.
Follow [the local route and preparation blocker](../../workshop/CAPSTONE.md#optional-advanced-local-it-ticketing-route-17-19);
do not create Microsoft Foundry resources or claim runtime/approval readiness from this
example as-is.

## Run the browser app

From the repository root, open a terminal and enter:

```powershell
Set-Location ".\examples\support-ticket-system"
python web_server.py
```

Open http://localhost:3000. Create, edit, or close a synthetic ticket and reload
the page to confirm persistence. Python is required for this optional example;
the browser app uses only its standard library and needs no frontend build.

## Run the MCP server and optional local agent

Use an isolated Python environment. From this example folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python mcp_server.py --http
```

On macOS/Linux, activate with `source .venv/bin/activate` instead.
The MCP server listens at http://localhost:8000/mcp. It exposes `list_tickets`,
`get_ticket`, `create_ticket`, `update_ticket`, and `close_ticket`.
Writes persist immediately; the server does not implement its own approval flow.
Keep this unauthenticated demo local and do not expose it through a public
tunnel. Foundry cannot directly call a server on your laptop's localhost.

For the optional local agent, install Azure CLI following the
[official instructions](https://learn.microsoft.com/cli/azure/install-azure-cli)
and sign in with `az login`. Create an ignored `.env` file in this example
folder with your project endpoint and selected deployment:

```dotenv
AZURE_AI_PROJECT_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project>
AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME=<your-model-deployment>
AZURE_CLI_PROCESS_TIMEOUT=60
```

In another terminal, activate the same environment, return to this example
folder, and run:

```powershell
python agent_with_mcp.py
```

Model requests may incur charges. Test reads before writes and compare each
result with the browser after reloading. Use synthetic data only; do not enter
production tickets, credentials, or real personal information. Type `quit` to
exit the agent, and stop each local server with Ctrl+C in its terminal.

## Files

| File | Purpose |
|------|---------|
| `index.html`, `styles.css`, `script.js` | Browser interface |
| `web_server.py` | Web application and ticket API on port 3000 |
| `ticket_store.py`, `tickets.json` | Shared local ticket persistence |
| `mcp_server.py` | MCP tools over HTTP or stdio |
| `agent_with_mcp.py` | Optional interactive Agent Framework client |
| `requirements.txt` | Dependencies scoped to this example |

These are demonstration components, not a production service. Rehearse
concurrent browser/MCP operations before using them in a cohort; the
file-backed store is not a production multi-process database. Keep local ticket
changes synthetic and review them before committing.
