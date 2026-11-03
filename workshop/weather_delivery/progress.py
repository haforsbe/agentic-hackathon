"""Pure state transitions for the optional lab after checkpoint 07."""

from copy import deepcopy


OPTIONAL_LAB = "weather_delivery"
STAGES = {"capture", "review", "validate", "release"}


def route_after_weather_release(progress):
    checkpoint = next(
        (item for item in progress.get("checkpoints", []) if item.get("id") == "07"),
        None,
    )
    if not checkpoint or checkpoint.get("status") != "passed":
        return "07"
    lab = progress.get("optional_labs", {}).get(OPTIONAL_LAB)
    if lab and lab.get("status") == "in_progress":
        return "weather-delivery"
    if lab and lab.get("status") == "blocked":
        return "weather-delivery-blocked"
    if lab and lab.get("status") in {"skipped", "completed"}:
        return "08"
    if progress.get("current_checkpoint") != "07":
        return progress.get("current_checkpoint") or "08"
    return "offer-weather-delivery"


def choose_weather_delivery(progress, choice):
    """Record an explicit start or skip without changing numbered checkpoints."""
    if route_after_weather_release(progress) != "offer-weather-delivery":
        raise ValueError("The optional lab is offered only after checkpoint 07 passes")
    if choice not in {"start", "skip"}:
        raise ValueError("Choose start or skip")
    result = deepcopy(progress)
    result.setdefault("optional_labs", {})[OPTIONAL_LAB] = {
        "status": "in_progress" if choice == "start" else "skipped",
        "current_stage": "capture" if choice == "start" else None,
        "attempts": [],
    }
    if choice == "skip":
        result["current_checkpoint"] = "08"
    return result


def skip_blocked_weather_delivery(progress):
    """Keep the failed attempt, but let the participant explicitly return to 08."""
    if route_after_weather_release(progress) != "weather-delivery-blocked":
        raise ValueError("Only a blocked Weather delivery lab can be explicitly skipped")
    updated = deepcopy(progress)
    lab = updated["optional_labs"][OPTIONAL_LAB]
    lab.update(status="skipped", current_stage=None)
    updated["current_checkpoint"] = "08"
    return updated


def advance_weather_delivery(progress, stage, result):
    """Persist a stage boundary; completion returns the learner to checkpoint 08."""
    if route_after_weather_release(progress) != "weather-delivery":
        raise ValueError("The Weather delivery lab is not in progress")
    if stage not in STAGES or result not in {"passed", "failed", "blocked", "paused"}:
        raise ValueError("Unknown optional-lab stage or result")
    updated = deepcopy(progress)
    lab = updated["optional_labs"][OPTIONAL_LAB]
    if stage != lab["current_stage"]:
        raise ValueError("Record evidence only for the current optional-lab stage")
    lab["attempts"].append({"stage": stage, "result": result})
    if result == "passed" and stage == "release":
        lab.update(status="completed", current_stage=None)
        updated["current_checkpoint"] = "08"
    elif result == "blocked":
        lab.update(status="blocked", current_stage=stage)
    elif result == "paused":
        lab.update(status="in_progress", current_stage=stage)
    elif result == "failed":
        lab.update(status="in_progress", current_stage=stage)
    else:
        next_stage = {
            "capture": "review",
            "review": "validate",
            "validate": "release",
        }.get(stage)
        if next_stage is None:
            raise ValueError("Only a passed release completes the optional lab")
        lab.update(status="in_progress", current_stage=next_stage)
    return updated
