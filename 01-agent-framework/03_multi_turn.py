# Copyright (c) Microsoft. All rights reserved.

import asyncio
import os

from agent_framework import Agent
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

"""
Multi-Turn Conversations — Use AgentSession to maintain context

This sample shows how to keep conversation history across multiple calls
by reusing the same session object.

Environment variables:
    AZURE_AI_PROJECT_ENDPOINT        — Your Azure AI project endpoint
    PROJECT_ENDPOINT                 — Compatibility alias for project endpoint
  AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME — Model deployment name (e.g. gpt-4o)
    AZURE_CLI_PROCESS_TIMEOUT        — Optional Azure CLI token timeout in seconds (default: 60)
"""


def _resolve_project_endpoint() -> str:
    project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT") or os.getenv("PROJECT_ENDPOINT")
    if project_endpoint:
        return project_endpoint
    raise ValueError("Missing project endpoint configuration. Set AZURE_AI_PROJECT_ENDPOINT or PROJECT_ENDPOINT.")


async def main() -> None:
    # <create_agent>
    cli_timeout = int(os.getenv("AZURE_CLI_PROCESS_TIMEOUT", "60"))
    credential = AzureCliCredential(process_timeout=cli_timeout)
    client = AzureOpenAIResponsesClient(
        project_endpoint=_resolve_project_endpoint(),
        deployment_name=os.environ["AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME"],
        credential=credential,
    )

    agent = Agent(
        client=client,
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
