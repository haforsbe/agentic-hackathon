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
Remote MCP Tools — Connect an agent to a remote MCP server with Agent Framework 1.13.0

This sample demonstrates how to connect an agent to a remote MCP (Model Context Protocol) server.
MCP servers expose tools that agents can use to access external data and services.
In this example, the agent connects to Microsoft Learn's MCP server to answer documentation questions.

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
    cli_timeout = int(os.getenv("AZURE_CLI_PROCESS_TIMEOUT", "60"))
    credential = AzureCliCredential(process_timeout=cli_timeout)

    token_provider = get_bearer_token_provider(credential, "https://ai.azure.com/.default")
    chat_client = OpenAIChatCompletionClient(
        model=os.environ["AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME"],
        base_url=f"{_resolve_project_endpoint().rstrip('/')}/openai/v1/",
        api_key=lambda: asyncio.to_thread(token_provider),
    )

    # <create_agent_with_mcp>
    # Connect to a remote MCP server and use it as a tool
    async with (
        MCPStreamableHTTPTool(
            name="Microsoft Learn MCP",
            url="https://learn.microsoft.com/api/mcp",
        ) as mcp_server,
    ):
        agent = Agent(
            client=chat_client,
            name="DocsAgent",
            instructions="You are a helpful assistant that answers questions using Microsoft documentation.",
            tools=[mcp_server],
        )

        # <run_agent>
        query = "How can I use Playwright for AI-enabled software testing?"
        print(f"User: {query}\n")
        print(f"{agent.name}: ", end="", flush=True)
        async for chunk in agent.run(query, stream=True):
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print("\n")
        # </run_agent>
    # </create_agent_with_mcp>


if __name__ == "__main__":
    asyncio.run(main())