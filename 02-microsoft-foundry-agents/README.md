# Microsoft Foundry Agents Quickstarts

This folder contains top-level quickstarts for working with Azure AI Foundry project agents and Responses.

Built against the **Microsoft Foundry SDK** (`azure-ai-projects` 2.4.0).

## Prerequisites

```bash
pip install -r ../requirements.txt
```

These quickstarts use `AzureCliCredential` exclusively. Sign in with Azure CLI (no API keys, browser broker, environment credential, or managed identity fallback):

```bash
az login
az account show
```

If you have multiple subscriptions, select the subscription that contains your Foundry project:

```bash
az account set --subscription "<subscription-name-or-id>"
```

Set the required environment variables:

These quickstarts require a **Microsoft Foundry V2 project** with a deployed chat model. Foundry V1 projects are not supported.

In the Foundry portal, open your V2 project and copy `AZURE_AI_PROJECT_ENDPOINT` from the project overview. Find `AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME` under **Models + endpoints**; use the deployment name, not the base model name. Choose `AGENT_NAME` yourself.

```bash
export AZURE_AI_PROJECT_ENDPOINT="https://your-project-endpoint"
export AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME="gpt-4o"
export AGENT_NAME="MyAgent"
```

Notes:
- These top-level quickstarts use `load_dotenv(override=True)` so values in `.env` take precedence over shell variables.
- Run `02-quickstart-create-agent.py` before `03-quickstart-chat-with-agent.py`, since the chat sample resolves an existing agent by `AGENT_NAME`.
- Foundry owns agent version numbers. Re-running an unchanged definition can return the existing version; creating a changed definition produces a new immutable version.

## What These Scripts Do

These quickstarts show the core Azure AI Foundry agent workflow:
- Connect to a Foundry project and call the Responses API directly.
- Chat with an existing agent reference over a multi-turn conversation.
- Create a new prompt-based agent version in your Foundry project.

## Quickstarts

| # | File | What you'll learn |
|---|------|-------------------|
| 1 | [01-quickstart-responses.py](01-quickstart-responses.py) | Call the Responses API through an Azure AI Foundry project client. |
| 2 | [02-quickstart-create-agent.py](02-quickstart-create-agent.py) | Create a new prompt agent version in your Foundry project. |
| 3 | [03-quickstart-chat-with-agent.py](03-quickstart-chat-with-agent.py) | Chat with an existing Foundry agent reference in a conversation. |

Run any sample with:

```bash
python 01-quickstart-responses.py
```

You can substitute `01-quickstart-responses.py` with any of the other quickstart filenames.
