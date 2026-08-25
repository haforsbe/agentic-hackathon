# Agentic Hackathon

![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

A hands-on hackathon for building AI agents with the **Microsoft Agent Framework**, **Microsoft Foundry**, and **GitHub Copilot**. Work through progressive labs — from a first "hello world" agent all the way to hosted deployments and MCP-powered tool integration.

## Learning path

| Lab | Focus | What you'll build |
|-----|-------|-------------------|
| [01 — Foundry Agents](01-microsoft-foundry-agents/) | Microsoft Foundry | Responses API, chat with agents, create prompt agents |
| [02 — Agent Framework Advanced](02-agent-framework%20ADVANCED/) | Core SDK concepts | Agents, tools, multi-turn sessions, memory, workflows, remote MCP |
| [03 — GitHub Copilot](03-github-copilot/) | GitHub Copilot + MCP | Build a ticketing app with inline suggestions, agents, MCP server, and Agent Framework integration |
| [04 — Agent Examples](04-Agent%20Examples/) | Agent examples | Build Foundry prompt agents or run an advanced MCP-enabled support ticket system |

Each folder has its own README with detailed instructions and sample descriptions.

## Prerequisites

- **Python 3.12+** — [python.org/downloads](https://www.python.org/downloads/)
- **VS Code** — [code.visualstudio.com](https://code.visualstudio.com/)
- **Azure CLI** — [Install docs](https://learn.microsoft.com/cli/azure/install-azure-cli)
- **Microsoft Foundry project** with a compatible deployed chat model (the tested example uses `gpt-4.1`)
- **GitHub Copilot** access (for Lab 03)

For complete step-by-step setup instructions, see:

| Guide | Scope |
|-------|-------|
| [Prereqs_Foundry.md](Prereqs_Foundry.md) | Labs 01, 02, and 04 (Foundry + Agent Framework) |
| [Prereqs_GHCP.md](Prereqs_GHCP.md) | Lab 03 (GitHub Copilot + Azure add-ons) |
| [Prereqs.md](Prereqs.md) | Combined guide (all labs) |

## Quickstart

### 1) Clone and open the repo

```powershell
git clone <repo-url>
cd agentic-hackathon
code .
```

### 2) Create and activate a virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Authenticate to Azure

Labs 01 and 02 use `AzureCliCredential` exclusively, so the active Azure CLI session is their only authentication source:

```bash
az login
az account show
```

If needed, select the subscription that contains your Foundry project with `az account set --subscription "<subscription-name-or-id>"`.

### 5) Configure environment variables

Copy the example and fill in your values:

```bash
cp example.env .env
```

Key variables (see [example.env](example.env) for all options):

| Variable | Description |
|----------|-------------|
| `AZURE_AI_PROJECT_ENDPOINT` | Your Microsoft Foundry project endpoint |
| `AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME` | Model deployment name (e.g. `gpt-4.1`) |
| `AGENT_NAME` | Foundry prompt agent name, used by Labs 01 and 04 |
| `AZURE_CLI_PROCESS_TIMEOUT` | Optional Azure CLI token timeout in seconds, used by Labs 02 and 04 |

### 6) Run your first agent

```bash
python "02-agent-framework ADVANCED/01_hello_agent.py"
```

## Project structure

```
agentic-hackathon/
├── 01-microsoft-foundry-agents/  # Microsoft Foundry quickstarts (3 scripts)
├── 02-agent-framework ADVANCED/  # Advanced Agent Framework samples (6 scripts)
├── 03-github-copilot/            # GitHub Copilot tutorial with MCP integration
├── 04-Agent Examples/            # Foundry challenges and advanced MCP support ticket system
├── example.env                  # Environment variable template
├── requirements.txt             # Python dependencies (all labs)
├── Prereqs.md                   # Combined setup guide
├── Prereqs_Foundry.md           # Setup for Labs 01, 02, and 04
└── Prereqs_GHCP.md              # Setup for Lab 03 (GitHub Copilot)
```
