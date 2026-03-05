import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv(override=True)


def _resolve_project_endpoint() -> str:
    return os.environ.get("AZURE_AI_PROJECT_ENDPOINT") or os.environ["PROJECT_ENDPOINT"]


def _resolve_model_deployment() -> str:
    return os.environ.get("AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME") or os.environ["MODEL_DEPLOYMENT_NAME"]

print(f"Using PROJECT_ENDPOINT: {_resolve_project_endpoint()}")
print(f"Using MODEL_DEPLOYMENT_NAME: {_resolve_model_deployment()}")

project_client = AIProjectClient(
    endpoint=_resolve_project_endpoint(),
    credential=DefaultAzureCredential(),
)

openai_client = project_client.get_openai_client()

response = openai_client.responses.create(
    model=_resolve_model_deployment(),
    input="What is the size of France in square miles?",
)
print(f"Response output: {response.output_text}")