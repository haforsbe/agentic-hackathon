"""MCP server that exposes the IT Support Ticketing System as tools via streamable HTTP."""

from mcp.server.fastmcp import FastMCP
from ticket_store import close_ticket as close_ticket_in_store
from ticket_store import create_ticket as create_ticket_in_store
from ticket_store import get_ticket, list_tickets as list_tickets_in_store
from ticket_store import update_ticket as update_ticket_in_store

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
    return list_tickets_in_store(status=status, priority=priority)


@mcp.tool()
def get_ticket(ticket_id: int) -> dict | str:
    """Get details of a specific ticket by ID.

    Args:
        ticket_id: The numeric ID of the ticket to retrieve.
    """
    ticket = get_ticket(ticket_id)
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
    try:
        return create_ticket_in_store(title, description, priority, assignee)
    except ValueError as error:
        return f"Error: {error}."


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
    try:
        ticket = update_ticket_in_store(ticket_id, status, assignee)
    except ValueError as error:
        return f"Error: {error}."
    return ticket or f"Ticket #{ticket_id} not found."


@mcp.tool()
def close_ticket(ticket_id: int) -> dict | str:
    """Close a ticket by ID.

    Args:
        ticket_id: The numeric ID of the ticket to close.
    """
    ticket = close_ticket_in_store(ticket_id)
    return ticket or f"Ticket #{ticket_id} not found."


if __name__ == "__main__":
    import sys

    transport = "streamable-http" if "--http" in sys.argv else "stdio"
    mcp.run(transport=transport)
