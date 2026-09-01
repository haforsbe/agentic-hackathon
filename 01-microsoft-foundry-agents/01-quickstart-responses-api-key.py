"""Quickstart: call the Responses API with an API key.

The project client uses Azure CLI authentication. The API key is passed only to the
OpenAI Responses client returned by the Microsoft Foundry SDK.
"""

import os

from azure.ai.projects import AIProjectClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv(override=True)


def _resolve_project_endpoint() -> str:
    return os.environ["AZURE_AI_PROJECT_ENDPOINT"]


def _resolve_model_deployment() -> str:
    return os.environ["AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME"]


def _resolve_api_key() -> str:
    return os.environ["AZURE_AI_API_KEY"]


print(f"Using AZURE_AI_PROJECT_ENDPOINT: {_resolve_project_endpoint()}")
print(f"Using AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME: {_resolve_model_deployment()}")

project_client = AIProjectClient(
    endpoint=_resolve_project_endpoint(),
    credential=AzureCliCredential(),
)

openai_client = project_client.get_openai_client(api_key=_resolve_api_key())

response = openai_client.responses.create(
    model=_resolve_model_deployment(),
    input="What is the size of France in square miles?",
)
print(f"Response output: {response.output_text}")