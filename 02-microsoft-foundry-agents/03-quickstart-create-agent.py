import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

load_dotenv(override=True)


def _resolve_project_endpoint() -> str:
    return os.environ.get("AZURE_AI_PROJECT_ENDPOINT") or os.environ["PROJECT_ENDPOINT"]


def _resolve_model_deployment() -> str:
    return os.environ.get("AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME") or os.environ["MODEL_DEPLOYMENT_NAME"]


def _resolve_agent_name() -> str:
    return os.environ["AGENT_NAME"]

project_client = AIProjectClient(
    endpoint=_resolve_project_endpoint(),
    credential=DefaultAzureCredential(),
)

agent = project_client.agents.create_version(
    agent_name=_resolve_agent_name(),
    definition=PromptAgentDefinition(
        model=_resolve_model_deployment(),
        instructions="You are a helpful assistant that answers general questions",
    ),
)
print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")