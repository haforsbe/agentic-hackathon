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
Multi-Turn Conversations — Use AgentSession to maintain context with Agent Framework 1.13.0

This sample shows how to keep conversation history across multiple calls
by reusing the same session object.

Environment variables:
    AZURE_AI_PROJECT_ENDPOINT        — Your Azure AI project endpoint
  AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME — Model deployment name (e.g. gpt-4o)
    AZURE_CLI_PROCESS_TIMEOUT        — Optional Azure CLI token timeout in seconds (default: 60)
"""


def _resolve_project_endpoint() -> str:
    project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    if project_endpoint:
        return project_endpoint
    raise ValueError("Missing project endpoint configuration. Set AZURE_AI_PROJECT_ENDPOINT in .env.")


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
        name="ConversationAgent",
        instructions="You are a friendly assistant. Keep your answers brief.",
    )
    # </create_agent>

    # <multi_turn>
    # Create a session to maintain conversation history
    session = agent.create_session()

    # First turn
    message = "My name is Alice and I love hiking."
    print(f"User: {message}\n")
    result = await agent.run(message, session=session)
    print(f"Agent: {result}\n")

    # Second turn — the agent should remember the user's name and hobby
    message = "What do you remember about me?"
    print(f"User: {message}\n")
    result = await agent.run(message, session=session)
    print(f"Agent: {result}")
    # </multi_turn>


if __name__ == "__main__":
    asyncio.run(main())
