# Copyright (c) Microsoft. All rights reserved.

import asyncio
import os

from agent_framework import Agent
from agent_framework.openai import OpenAIChatCompletionClient
from azure.identity import AzureCliCredential, get_bearer_token_provider
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

"""
Hello Agent — Simplest possible agent with Agent Framework 1.13.0

This sample creates a minimal agent using an Azure AI Foundry project endpoint,
and runs it in both non-streaming and streaming modes.

There are XML tags in all of the get started samples, those are used to display the same code in the docs repo.

Environment variables:
        AZURE_AI_PROJECT_ENDPOINT        — Your Azure AI project endpoint
  AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME — Model deployment name (e.g. gpt-4o)
    AZURE_CLI_PROCESS_TIMEOUT        — Optional Azure CLI token timeout in seconds (default: 60)
"""


def _resolve_project_endpoint() -> str:
    project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    if project_endpoint:
        return project_endpoint

    raise ValueError(
        "Missing project endpoint configuration. Set AZURE_AI_PROJECT_ENDPOINT in .env."
    )


async def main() -> None:
    # <create_agent>
    cli_timeout = int(os.getenv("AZURE_CLI_PROCESS_TIMEOUT", "60"))
    credential = AzureCliCredential(process_timeout=cli_timeout)

    token_provider = get_bearer_token_provider(credential, "https://ai.azure.com/.default")
    chat_client = OpenAIChatCompletionClient(
        model=os.environ["AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME"],
        base_url=f"{_resolve_project_endpoint().rstrip('/')}/openai/v1/",
        api_key=lambda: asyncio.to_thread(token_provider),
    )

    agent = Agent(
        client=chat_client,
        name="HelloAgent",
        instructions="You are a friendly assistant. Keep your answers brief.",
    )
    # </create_agent>

    # <run_agent>
    # Non-streaming: get the complete response at once
    response = await agent.run("What is the capital of France?")
    print(f"Agent: {response}")
    # </run_agent>

    # <run_agent_streaming>
    # Streaming: receive tokens as they are generated
    print("Agent (streaming): ", end="", flush=True)
    async for chunk in agent.run("Tell me a one-sentence fun fact.", stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print()
    # </run_agent_streaming>


if __name__ == "__main__":
    asyncio.run(main())
