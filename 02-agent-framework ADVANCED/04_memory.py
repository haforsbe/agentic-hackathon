# Copyright (c) Microsoft. All rights reserved.

import asyncio
import os
from typing import Any

from agent_framework import Agent, AgentSession, ContextProvider, SessionContext
from agent_framework.openai import OpenAIChatCompletionClient
from azure.identity import AzureCliCredential, get_bearer_token_provider
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

"""
Agent Memory with Context Providers with Agent Framework 1.13.0

Context providers let you inject dynamic instructions and context into each
agent invocation. This sample defines a simple provider that tracks the user's
name and enriches every request with personalization instructions.

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


# <context_provider>
class UserNameProvider(ContextProvider):
    """A simple context provider that remembers the user's name."""

    def __init__(self) -> None:
        super().__init__(source_id="user-name-provider")
        self.user_name: str | None = None

    async def before_run(
        self,
        *,
        agent: Any,
        session: AgentSession,
        context: SessionContext,
        state: dict[str, Any],
    ) -> None:
        """Called before each agent invocation — add extra instructions."""
        if self.user_name:
            context.instructions.append(f"The user's name is {self.user_name}. Always address them by name.")
        else:
            context.instructions.append("You don't know the user's name yet. Ask for it politely.")

    async def after_run(
        self,
        *,
        agent: Any,
        session: AgentSession,
        context: SessionContext,
        state: dict[str, Any],
    ) -> None:
        """Called after each agent invocation — extract information."""
        for msg in context.input_messages:
            text = msg.text if hasattr(msg, "text") else ""
            if isinstance(text, str) and "my name is" in text.lower():
                # Simple extraction — production code should use structured extraction
                self.user_name = text.lower().split("my name is")[-1].strip().split()[0].capitalize()
# </context_provider>


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

    memory = UserNameProvider()

    agent = Agent(
        client=chat_client,
        name="MemoryAgent",
        instructions="You are a friendly assistant.",
        context_providers=[memory],
    )
    # </create_agent>

    # <run_with_memory>
    session = agent.create_session()

    # The provider doesn't know the user yet — it will ask for a name
    message = "Hello! What's the square root of 9?"
    print(f"User: {message}\n")
    result = await agent.run(message, session=session)
    print(f"Agent: {result}\n")

    # Now provide the name — the provider extracts and stores it
    message = "My name is Alice"
    print(f"User: {message}\n")
    result = await agent.run(message, session=session)
    print(f"Agent: {result}\n")

    # Subsequent calls are personalized
    message = "What is 2 + 2?"
    print(f"User: {message}\n")
    result = await agent.run(message, session=session)
    print(f"Agent: {result}\n")

    print(f"[Memory] Stored user name: {memory.user_name}")
    # </run_with_memory>


if __name__ == "__main__":
    asyncio.run(main())
