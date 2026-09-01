# Participant Prerequisites

Use this checklist before the training. Everyone is expected to complete all labs, so all requirements are mandatory.

## Required for everyone: without these, you cannot participate

Complete all items in this section before the training. Without them, you cannot participate in the hands-on training.

Install:

1. **Visual Studio Code** (latest stable)
   - Download and install: https://code.visualstudio.com/Download
   - Open VS Code after installation.

2. **Git**
   - Download and install: https://git-scm.com/downloads
   - Check it works by running `git --version` in the VS Code terminal.

3. **Python 3.12 or newer**
   - Download and install: https://www.python.org/downloads/
   - Windows: select **Add python.exe to PATH** during installation.
   - Check it works by running `python --version` in the VS Code terminal.
   - Verify local script execution: create a file named `python-check.py` in VS Code with this content:

      ```python
      print("Local Python scripts work.")
      ```

      Run `python python-check.py` in the VS Code terminal. You should see `Local Python scripts work.`

4. **Azure CLI**
   - Install: https://learn.microsoft.com/cli/azure/install-azure-cli
   - You will use it to sign in to Azure and access Microsoft Foundry.

5. **Azure account and Microsoft Foundry permissions**
   - A Microsoft Azure subscription with valid credits for participating in the labs.
   - An Azure account with access to Microsoft Foundry.
   - Permission to create Microsoft Foundry projects, agents, and model deployments.
   - Sign in by running `az login` in the VS Code terminal.
   - Open https://ai.azure.com/ in your browser and confirm that you can access the training project and see the options to create projects, agents, and model deployments.

6. **GitHub account**
   - Sign in to GitHub in VS Code.
   - In VS Code, select the **Accounts** icon in the lower-left corner, choose **Sign in with GitHub**, and complete the browser sign-in.

7. **GitHub Copilot seat**
   - An active GitHub Copilot seat is required. Copilot Pro or an organization-provided seat is recommended for this training.
   - In VS Code, select the **Copilot** icon and confirm that Copilot is enabled for your account.

Install and enable these VS Code extensions in the VS Code Extensions view (`Ctrl+Shift+X`):

- **GitHub Copilot** (includes GitHub Copilot Chat)
- **GitHub Copilot for Azure**
- **Python**
- **Azure MCP Server** (requires VS Code 1.103 or newer)

For each extension, search for its name, select **Install**, and confirm that it shows as enabled.

## Verify your setup

Open a new VS Code terminal and run these commands:

```powershell
git --version
python --version
az --version
az login
az account show
```

Confirm that:

- Git prints version information.
- Python reports version `3.12` or newer.
- Azure CLI prints version information.
- `az account show` displays the Azure account/subscription supplied for training.
- The GitHub Copilot icon is visible in VS Code and shows your Copilot access.
- The Python and Azure MCP Server extensions are installed and enabled.

## If something fails

Do not wait until the training starts. Record the error message, your operating system, and the first command that failed.
Contact your local IT administrator for help with errors or access-related questions.