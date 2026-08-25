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
   - Azure MCP Server requires VS Code `1.103` or later. GitHub Copilot Chat tracks the latest VS Code release, so keeping VS Code current is recommended.

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

You need an Azure subscription with access to Microsoft Foundry and model deployments.

1. Sign in to Azure portal: https://portal.azure.com/
2. Open Microsoft Foundry: https://ai.azure.com/
3. Create or use an existing **Microsoft Foundry V2 project**. Foundry V1 projects are not supported by these samples.
4. Deploy a chat model that supports the samples (for example, `gpt-4.1`). Use the deployment name, which can differ from the model name, in your `.env` file.
5. Copy these values (you will use them later):
   - **Project endpoint** (example: `https://<resource>.services.ai.azure.com/api/projects/<project>`)
   - **Model deployment name**
6. (Optional!!!)  If you plan to run web/foundry-tool hosted samples, also prepare:
   - Bing Grounding connection (for web-search sample)
   - Optional Foundry MCP tool connection id (for foundry-tools sample)

### Authenticate local Foundry samples with Azure CLI

The local Python samples in `01-microsoft-foundry-agents` and `02-agent-framework ADVANCED` use `AzureCliCredential` exclusively. They do not fall back to browser broker, environment, managed identity, or other credential types.

```powershell
az login
az account show
```

If you have multiple subscriptions, select the subscription that contains your Foundry project:

```powershell
az account set --subscription "<subscription-name-or-id>"
```



---







# Prereqs for GitHub Copilot

This guide explains how to install and set up **GitHub Copilot** and the key **Azure add-ons** in VS Code. GitHub Enterprise is not required. You can use an eligible individual GitHub Copilot plan or access provided by an organization.

## Important roles

For an individual plan, the developer manages access and local setup. For an organization-managed plan, an **Organization/Enterprise Admin** manages seat assignment and policies while each **Developer** completes the local install and sign-in.

---

## 1) Confirm access to GitHub Copilot

GitHub Enterprise is not required. Available features and usage limits depend on your GitHub Copilot plan.

For this workshop, **GitHub Copilot Pro or higher, or an organization-provided Copilot seat, is recommended**. GitHub measures usage with **GitHub AI Credits**, not a user-managed token balance. Copilot Free has a limited credit allowance and may run out during repeated Agent mode exercises.

Before the workshop:

- In VS Code, select the GitHub Copilot icon and confirm your plan is active and has AI Credits remaining.
- If your access is organization-managed, ask your admin to confirm that Copilot is enabled and that the organization's AI Credit policy or budget allows workshop usage.
- Use the plan overview below to compare current credit allowances because plan limits can change.

1. Choose or confirm an eligible individual or organization-managed GitHub Copilot plan.
   - GitHub Copilot plan overview: https://docs.github.com/en/copilot/about-github-copilot/subscription-plans-for-github-copilot

2. For an individual plan, activate GitHub Copilot on your GitHub account.
   - Getting started with a GitHub Copilot plan: https://docs.github.com/en/copilot/how-tos/manage-your-account/get-started-with-a-copilot-plan

3. For an organization-managed plan, ask an Organization/Enterprise Admin to enable GitHub Copilot, configure policies, and assign seats.
   - Seat management docs: https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-copilot-seat-assignments

4. (Optional, managed organizations) Configure SSO and identity governance with Microsoft Entra ID.
   - Enterprise identity + access docs: https://docs.github.com/en/enterprise-cloud@latest/admin/identity-and-access-management

---

## 2) Developer setup: GitHub sign-in and entitlement check

1. Sign in to GitHub in your browser with the account that has GitHub Copilot access.
2. In VS Code, sign in to GitHub when prompted by GitHub Copilot extensions.
3. Validate you have GitHub Copilot access:
   - GitHub Copilot quickstart: https://docs.github.com/en/copilot/quickstart

---

## 3) Install GitHub Copilot extensions in VS Code

Install these extensions:

1. **GitHub Copilot**
   - Marketplace: https://marketplace.visualstudio.com/items?itemName=GitHub.copilot
   - Installing GitHub Copilot also installs its companion **GitHub Copilot Chat** extension. Confirm that both are enabled in VS Code.
   - Marketplace: https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat

2. **GitHub Copilot for Azure** (Azure add-on)
   - Marketplace: https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat-azure
   - Microsoft Learn quickstart: https://learn.microsoft.com/azure/developer/github-copilot-azure/get-started

---

## 4) Install Azure tooling add-ons in VS Code

These are recommended Azure add-ons for GitHub Copilot workflows:

1. **Azure Tools Extension Pack**
   - Marketplace: https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack

2. **Azure MCP Server extension** (recommended for the MCP exercises; requires VS Code `1.103` or later)
   - Marketplace: https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azure-mcp-server
   - Setup guide: https://learn.microsoft.com/azure/developer/azure-mcp-server/get-started/tools/visual-studio-code
   - After installation, open `MCP: List Servers` from the Command Palette and confirm **Azure MCP Server ext** is running.

3. (Optional, Python projects) **Python extension**
   - Marketplace: https://marketplace.visualstudio.com/items?itemName=ms-python.python

---

## 5) Sign in to Azure from VS Code

1. In terminal:

```powershell
az login
az account show
```

2. In VS Code, open Azure view and select **Sign in to Azure** if needed.
3. If you use multiple Entra tenants, set tenant in GitHub Copilot for Azure:
   - In chat: `@azure /changeTenant`
   - Tenant setup reference: https://learn.microsoft.com/azure/developer/github-copilot-azure/get-started#set-your-default-tenant

---

## 6) Verify GitHub Copilot + Azure add-ons are working

In GitHub Copilot Chat (Agent mode), run these prompts:

1. `What Azure tools are available?`
2. `Do I have any Azure resources currently running?`
3. `What is the az command to list all my storage accounts ordered by location?`

Reference: https://learn.microsoft.com/azure/developer/github-copilot-azure/get-started#install-github-copilot-for-azure

---

## 7) Recommended organization governance settings

For organization-managed plans, have admins review these before broad rollout:

1. Seat assignment model (all users vs selected groups)
2. Content exclusion / policy controls for GitHub Copilot
3. SSO/SCIM lifecycle management with Entra ID
4. Approved extension list for VS Code in managed environments
5. Azure role-based access controls (least privilege) for subscriptions used by developers

---

## 8) Common issues

1. **GitHub Copilot not available in VS Code**
   - Confirm the signed-in GitHub account has an active individual plan or an assigned organization seat.

2. **Azure tools return auth/tenant errors**
   - Run `az login` again and switch tenant via `@azure /changeTenant`.

3. **No Azure context in chat**
   - Ensure `GitHub Copilot for Azure` extension is installed and enabled.

---

## 9) Quick links bundle

- VS Code: https://code.visualstudio.com/Download
- Git: https://git-scm.com/downloads
- Azure CLI: https://learn.microsoft.com/cli/azure/install-azure-cli
- Azure Developer CLI: https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd
- GitHub Copilot in VS Code setup: https://code.visualstudio.com/docs/copilot/setup
- GitHub Copilot Chat in VS Code: https://code.visualstudio.com/docs/copilot/getting-started-chat
- GitHub Copilot: https://marketplace.visualstudio.com/items?itemName=GitHub.copilot
- GitHub Copilot Chat: https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat
- GitHub Copilot for Azure: https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat-azure
- GitHub Copilot for Azure quickstart: https://learn.microsoft.com/azure/developer/github-copilot-azure/get-started
- Azure MCP Server extension: https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azure-mcp-server
- Azure MCP Server setup: https://learn.microsoft.com/azure/developer/azure-mcp-server/get-started/tools/visual-studio-code

---

## 10) Tested Python package baseline

Python `3.12+` is the workshop baseline. The repository pins a tested, mutually compatible package set in `requirements.txt`; key versions are:

| Package | Tested version |
|---|---:|
| `agent-framework-core` | `1.13.0` |
| `agent-framework-openai` | `1.12.0` |
| `azure-ai-projects` | `2.4.0` |
| `azure-identity` | `1.25.3` |
| `mcp` | `1.26.0` |

Do not upgrade packages independently during the workshop. Install or restore the tested set with `pip install -r requirements.txt`.