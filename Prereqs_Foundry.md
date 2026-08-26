# Prereqs and Setup Guide

This guide is a **full sequence** for running the examples in this repo from a machine that does not have Python or VS Code installed.

Scope covered:
- `01-microsoft-foundry-agents`
- `02-agent-framework ADVANCED`
- `04-Agent Examples`

---

## 1) Install required software (in this order)

1. **Visual Studio Code (latest stable release)**
   - Download: https://code.visualstudio.com/Download

2. **Python 3.12+**
   - Download: https://www.python.org/downloads/
   - During install on Windows, check **"Add python.exe to PATH"**.

3. **Git**
   - Download: https://git-scm.com/downloads

4. **Azure CLI**
   - Install docs (Windows/macOS/Linux): https://learn.microsoft.com/cli/azure/install-azure-cli

5. **(Optional, for hosted-agent deployment scenarios) Azure Developer CLI (`azd`)**
   - Install docs: https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd

6. **(Optional, for local container builds) Docker Desktop**
   - Download: https://www.docker.com/products/docker-desktop/

---

## 2) Create/prepare Azure resources

You need a working Microsoft Foundry project in an Azure subscription. Your account must have sufficient access rights in that project to deploy models and create or manage agents. If an administrator controls project access, ask them to grant these permissions before the workshop.

1. Sign in to Azure portal: https://portal.azure.com/
2. Open Microsoft Foundry: https://ai.azure.com/
3. Create or use an existing **Microsoft Foundry V2 project** and confirm that you can deploy models and create agents in it. Foundry V1 projects are not supported by these samples.
4. Deploy a chat model that supports the samples (for example, `gpt-4.1`). Use the deployment name, which can differ from the model name, in your `.env` file.
5. Copy these values (you will use them later):
   - **Project endpoint** (example: `https://<resource>.services.ai.azure.com/api/projects/<project>`)
   - **Model deployment name**
6. If you plan to run web/foundry-tool hosted samples, also prepare:
   - Bing Grounding connection (for web-search sample)
   - Optional Foundry MCP tool connection id (for foundry-tools sample)

---

## 3) Open the project in VS Code

1. Launch VS Code.
2. `File -> Open Folder...` and select your cloned repo folder:
   - `<your-clone-path>\agentic-hackathon`
3. Open a new terminal in VS Code (`Terminal -> New Terminal`).

---

## 4) Authenticate with Azure CLI

The local Python samples in Labs 01, 02, and 04 use `AzureCliCredential` exclusively. They do not fall back to browser broker, environment, managed identity, or other credential types.

In the VS Code terminal:

```powershell
az login
az account show
```

If you have multiple subscriptions, set the one you want:

```powershell
az account set --subscription "<subscription-name-or-id>"
```

---

## 5) Create and activate a Python virtual environment

From repo root (`agentic-hackathon`):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
pip --version
```

If PowerShell blocks activation, run once as needed:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

---

## 6) Install dependencies for 01 and 02 samples

From repo root:

```powershell
pip install -r requirements.txt
```

The repository pins a tested, mutually compatible package set. Key versions are:

| Package | Tested version |
|---|---:|
| `agent-framework-core` | `1.13.0` |
| `agent-framework-openai` | `1.12.0` |
| `azure-ai-projects` | `2.4.0` |
| `azure-identity` | `1.25.3` |
| `mcp` | `1.26.0` |

Do not upgrade packages independently during the workshop. Reinstall from `requirements.txt` if your environment differs.

---

## 7) Configure environment variables for 01 and 02

Use the values you collected in **Step 2 (Create/prepare Azure resources)**:
- `AZURE_AI_PROJECT_ENDPOINT` = your Foundry project endpoint from Step 2
- `AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME` = your model deployment name from Step 2

Create a `.env` file in repo root (`agentic-hackathon/.env`) with:

```dotenv
AZURE_AI_PROJECT_ENDPOINT=https://<your-resource>.services.ai.azure.com/api/projects/<your-project>
AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME=<your-model-deployment>
AZURE_CLI_PROCESS_TIMEOUT=60
AGENT_NAME=MyAgent
```

Notes:
- `PROJECT_ENDPOINT` works as compatibility alias for `AZURE_AI_PROJECT_ENDPOINT`.
- `MODEL_DEPLOYMENT_NAME` works as compatibility alias for `AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME`.
- Labs 01, 02, and 04 authenticate only through the active Azure CLI session (no API keys required).

---

## 8) Run examples in `01-microsoft-foundry-agents`

```powershell
cd 01-microsoft-foundry-agents
python 01-quickstart-responses.py
python 02-quickstart-create-agent.py
python 03-quickstart-chat-with-agent.py
cd ..
```

---

## 9) Run examples in `02-agent-framework ADVANCED`

```powershell
cd "02-agent-framework ADVANCED"
python 01_hello_agent.py
python 02_add_tools.py
python 03_multi_turn.py
python 04_memory.py
python 05_first_workflow.py
python 06_remote_mcp.py
cd ..
```

---

## 10) Useful links (one place)

- VS Code download: https://code.visualstudio.com/Download
- Python download: https://www.python.org/downloads/
- Git download: https://git-scm.com/downloads
- Azure CLI install: https://learn.microsoft.com/cli/azure/install-azure-cli
- Azure Developer CLI (`azd`) install: https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd
- Docker Desktop download: https://www.docker.com/products/docker-desktop/
- Azure portal: https://portal.azure.com/
- Microsoft Foundry portal: https://ai.azure.com/
- Microsoft Foundry documentation: https://learn.microsoft.com/azure/foundry/
- Hosted agents docs: https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents?view=foundry&tabs=cli

---

## 11) Recommended run order

1. `01-microsoft-foundry-agents/01-quickstart-responses.py`
2. `01-microsoft-foundry-agents/02-quickstart-create-agent.py`
3. `01-microsoft-foundry-agents/03-quickstart-chat-with-agent.py`
4. `02-agent-framework ADVANCED/01_hello_agent.py`
5. `02-agent-framework ADVANCED/02_add_tools.py`
6. `02-agent-framework ADVANCED/03_multi_turn.py`
7. Continue with the remaining advanced Agent Framework samples as needed.

This sequence starts with Foundry quickstarts and then moves into the advanced Agent Framework scenarios.
