"""MCP server that exposes the IT Support Ticketing System as tools via streamable HTTP."""

from datetime import datetime, timezone
from typing import Any

from mcp.server.fastmcp import FastMCP

# ─── In-memory ticket store ─────────────────────────────────────────
VALID_PRIORITIES = {"Low", "Medium", "High", "Critical"}
VALID_STATUSES = {"Open", "In Progress", "Resolved", "Closed"}

_next_id = 1
_tickets: dict[int, dict[str, Any]] = {}


def _new_id() -> int:
    global _next_id
    ticket_id = _next_id
    _next_id += 1
    return ticket_id


def _seed_tickets() -> None:
    samples = [
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
            "title": "Software license expired — Adobe Creative Suite",
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
    for sample in samples:
        tid = _new_id()
        _tickets[tid] = {
            "id": tid,
            **sample,
            "createdAt": datetime.now(timezone.utc).isoformat(),
        }


_seed_tickets()

# ─── MCP Server ──────────────────────────────────────────────────────
mcp = FastMCP(
    "IT Support Ticketing System",
    instructions=(
        "This server manages IT support tickets. Use the provided tools to "
        "list, view, create, update, and close tickets."
    ),
)


@mcp.tool()
def list_tickets(status: str | None = None, priority: str | None = None) -> list[dict]:
    """List all tickets with optional filters for status and priority.

    Args:
        status: Filter by status (Open, In Progress, Resolved, Closed). Leave empty for all.
        priority: Filter by priority (Low, Medium, High, Critical). Leave empty for all.
    """
    results = list(_tickets.values())
    if status:
        results = [t for t in results if t["status"] == status]
    if priority:
        results = [t for t in results if t["priority"] == priority]
    return results


@mcp.tool()
def get_ticket(ticket_id: int) -> dict | str:
    """Get details of a specific ticket by ID.

    Args:
        ticket_id: The numeric ID of the ticket to retrieve.
    """
    ticket = _tickets.get(ticket_id)
    if not ticket:
        return f"Ticket #{ticket_id} not found."
    return ticket


@mcp.tool()
def create_ticket(
    title: str,
    description: str,
    priority: str,
    assignee: str = "",
) -> dict | str:
    """Create a new ticket.

    Args:
        title: Brief summary of the issue (required).
        description: Detailed description of the issue (required).
        priority: Priority level — one of Low, Medium, High, Critical (required).
        assignee: Name of the assigned technician (optional).
    """
    if not title or not title.strip():
        return "Error: title is required."
    if not description or not description.strip():
        return "Error: description is required."
    if priority not in VALID_PRIORITIES:
        return f"Error: priority must be one of {sorted(VALID_PRIORITIES)}."

    tid = _new_id()
    _tickets[tid] = {
        "id": tid,
        "title": title.strip(),
        "description": description.strip(),
        "priority": priority,
        "status": "Open",
        "assignee": assignee.strip(),
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }
    return _tickets[tid]


@mcp.tool()
def update_ticket(
    ticket_id: int,
    status: str | None = None,
    assignee: str | None = None,
) -> dict | str:
    """Update a ticket's status or assignee.

    Args:
        ticket_id: The numeric ID of the ticket to update.
        status: New status (Open, In Progress, Resolved, Closed). Leave empty to keep current.
        assignee: New technician name. Leave empty to keep current.
    """
    ticket = _tickets.get(ticket_id)
    if not ticket:
        return f"Ticket #{ticket_id} not found."
    if status is not None:
        if status not in VALID_STATUSES:
            return f"Error: status must be one of {sorted(VALID_STATUSES)}."
        ticket["status"] = status
    if assignee is not None:
        ticket["assignee"] = assignee.strip()
    return ticket


@mcp.tool()
def close_ticket(ticket_id: int) -> dict | str:
    """Close a ticket by ID.

    Args:
        ticket_id: The numeric ID of the ticket to close.
    """
    ticket = _tickets.get(ticket_id)
    if not ticket:
        return f"Ticket #{ticket_id} not found."
    ticket["status"] = "Closed"
    return ticket

@mcp.tool()
def close_vlads_ticket(ticket_id: int) -> dict | str:
    """Close a ticket by ID.

    Args:
        ticket_id: The numeric ID of the ticket to close.
    """
    ticket = _tickets.get(ticket_id)
    if not ticket:
        return f"Ticket #{ticket_id} not found."
    ticket["status"] = "Closed"
    return ticket


if __name__ == "__main__":
    import sys

    transport = "streamable-http" if "--http" in sys.argv else "stdio"
    mcp.run(transport=transport)
