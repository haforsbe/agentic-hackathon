# Agent Framework 1.13.0 Migration Guide

## Overview
This guide documents the changes made to update the agent-framework samples from the old API to **Agent Framework 1.13.0**.

## Key Changes

### 1. **Removed: `AzureOpenAIResponsesClient`**

The `AzureOpenAIResponsesClient` class is **no longer available** in agent-framework 1.13.0.

**Old Code:**
```python
from agent_framework.azure import AzureOpenAIResponsesClient

client = AzureOpenAIResponsesClient(
    project_endpoint=_resolve_project_endpoint(),
    deployment_name=os.environ["AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME"],
    credential=credential,
)
```

### 2. **New Pattern: `OpenAIChatCompletionClient`**

Use Agent Framework's `OpenAIChatCompletionClient` when creating an `Agent`. The client implements the Agent Framework chat protocol and supports tool invocation. For a Foundry project endpoint, configure the client with the project OpenAI route and an Entra token for the `https://ai.azure.com/.default` audience.

**New Code:**
```python
import asyncio

from agent_framework.openai import OpenAIChatCompletionClient
from azure.identity import AzureCliCredential, get_bearer_token_provider

credential = AzureCliCredential(process_timeout=cli_timeout)
token_provider = get_bearer_token_provider(credential, "https://ai.azure.com/.default")

chat_client = OpenAIChatCompletionClient(
    model=os.environ["AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME"],
    base_url=f"{_resolve_project_endpoint().rstrip('/')}/openai/v1/",
    api_key=lambda: asyncio.to_thread(token_provider),
)
```

### 3. **Agent Creation Remains Unchanged**

The `Agent` class constructor remains the same - it still expects the same `client` parameter:

```python
agent = Agent(
    client=chat_client,
    name="HelloAgent",
    instructions="You are a friendly assistant. Keep your answers brief.",
)
```

## Updated Files

All six sample files have been updated with the new pattern:

| File | Status | Changes |
|------|--------|---------|
| `01_hello_agent.py` | ✅ Updated | Basic agent setup |
| `02_add_tools.py` | ✅ Updated | Agent with function tools |
| `03_multi_turn.py` | ✅ Updated | Multi-turn conversations |
| `04_memory.py` | ✅ Updated | Agent with context providers |
| `05_first_workflow.py` | ✅ Already Compatible | No changes needed |
| `06_remote_mcp.py` | ✅ Updated | Remote MCP server integration |

## Environment Configuration

Ensure your `.env` file contains:

```env
# Required
AZURE_AI_PROJECT_ENDPOINT=https://your-project.eastus.api.azureml.ms

# Optional (for compatibility)
PROJECT_ENDPOINT=https://your-project.eastus.api.azureml.ms

# Model deployment
AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME=gpt-4o

# Optional authentication timeout
AZURE_CLI_PROCESS_TIMEOUT=60
```

## How to Run the Samples

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure your Azure credentials:**
   ```bash
   az login
   ```

3. **Run a sample:**
   ```bash
   # Workflow sample (no Azure setup required)
   python 01-agent-framework/05_first_workflow.py
   
   # Agent samples (require Azure AI Foundry setup)
   python 01-agent-framework/01_hello_agent.py
   python 01-agent-framework/02_add_tools.py
   ```

## API Compatibility

- ✅ Agent Framework Core: **1.13.0**
- ✅ Agent Framework OpenAI adapter: **1.12.0**
- ✅ Azure AI Projects: **2.4.0** (used by the Foundry SDK quickstarts)
- ✅ Azure Identity: **1.25.3**

## What Stayed the Same

- `Agent` class API is unchanged
- `@tool` decorator still works the same way
- `AgentSession` for multi-turn conversations
- Context providers for dynamic instructions
- MCP server integration pattern

## Migration Checklist

If you're updating your own code:

- [ ] Replace `AzureOpenAIResponsesClient` imports with `OpenAIChatCompletionClient`
- [ ] Configure `OpenAIChatCompletionClient` with the Foundry project OpenAI route and an Entra token callback
- [ ] Keep the deployment name in the chat client `model` parameter
- [ ] Verify `.env` has `AZURE_AI_PROJECT_ENDPOINT` set
- [ ] Test agent creation and runs
- [ ] Verify imports compile with `python -m py_compile your_script.py`

## Example: Complete Migration

**Before (Old API):**
```python
from agent_framework.azure import AzureOpenAIResponsesClient

credential = AzureCliCredential()
client = AzureOpenAIResponsesClient(
    project_endpoint="https://...",
    deployment_name="gpt-4o",
    credential=credential,
)
agent = Agent(client=client, name="MyAgent", instructions="...")
```

**After (1.13.0):**
```python
import asyncio

from agent_framework.openai import OpenAIChatCompletionClient
from azure.identity import AzureCliCredential, get_bearer_token_provider

credential = AzureCliCredential()
token_provider = get_bearer_token_provider(credential, "https://ai.azure.com/.default")
chat_client = OpenAIChatCompletionClient(
    model="gpt-4o",
    base_url="https://<project-endpoint>/openai/v1/",
    api_key=lambda: asyncio.to_thread(token_provider),
)
agent = Agent(client=chat_client, name="MyAgent", instructions="...")
```

## Support

For issues or questions:
- Check the [Agent Framework documentation](https://aka.ms/agent-framework)
- Review the sample implementations in this directory
- Test with `05_first_workflow.py` first (no Azure setup required)
