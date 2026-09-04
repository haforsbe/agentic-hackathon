# Agentic Hackathon

![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

A hands-on hackathon for building AI agents with the **Microsoft Agent Framework**, **Microsoft Foundry**, and **GitHub Copilot**. Work through progressive labs — from a first "hello world" agent all the way to hosted deployments and MCP-powered tool integration.

## Learning path

| Lab | Focus | What you'll build |
|-----|-------|-------------------|
| [01 — Foundry Agents](01-microsoft-foundry-agents/) | Microsoft Foundry | Responses API, chat with agents, create prompt agents |
| [02 — Agent Framework Advanced](02-agent-framework%20ADVANCED/) | Core SDK concepts | Agents, tools, multi-turn sessions, memory, workflows, remote MCP |
| [03 — GitHub Copilot](03-github-copilot/) | GitHub Copilot | Build a small HTML page with inline suggestions, agents, custom instructions, and smart actions |
| [04 — Agent Examples](04-Agent%20Examples/) | GitHub Copilot + Foundry | Generate Foundry agent tasks in VS Code or run an advanced MCP support system |

Each folder has its own README with detailed instructions and sample descriptions.

## Prerequisites

- **Python 3.12+** — [python.org/downloads](https://www.python.org/downloads/)
- **VS Code** — [code.visualstudio.com](https://code.visualstudio.com/)
- **Azure CLI** — [Install docs](https://learn.microsoft.com/cli/azure/install-azure-cli)
- **Microsoft Foundry project** with a compatible deployed chat model (the tested example uses `gpt-4.1`)
- **GitHub Copilot** access (for Labs 03 and 04)

For complete step-by-step setup instructions, see:

| Guide | Scope |
|-------|-------|
| [Prereqs_Participant.md](Prereqs_Participant.md) | Laptop, access, Foundry, Agent Framework, and GitHub Copilot setup for training participants |

## Quickstart

### 1) Clone and open the repo (if not already done)

```powershell
git clone <repo-url>
cd agentic-hackathon
code .
```

### 2) Create and activate a virtual environment

A virtual environment is an isolated Python workspace for this project. It keeps the
packages installed for the hackathon separate from your system Python and from other
projects, preventing dependency and version conflicts.

Creating `.venv` prepares that isolated workspace. Activating it makes the `python` and
`pip` commands in the current terminal use the environment, so the dependencies in the
next step are installed and run in the correct place.

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

Dependencies are external Python packages that the labs use, including the Microsoft
Foundry SDK, Agent Framework, Azure authentication libraries, and MCP support. The
`requirements.txt` file lists the versions tested with this project so every participant
uses a consistent setup.

Run the command below after activating `.venv`. `pip` will install the required packages
into that virtual environment without changing your system Python installation.

```bash
pip install -r requirements.txt
```

### 4) Authenticate to Azure

Labs 01, 02, and 04 use Microsoft Entra authentication through the Azure Identity
library. Sign in with Azure CLI before running them:

```bash
az login
az account show
```

If needed, select the subscription that contains your Foundry project with `az account set --subscription "<subscription-name-or-id>"`.

Lab 01 also includes an optional Responses-only API-key sample. Its project client still
uses Azure CLI authentication; keep the API key only in `.env`.

### 5) Configure environment variables

Environment variables provide settings that can change between participants and
environments, such as a Foundry project endpoint, model deployment, or agent name. The
labs read these values at runtime so personal configuration does not need to be written
directly into the Python files.

`example.env` is a safe template containing the required variable names and placeholder
values. Copy it to `.env`, replace the placeholders with your own values, and keep that
file private. The repository ignores `.env` because it may contain credentials or other
sensitive configuration; never commit or share it.

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
├── 03-github-copilot/            # GitHub Copilot tutorial with a small HTML page
├── 04-Agent Examples/            # Copilot-built Foundry agents and advanced MCP system
├── example.env                  # Environment variable template
├── requirements.txt             # Python dependencies (all labs)
└── Prereqs_Participant.md       # Participant setup and access checklist
```
