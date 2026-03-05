# Microsoft Foundry Agents Quickstarts

This folder contains top-level quickstarts for working with Azure AI Foundry project agents and Responses.

## Prerequisites

```bash
pip install -r ../requirements.txt
```

Use **Entra ID authentication** (no API keys):

```bash
az login
```

Set the required environment variables:

```bash
export AZURE_AI_PROJECT_ENDPOINT="https://your-project-endpoint"
export AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME="gpt-4o"
export AGENT_NAME="MyAgent"
```

Notes:
- `PROJECT_ENDPOINT` is supported as a compatibility alias for `AZURE_AI_PROJECT_ENDPOINT`.
- `MODEL_DEPLOYMENT_NAME` is supported as a compatibility alias for `AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME`.
- These top-level quickstarts use `load_dotenv(override=True)` so values in `.env` take precedence over shell variables.

## What These Scripts Do

These quickstarts show the core Azure AI Foundry agent workflow:
- Connect to a Foundry project and call the Responses API directly.
- Chat with an existing agent reference over a multi-turn conversation.
- Create a new prompt-based agent version in your Foundry project.

## Quickstarts

| # | File | What you'll learn |
|---|------|-------------------|
| 1 | [01-quickstart-responses.py](01-quickstart-responses.py) | Call the Responses API through an Azure AI Foundry project client. |
| 2 | [02-quickstart-chat-with-agent.py](02-quickstart-chat-with-agent.py) | Chat with an existing Foundry agent reference in a conversation. |
| 3 | [03-quickstart-create-agent.py](03-quickstart-create-agent.py) | Create a new prompt agent version in your Foundry project. |

Run any sample with:

```bash
python 01-quickstart-responses.py
```

You can substitute `01-quickstart-responses.py` with any of the other quickstart filenames.
