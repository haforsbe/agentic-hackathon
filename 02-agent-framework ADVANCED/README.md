# Get Started with Agent Framework for Python (v1.13.0)

This folder contains a progressive set of samples that introduce the core
concepts of **Agent Framework** one step at a time.

## Prerequisites

```bash
pip install -r ../requirements.txt
```

These samples use `AzureCliCredential` exclusively. Sign in with Azure CLI (no API keys or fallback credential types):

```bash
az login
az account show
```

Set the required environment variables:

These samples require a **Microsoft Foundry V2 project** with a deployed chat model. Foundry V1 projects are not supported.

In the Foundry portal, open your V2 project and copy `AZURE_AI_PROJECT_ENDPOINT` from the project overview. Find `AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME` under **Models + endpoints**; use the deployment name, not the base model name.

```bash
export AZURE_AI_PROJECT_ENDPOINT="https://your-project-endpoint"
export AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME="gpt-4o"
export AZURE_CLI_PROCESS_TIMEOUT="60"   # optional
```

Notes:
- The samples use `OpenAIChatCompletionClient` with the Foundry project OpenAI route and authenticate only through the active Azure CLI session.
- `AZURE_CLI_PROCESS_TIMEOUT` is optional and defaults to `60` seconds.

## What These Scripts Do

These scripts are a progressive learning path for Agent Framework on Azure:
- Start with a minimal agent and basic runs (non-streaming + streaming).
- Add local tools/functions and let the model invoke them.
- Maintain conversation context across turns and sessions.
- Inject dynamic runtime context using custom context providers.
- Build an executor-based workflow with explicit graph edges.
- Connect an agent to a remote MCP server so it can call external tools.

## Samples

| # | File | What you'll learn |
|---|------|-------------------|
| 1 | [01_hello_agent.py](01_hello_agent.py) | Create your first agent and run it (streaming and non-streaming). |
| 2 | [02_add_tools.py](02_add_tools.py) | Define a function tool with `@tool` and attach it to an agent. |
| 3 | [03_multi_turn.py](03_multi_turn.py) | Keep conversation history across turns with `Agent` sessions. |
| 4 | [04_memory.py](04_memory.py) | Add dynamic context with a custom `ContextProvider`. |
| 5 | [05_first_workflow.py](05_first_workflow.py) | Chain executors into a workflow with edges. |
| 6 | [06_remote_mcp.py](06_remote_mcp.py) | Connect an agent to a remote MCP server for live tool use. |

## What's New in 1.13.0

- Improved Agent API with better type safety
- Enhanced workflow and executor patterns
- Better integration with Azure services
- Streamlined context provider interface
- More consistent error handling

Run any sample with:

```bash
python 01_hello_agent.py
```

These samples use Azure AI Foundry models through the Chat Completions API so Agent Framework can invoke local and MCP tools.
