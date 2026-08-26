"""Create a Microsoft guidance prompt-agent from tested instructions."""

import os
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
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
instructions = (SCENARIO_DIR / "agent-instructions.md").read_text(encoding="utf-8")

agent = project_client.agents.create_version(
    agent_name=os.environ["AGENT_NAME"],
    definition=PromptAgentDefinition(
        model=os.environ["AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME"],
        instructions=instructions,
    ),
)
print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")