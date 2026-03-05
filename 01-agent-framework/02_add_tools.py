# Copyright (c) Microsoft. All rights reserved.

import asyncio
import os
from random import randint
from typing import Annotated

from agent_framework import Agent, tool
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
from pydantic import Field

# Load environment variables from .env file
load_dotenv(override=True)

"""
Add Tools — Give your agent a function tool

This sample shows how to define a function tool with the @tool decorator
and wire it into an agent so the model can call it.

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

    raise ValueError(
        "Missing project endpoint configuration. Set AZURE_AI_PROJECT_ENDPOINT "
        "or PROJECT_ENDPOINT in .env."
    )


# <define_tool>
# NOTE: approval_mode="never_require" is for sample brevity.
# Use "always_require" in production for user confirmation before tool execution.
@tool(approval_mode="never_require")
def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."
# </define_tool>


async def main() -> None:
    cli_timeout = int(os.getenv("AZURE_CLI_PROCESS_TIMEOUT", "60"))
    credential = AzureCliCredential(process_timeout=cli_timeout)
    client = AzureOpenAIResponsesClient(
        project_endpoint=_resolve_project_endpoint(),
        deployment_name=os.environ["AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME"],
        credential=credential,
    )

    # <create_agent_with_tools>
    agent = Agent(
        client=client,
        name="WeatherAgent",
        instructions="You are a helpful weather agent. Use the get_weather tool to answer questions.",
        tools=get_weather,
    )
    # </create_agent_with_tools>

    # <run_agent>
    result = await agent.run("What's the weather like in Seattle?")
    print(f"Agent: {result}")
    # </run_agent>


if __name__ == "__main__":
    asyncio.run(main())
