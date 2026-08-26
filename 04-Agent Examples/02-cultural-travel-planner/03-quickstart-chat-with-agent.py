"""Chat with the cultural travel agent after its MCP tool is connected."""

import os
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv


SCENARIO_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCENARIO_DIR.parents[1]
load_dotenv(WORKSPACE_ROOT / ".env")

project_client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=AzureCliCredential(
        process_timeout=int(os.getenv("AZURE_CLI_PROCESS_TIMEOUT", "60"))
    ),
)
openai_client = project_client.get_openai_client()
conversation = openai_client.conversations.create()

message = (
    "Plan an art-focused visit to Paris on Saturday, October 10, 2026, using current "
    "museum information. I have six hours, prefer a relaxed pace, and want practical "
    "details and source links."
)
print(f"User: {message}")
response = openai_client.responses.create(
    conversation=conversation.id,
    extra_body={
        "agent_reference": {
            "name": os.environ["AGENT_NAME"],
            "type": "agent_reference",
        }
    },
    input=message,
)
if not response.output_text.strip():
    raise RuntimeError("The model returned no visible output. Rerun this test.")
print(f"\nAgent: {response.output_text}")