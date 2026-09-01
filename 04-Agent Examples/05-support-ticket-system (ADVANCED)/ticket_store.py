"""Shared local storage for the ticketing web app and MCP server."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any

VALID_PRIORITIES = {"Low", "Medium", "High", "Critical"}
VALID_STATUSES = {"Open", "In Progress", "Resolved", "Closed"}

_DATA_FILE = Path(__file__).with_name("tickets.json")
_LOCK = Lock()
_SAMPLE_TICKETS = [
    {
        "title": "Email server not responding",
        "description": "Multiple users report they cannot send or receive emails since 9 AM. Exchange server appears to be down.",
        "priority": "Critical",
        "status": "Open",
        "assignee": "Alice Johnson",
    },
    {
        "title": "VPN connection drops frequently",
        "description": "Remote employees are experiencing intermittent VPN disconnections throughout the day, especially during video calls.",
        "priority": "High",
        "status": "In Progress",
        "assignee": "Bob Smith",
    },
    {
        "title": "New laptop setup for onboarding",
        "description": "Set up a new Dell laptop for the incoming marketing hire starting next Monday. Install standard software suite.",
        "priority": "Medium",
        "status": "Open",
        "assignee": "Carol Davis",
    },
    {
        "title": "Printer on 3rd floor is jamming",
        "description": "The HP LaserJet on the 3rd floor keeps jamming when printing double-sided documents.",
        "priority": "Low",
        "status": "Open",
        "assignee": "Dan Wilson",
    },
    {
        "title": "Password reset request",
        "description": "User locked out of Active Directory account after too many failed login attempts. Needs password reset.",
        "priority": "Medium",
        "status": "Resolved",
        "assignee": "Eve Martinez",
    },
    {
        "title": "Software license expired - Adobe Creative Suite",
        "description": "The design team cannot use Photoshop or Illustrator. License renewal needed ASAP.",
        "priority": "High",
        "status": "In Progress",
        "assignee": "Alice Johnson",
    },
    {
        "title": "Conference room display not working",
        "description": "The HDMI connection in Conference Room B does not display laptop screens. Adapter and cables tested.",
        "priority": "Low",
        "status": "Closed",
        "assignee": "Bob Smith",
    },
]


def _seed() -> list[dict[str, Any]]:
    created_at = datetime.now(timezone.utc).isoformat()
    return [
        {"id": index, **ticket, "createdAt": created_at}
        for index, ticket in enumerate(_SAMPLE_TICKETS, start=1)
    ]


def _load() -> list[dict[str, Any]]:
    if not _DATA_FILE.exists():
        tickets = _seed()
        _save(tickets)
        return tickets
    with _DATA_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def _save(tickets: list[dict[str, Any]]) -> None:
    temporary_file = _DATA_FILE.with_suffix(".tmp")
    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=2)
    os.replace(temporary_file, _DATA_FILE)


def list_tickets(status: str | None = None, priority: str | None = None) -> list[dict[str, Any]]:
    with _LOCK:
        tickets = _load()
    return [
        ticket
        for ticket in tickets
        if (not status or ticket["status"] == status)
        and (not priority or ticket["priority"] == priority)
    ]


def get_ticket(ticket_id: int) -> dict[str, Any] | None:
    return next((ticket for ticket in list_tickets() if ticket["id"] == ticket_id), None)


def create_ticket(title: str, description: str, priority: str, assignee: str = "") -> dict[str, Any]:
    if priority not in VALID_PRIORITIES:
        raise ValueError(f"priority must be one of {sorted(VALID_PRIORITIES)}")
    if not title.strip() or not description.strip():
        raise ValueError("title and description are required")

    with _LOCK:
        tickets = _load()
        ticket = {
            "id": max((entry["id"] for entry in tickets), default=0) + 1,
            "title": title.strip(),
            "description": description.strip(),
            "priority": priority,
            "status": "Open",
            "assignee": assignee.strip(),
            "createdAt": datetime.now(timezone.utc).isoformat(),
        }
        tickets.append(ticket)
        _save(tickets)
        return ticket


def update_ticket(
    ticket_id: int,
    status: str | None = None,
    assignee: str | None = None,
    title: str | None = None,
    description: str | None = None,
    priority: str | None = None,
) -> dict[str, Any] | None:
    if status is not None and status not in VALID_STATUSES:
        raise ValueError(f"status must be one of {sorted(VALID_STATUSES)}")
    if priority is not None and priority not in VALID_PRIORITIES:
        raise ValueError(f"priority must be one of {sorted(VALID_PRIORITIES)}")
    if title is not None and not title.strip():
        raise ValueError("title is required")
    if description is not None and not description.strip():
        raise ValueError("description is required")

    with _LOCK:
        tickets = _load()
        ticket = next((entry for entry in tickets if entry["id"] == ticket_id), None)
        if ticket is None:
            return None
        if status is not None:
            ticket["status"] = status
        if assignee is not None:
            ticket["assignee"] = assignee.strip()
        if title is not None:
            ticket["title"] = title.strip()
        if description is not None:
            ticket["description"] = description.strip()
        if priority is not None:
            ticket["priority"] = priority
        _save(tickets)
        return ticket


def close_ticket(ticket_id: int) -> dict[str, Any] | None:
    return update_ticket(ticket_id, status="Closed")