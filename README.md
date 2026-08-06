# Agentic Hackathon

![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

A hands-on hackathon for building AI agents with the **Microsoft Agent Framework**, **Azure AI Foundry**, and **GitHub Copilot**. Work through progressive labs — from a first "hello world" agent all the way to hosted deployments and MCP-powered tool integration.

## Learning path

| Lab | Focus | What you'll build |
|-----|-------|-------------------|
| [01 — Agent Framework](01-agent-framework/) | Core SDK concepts | Agents, tools, multi-turn sessions, memory, workflows, remote MCP |
| [02 — Foundry Agents](02-microsoft-foundry-agents/) | Azure AI Foundry | Responses API, chat with agents, create prompt agents |
| [03 — Hosted Agents](03-microsoft-foundry-hosted-agents/) | Deployment scenarios | Echo agent, web search, RAG, workflows, human-in-the-loop |
| [05 — GitHub Copilot](05-github-copilot/) | Copilot + MCP | Build a ticketing app with inline suggestions, agents, MCP server, and Agent Framework integration |

Each folder has its own README with detailed instructions and sample descriptions.

## Prerequisites

- **Python 3.12+** — [python.org/downloads](https://www.python.org/downloads/)
- **VS Code** — [code.visualstudio.com](https://code.visualstudio.com/)
- **Azure CLI** — [Install docs](https://learn.microsoft.com/cli/azure/install-azure-cli)
- **Azure AI Foundry project** with a deployed chat model (e.g. `gpt-4.1`)
- **GitHub Copilot** access (for Lab 05)

For complete step-by-step setup instructions, see:

| Guide | Scope |
|-------|-------|
| [Prereqs_Foundry.md](Prereqs_Foundry.md) | Labs 01–03 (Agent Framework + Foundry) |
| [Prereqs_GHCP.md](Prereqs_GHCP.md) | Lab 05 (GitHub Copilot Enterprise + Azure add-ons) |
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

```bash
az login
```

### 5) Configure environment variables

Copy the example and fill in your values:

```bash
cp example.env .env
```

Key variables (see [example.env](example.env) for all options):

| Variable | Description |
|----------|-------------|
| `AZURE_AI_PROJECT_ENDPOINT` | Your Azure AI Foundry project endpoint |
| `AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME` | Model deployment name (e.g. `gpt-4.1`) |
| `AGENT_NAME` | Foundry prompt agent name, used by Lab 02 agent samples |
| `AZURE_CLI_PROCESS_TIMEOUT` | Optional Azure CLI token timeout in seconds, used by Labs 01 and 05 |

### 6) Run your first agent

```bash
python 01-agent-framework/01_hello_agent.py
```

## Project structure

```
agentic-hackathon/
├── 01-agent-framework/          # Progressive Agent Framework samples (6 scripts)
├── 02-microsoft-foundry-agents/ # Azure AI Foundry quickstarts (3 scripts)
├── 03-microsoft-foundry-hosted-agents/  # Hosted agent deployment scenarios
├── 05-github-copilot/           # Copilot tutorial with MCP integration
├── example.env                  # Environment variable template
├── requirements.txt             # Python dependencies (all labs)
├── Prereqs.md                   # Combined setup guide
├── Prereqs_Foundry.md           # Setup for Labs 01–03
└── Prereqs_GHCP.md              # Setup for Lab 05 (Copilot)
```
