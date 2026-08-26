"""Test the Microsoft guidance instructions without documentation tools."""

import argparse
import os
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv


SCENARIO_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCENARIO_DIR.parents[1]
TEST_PROMPTS = {
    "no-tool": (
        "Give me the current documented steps and official links for configuring managed "
        "identity in Azure Container Apps. State whether you searched Microsoft Learn."
    ),
    "method": (
        "Explain how you would compare Azure Container Apps and Azure App Service after "
        "Microsoft Learn tools are connected. Include how you would verify current claims."
    ),
    "code": (
        "Provide the latest official Python SDK code for a Microsoft service and cite the "
        "sample you retrieved. I have not specified the service."
    ),
}


def run_test(test_name: str) -> str:
    load_dotenv(WORKSPACE_ROOT / ".env")
    instructions = (SCENARIO_DIR / "agent-instructions.md").read_text(encoding="utf-8")
    project_client = AIProjectClient(
        endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        credential=AzureCliCredential(
            process_timeout=int(os.getenv("AZURE_CLI_PROCESS_TIMEOUT", "60"))
        ),
    )
    response = project_client.get_openai_client().responses.create(
        model=os.environ["AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME"],
        instructions=instructions,
        input=TEST_PROMPTS[test_name],
    )
    if not response.output_text.strip():
        raise RuntimeError("The model returned no visible output. Rerun this test.")
    return response.output_text


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--test", choices=[*TEST_PROMPTS, "all"], default="all")
    args = parser.parse_args()
    selected = TEST_PROMPTS if args.test == "all" else {args.test: TEST_PROMPTS[args.test]}

    for test_name in selected:
        print(f"\n=== {test_name.upper()} ===")
        print(run_test(test_name))


if __name__ == "__main__":
    main()