# Prereqs and Setup Guide

This guide is a **full sequence** for running the examples in this repo from a machine that does not have Python or VS Code installed.

Scope covered:
- `01-agent-framework`
- `02-microsoft-foundry-agents`
- `03-microsoft-foundry-hosted-agents` (**optional**)

---

## 1) Install required software (in this order)

1. **Visual Studio Code**
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

You need an Azure subscription with access to Azure AI Foundry and model deployments.

1. Sign in to Azure portal: https://portal.azure.com/
2. Open Azure AI Foundry: https://ai.azure.com/
3. Create or use an existing **Foundry project**.
4. Deploy a chat model (for example, `gpt-4o` or `gpt-4.1-mini`).
5. Copy these values (you will use them later):
   - **Project endpoint** (example: `https://<resource>.services.ai.azure.com/api/projects/<project>`)
   - **Model deployment name**
6. (Optional!!!)  If you plan to run web/foundry-tool hosted samples, also prepare:
   - Bing Grounding connection (for web-search sample)
   - Optional Foundry MCP tool connection id (for foundry-tools sample)



---







# Prereqs for GitHub Copilot Enterprise

This guide explains how to install and set up **GitHub Copilot Enterprise** and the key **Azure add-ons** in VS Code.

## Important roles

Some steps must be done by an **Enterprise/Organization Admin** (license + policy), while others are done by each **Developer** (local install/sign-in).

---

## 1) Admin setup: enable GitHub Copilot Enterprise

> These steps are completed by your GitHub Enterprise/Org admin.

1. Confirm your company is on **GitHub Enterprise Cloud** and has purchased **Copilot Enterprise**.
   - Copilot plan overview: https://docs.github.com/en/copilot/about-github-copilot/subscription-plans-for-github-copilot

2. Enable Copilot for the enterprise/org and configure policies.
   - Getting started with Copilot plan: https://docs.github.com/en/copilot/how-tos/manage-your-account/get-started-with-a-copilot-plan

3. Assign Copilot seats to users/teams.
   - Seat management docs: https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-copilot-seat-assignments

4. (Recommended) Configure SSO / identity governance (Microsoft Entra ID).
   - Enterprise identity + access docs: https://docs.github.com/en/enterprise-cloud@latest/admin/identity-and-access-management

---

## 2) Developer setup: GitHub sign-in and entitlement check

1. Sign in to GitHub in your browser with your company account.
2. In VS Code, sign in to GitHub when prompted by Copilot extensions.
3. Validate you have Copilot access:
   - Copilot quickstart: https://docs.github.com/en/copilot/quickstart

---

## 3) Install Copilot extensions in VS Code

Install these extensions:

1. **GitHub Copilot**
   - Marketplace: https://marketplace.visualstudio.com/items?itemName=GitHub.copilot

2. **GitHub Copilot Chat**
   - Marketplace: https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat

3. **GitHub Copilot for Azure** (Azure add-on)
   - Marketplace: https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat-azure
   - Microsoft Learn quickstart: https://learn.microsoft.com/azure/developer/github-copilot-azure/get-started

---

## 4) Install Azure tooling add-ons in VS Code

These are recommended Azure add-ons for Copilot workflows:

1. **Azure Tools Extension Pack**
   - Marketplace: https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack

2. **Azure MCP Server extension** (optional if already included via Copilot for Azure)
   - Marketplace: https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azure-mcp-server
   - Setup guide: https://learn.microsoft.com/azure/developer/azure-mcp-server/get-started/tools/visual-studio-code

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
3. If you use multiple Entra tenants, set tenant in Copilot for Azure:
   - In chat: `@azure /changeTenant`
   - Tenant setup reference: https://learn.microsoft.com/azure/developer/github-copilot-azure/get-started#set-your-default-tenant

---

## 6) Verify Copilot + Azure add-ons are working

In Copilot Chat (Agent mode), run these prompts:

1. `What Azure tools are available?`
2. `Do I have any Azure resources currently running?`
3. `What is the az command to list all my storage accounts ordered by location?`

Reference: https://learn.microsoft.com/azure/developer/github-copilot-azure/get-started#install-github-copilot-for-azure

---

## 7) Recommended enterprise governance settings

Have admins review these before broad rollout:

1. Seat assignment model (all users vs selected groups)
2. Content exclusion / policy controls for Copilot
3. SSO/SCIM lifecycle management with Entra ID
4. Approved extension list for VS Code in managed environments
5. Azure role-based access controls (least privilege) for subscriptions used by developers

---

## 8) Common issues

1. **Copilot not available in VS Code**
   - Usually missing seat assignment or wrong GitHub account signed in.

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
- Copilot in VS Code setup: https://code.visualstudio.com/docs/copilot/setup
- Copilot Chat in VS Code: https://code.visualstudio.com/docs/copilot/getting-started-chat
- GitHub Copilot: https://marketplace.visualstudio.com/items?itemName=GitHub.copilot
- GitHub Copilot Chat: https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat
- GitHub Copilot for Azure: https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat-azure
- GitHub Copilot for Azure quickstart: https://learn.microsoft.com/azure/developer/github-copilot-azure/get-started
- Azure MCP Server extension: https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azure-mcp-server
- Azure MCP Server setup: https://learn.microsoft.com/azure/developer/azure-mcp-server/get-started/tools/visual-studio-code