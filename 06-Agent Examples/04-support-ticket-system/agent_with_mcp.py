# Copyright (c) Microsoft. All rights reserved.

import asyncio
import os

from agent_framework import Agent, MCPStreamableHTTPTool
from agent_framework.openai import OpenAIChatCompletionClient
from azure.identity import AzureCliCredential, get_bearer_token_provider
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

"""
IT Support Agent with MCP — Connect an agent to the local ticketing MCP server

This script creates an AI agent that manages IT support tickets via the
ticketing MCP server (mcp_server.py). Start the MCP server in HTTP mode
first, then run this script for a multi-turn conversation.

    Terminal 1:  python mcp_server.py --http
    Terminal 2:  python agent_with_mcp.py

Environment variables:
        AZURE_AI_PROJECT_ENDPOINT        — Your Azure AI project endpoint
  AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME — Model deployment name (e.g. gpt-4o)
        AZURE_CLI_PROCESS_TIMEOUT        — Optional Azure CLI token timeout in seconds (default: 60)
"""

MCP_SERVER_URL = "http://localhost:8000/mcp"


def _resolve_project_endpoint() -> str:
    project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    if project_endpoint:
        return project_endpoint

    raise ValueError(
        "Missing project endpoint configuration. Set AZURE_AI_PROJECT_ENDPOINT in .env."
    )


async def main() -> None:
    cli_timeout = int(os.getenv("AZURE_CLI_PROCESS_TIMEOUT", "60"))
    credential = AzureCliCredential(process_timeout=cli_timeout)
    token_provider = get_bearer_token_provider(credential, "https://ai.azure.com/.default")
    client = OpenAIChatCompletionClient(
        model=os.environ["AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME"],
        base_url=f"{_resolve_project_endpoint().rstrip('/')}/openai/v1/",
        api_key=lambda: asyncio.to_thread(token_provider),
    )

    # Connect to the local ticketing MCP server
    async with (
        MCPStreamableHTTPTool(
            name="IT Support Ticketing",
            url=MCP_SERVER_URL,
        ) as mcp_server,
    ):
        agent = Agent(
            client=client,
            name="IT Support Agent",
            instructions=(
                "You are an IT support assistant that manages support tickets. "
                "Use the ticketing tools to list, create, update, and close tickets. "
                "When listing tickets, format them in a readable way. "
                "Always confirm actions you take on tickets."
            ),
            tools=[mcp_server],
        )

        # Multi-turn conversation loop
        session = agent.create_session()
        print("IT Support Agent ready. Type 'quit' to exit.\n")

        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "q"):
                print("Goodbye!")
                break

            print(f"\n{agent.name}: ", end="", flush=True)
            async for chunk in agent.run(user_input, session=session, stream=True):
                if chunk.text:
                    print(chunk.text, end="", flush=True)
            print("\n")


if __name__ == "__main__":
    asyncio.run(main())
