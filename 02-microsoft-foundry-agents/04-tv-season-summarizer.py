import json
import os
import re
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

load_dotenv(override=True)

DATA_FILE = Path(__file__).with_name("tv_season_data.json")


def _resolve_project_endpoint() -> str:
    return os.environ.get("AZURE_AI_PROJECT_ENDPOINT") or os.environ["PROJECT_ENDPOINT"]


def _resolve_model_deployment() -> str:
    return os.environ.get("AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME") or os.environ["MODEL_DEPLOYMENT_NAME"]


def _resolve_agent_name() -> str:
    return (
        os.environ.get("TV_SUMMARIZER_AGENT_NAME")
        or os.environ.get("AGENT_NAME")
        or "TvSeasonSummarizer"
    )


def _load_series_data() -> dict[str, Any]:
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def _build_season_index(data: dict[str, Any]) -> dict[tuple[str, int], dict[str, Any]]:
    index: dict[tuple[str, int], dict[str, Any]] = {}
    for series in data.get("series", []):
        title = str(series.get("title", "")).strip()
        if not title:
            continue

        for season in series.get("seasons", []):
            season_num = season.get("season_number")
            if isinstance(season_num, int):
                index[(title.lower(), season_num)] = season
    return index


def _parse_request(user_text: str) -> tuple[str | None, int | None]:
    # Supports: "Show | 2", "Show, 2", and natural text with "season <n>"
    if "|" in user_text:
        left, right = user_text.split("|", 1)
        season_text = right.strip()
        return left.strip() or None, int(season_text) if season_text.isdigit() else None

    if "," in user_text:
        left, right = user_text.rsplit(",", 1)
        season_text = right.strip()
        return left.strip() or None, int(season_text) if season_text.isdigit() else None

    match = re.search(r"season\s+(\d+)", user_text, flags=re.IGNORECASE)
    if not match:
        return None, None

    season_num = int(match.group(1))
    series_name = re.sub(r"season\s+\d+", "", user_text, flags=re.IGNORECASE).strip(" :,-")
    if not series_name:
        return None, None

    return series_name, season_num


def _list_available_series(data: dict[str, Any]) -> list[str]:
    return [str(s.get("title", "")).strip() for s in data.get("series", []) if s.get("title")]


def _create_or_update_agent(project_client: AIProjectClient) -> str:
    agent_name = _resolve_agent_name()
    deployment_name = _resolve_model_deployment()

    instructions = (
        "You are a TV season recap specialist. Use only the provided season context. "
        "Return a high-level summary with: (1) season overview, (2) major turning points, "
        "(3) ending status, (4) where-next hook. "
        "Do not invent details that are not in context. If context is missing, say so clearly."
    )

    agent = project_client.agents.create_version(
        agent_name=agent_name,
        definition=PromptAgentDefinition(
            model=deployment_name,
            instructions=instructions,
        ),
    )
    print(f"Using agent (id: {agent.id}, name: {agent.name}, version: {agent.version})")
    return agent.name


def _build_prompt(series_name: str, season_num: int, season_data: dict[str, Any]) -> str:
    return (
        f"Series: {series_name}\n"
        f"Season: {season_num}\n"
        f"Context JSON:\n{json.dumps(season_data, indent=2)}\n\n"
        "Create a concise high-level recap.\n"
        "Format:\n"
        "- Overview: ...\n"
        "- Turning Points: ...\n"
        "- Ending Status: ...\n"
        "- Where Next: ..."
    )


def main() -> None:
    data = _load_series_data()
    season_index = _build_season_index(data)
    available_series = _list_available_series(data)

    if not season_index:
        raise ValueError("No season data found in tv_season_data.json")

    project_client = AIProjectClient(
        endpoint=_resolve_project_endpoint(),
        credential=DefaultAzureCredential(),
    )

    agent_name = _create_or_update_agent(project_client)
    openai_client = project_client.get_openai_client()

    conversation = openai_client.conversations.create()
    print(f"Created conversation (id: {conversation.id})")
    print("\nEnter requests as 'Series | SeasonNumber' (example: Breaking Bad | 1)")
    print("You can also type natural text like 'Summarize The Office season 2'.")
    print("Type 'q' to quit.\n")

    while True:
        user_text = input("Request> ").strip()
        if user_text.lower() in {"q", "quit", "exit"}:
            print("Exiting TV season summarizer.")
            break

        series_name, season_num = _parse_request(user_text)
        if not series_name or season_num is None:
            print("Could not parse request. Use 'Series | SeasonNumber' or include 'season <number>'.")
            continue

        key = (series_name.lower(), season_num)
        season_data = season_index.get(key)
        if season_data is None:
            print(f"No local data for '{series_name}' season {season_num}.")
            print(f"Available series: {', '.join(available_series)}")
            continue

        prompt = _build_prompt(series_name, season_num, season_data)
        response = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent": {"name": agent_name, "type": "agent_reference"}},
            input=prompt,
        )

        print("\nSummary")
        print("-" * 60)
        print(response.output_text)
        print("-" * 60 + "\n")


if __name__ == "__main__":
    main()
