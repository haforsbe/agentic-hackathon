# Get Started with Agent Framework for Python

This folder contains a progressive set of samples that introduce the core
concepts of **Agent Framework** one step at a time.

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
export AZURE_CLI_PROCESS_TIMEOUT="60"   # optional
```

Notes:
- `PROJECT_ENDPOINT` is supported as a compatibility alias for `AZURE_AI_PROJECT_ENDPOINT`.
- Samples in this folder are configured for Entra auth + project endpoint.

## What These Scripts Do

These scripts are a progressive learning path for Agent Framework on Azure:
- Start with a minimal agent and basic runs (non-streaming + streaming).
- Add local tools/functions and let the model invoke them.
- Maintain conversation context across turns and sessions.
- Inject dynamic runtime context using custom context providers.
- Build an executor-based workflow with explicit graph edges.
- Host an agent behind Azure Functions for API-style invocation.

## Samples

| # | File | What you'll learn |
|---|------|-------------------|
| 1 | [01_hello_agent.py](01_hello_agent.py) | Create your first agent and run it (streaming and non-streaming). |
| 2 | [02_add_tools.py](02_add_tools.py) | Define a function tool with `@tool` and attach it to an agent. |
| 3 | [03_multi_turn.py](03_multi_turn.py) | Keep conversation history across turns with `Agent` sessions. |
| 4 | [04_memory.py](04_memory.py) | Add dynamic context with a custom `BaseContextProvider`. |
| 5 | [05_first_workflow.py](05_first_workflow.py) | Chain executors into a workflow with edges. |
| 6 | [06_host_your_agent.py](06_host_your_agent.py) | Host a single agent with Azure Functions. |

Run any sample with:

```bash
python 01_hello_agent.py
```

These samples use Azure AI Foundry models with the Responses API.
