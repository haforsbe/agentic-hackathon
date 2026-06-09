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
- Build a domain-specific TV season summarizer that uses local mock data.

## Quickstarts

| # | File | What you'll learn |
| --- | --- | --- |
| 1 | [01-quickstart-responses.py](01-quickstart-responses.py) | Call the Responses API through an Azure AI Foundry project client. |
| 2 | [02-quickstart-create-agent.py](02-quickstart-create-agent.py) | Create a new prompt agent version in your Foundry project. |
| 3 | [03-quickstart-chat-with-agent.py](03-quickstart-chat-with-agent.py) | Chat with an existing Foundry agent reference in a conversation. |
| 4 | [04-tv-season-summarizer.py](04-tv-season-summarizer.py) | Create or update a TV summarizer agent and generate high-level season recaps from local data. |

## TV Season Summarizer Sample

The TV season summarizer sample uses a local dataset in [tv_season_data.json](tv_season_data.json) so you can test cross-series summaries without external TV APIs.

Run it with:

```bash
python 04-tv-season-summarizer.py
```

Optional environment variable (if you want a dedicated agent name):

```bash
export TV_SUMMARIZER_AGENT_NAME="TvSeasonSummarizer"
```

Prompt examples:

- `Breaking Bad | 1`
- `The Office | 2`
- `Summarize Stranger Things season 1`
- `Summarize Breaking Bad season 2`
- `Stranger Things, 2`

Run any sample with:

```bash
python 01-quickstart-responses.py
```

You can substitute `01-quickstart-responses.py` with any of the other quickstart filenames.
