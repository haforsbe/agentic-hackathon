import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv(override=True)


def _resolve_project_endpoint() -> str:
    return os.environ.get("AZURE_AI_PROJECT_ENDPOINT") or os.environ["PROJECT_ENDPOINT"]


def _resolve_agent_name() -> str:
    return os.environ["AGENT_NAME"]

project_client = AIProjectClient(
    endpoint=_resolve_project_endpoint(),
    credential=DefaultAzureCredential(),
)

agent_name = _resolve_agent_name()
openai_client = project_client.get_openai_client()

# Optional Step: Create a conversation to use with the agent
conversation = openai_client.conversations.create()
print(f"Created conversation (id: {conversation.id})")

# Chat with the agent to answer questions
message = "What is the size of France in square miles?"
print(f"\nUser: {message}")
response = openai_client.responses.create(
    conversation=conversation.id, #Optional conversation context for multi-turn
    extra_body={"agent": {"name": agent_name, "type": "agent_reference"}},
    input=message,
)
print(f"\nAgent: {response.output_text}")

# Optional Step: Ask a follow-up question in the same conversation
message = "And what is the capital city?"
print(f"\nUser: {message}")
response = openai_client.responses.create(
    conversation=conversation.id,
    extra_body={"agent": {"name": agent_name, "type": "agent_reference"}},
    input=message,
)
print(f"\nAgent: {response.output_text}")
