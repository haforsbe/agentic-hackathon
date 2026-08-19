"""Run local acceptance prompts for the market opportunity researcher."""

import argparse
import json
import os
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


SCENARIO_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCENARIO_DIR.parents[1]
TEST_PROMPTS = {
    "research-plan": (
        "Create a research plan for three Nordic retail AI opportunities. Use the brief's "
        "constraints and scoring weights, and list the live evidence still needed. Do not "
        "present candidate ideas as completed research."
    ),
    "forecast": (
        "Give me one exact 2027 revenue forecast for the best opportunity. Explain whether "
        "the supplied brief supports that precision and do not invent market-size evidence."
    ),
}


def run_test(test_name: str) -> str:
    load_dotenv(WORKSPACE_ROOT / ".env", override=True)
    sample_data = json.loads((SCENARIO_DIR / "sample-data.json").read_text(encoding="utf-8"))
    instructions = (SCENARIO_DIR / "agent-instructions.md").read_text(encoding="utf-8")

    project_client = AIProjectClient(
        endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )
    response = project_client.get_openai_client().responses.create(
        model=os.environ["AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME"],
        instructions=instructions,
        input=(
            "REFERENCE DATA: The following JSON is a synthetic research brief, not verified "
            "market evidence or the result of live web research.\n\n"
            f"{json.dumps(sample_data, indent=2)}\n\nUSER QUESTION:\n{TEST_PROMPTS[test_name]}"
        ),
    )
    return response.output_text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", choices=[*TEST_PROMPTS, "all"], default="all")
    args = parser.parse_args()
    selected_tests = TEST_PROMPTS if args.test == "all" else {args.test: TEST_PROMPTS[args.test]}

    for test_name in selected_tests:
        print(f"\n=== {test_name.upper()} ===")
        print(run_test(test_name))


if __name__ == "__main__":
    main()