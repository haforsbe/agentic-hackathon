"""Serve the ticketing UI and its shared ticket API on localhost:3000."""

import json
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from ticket_store import close_ticket, create_ticket, list_tickets, update_ticket

APP_DIRECTORY = Path(__file__).parent


class TicketingRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(APP_DIRECTORY), **kwargs)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/api/tickets":
            super().do_GET()
            return
        filters = parse_qs(parsed.query)
        self._send_json(
            HTTPStatus.OK,
            list_tickets(
                status=filters.get("status", [None])[0],
                priority=filters.get("priority", [None])[0],
            ),
        )

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path.endswith("/close"):
            ticket = self._ticket_from_path(parsed.path.removesuffix("/close"))
            if ticket is not None:
                ticket = close_ticket(ticket)
            self._send_ticket_result(ticket)
            return

        payload = self._read_json()
        if payload is None:
            return
        if parsed.path == "/api/tickets":
            try:
                ticket = create_ticket(**payload)
            except (TypeError, ValueError) as error:
                self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
                return
            self._send_json(HTTPStatus.CREATED, ticket)
            return
        self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})

    def do_PUT(self) -> None:
        ticket_id = self._ticket_from_path(urlparse(self.path).path)
        payload = self._read_json()
        if ticket_id is None or payload is None:
            return
        try:
            ticket = update_ticket(ticket_id, **payload)
        except (TypeError, ValueError) as error:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
            return
        self._send_ticket_result(ticket)

    def _ticket_from_path(self, path: str) -> int | None:
        parts = path.strip("/").split("/")
        if len(parts) != 3 or parts[:2] != ["api", "tickets"]:
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})
            return None
        try:
            return int(parts[2])
        except ValueError:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Ticket ID must be numeric"})
            return None

    def _read_json(self) -> dict | None:
        try:
            length = int(self.headers.get("Content-Length", "0"))
            return json.loads(self.rfile.read(length))
        except (ValueError, json.JSONDecodeError):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Request body must be JSON"})
            return None

    def _send_ticket_result(self, ticket: dict | None) -> None:
        if ticket is None:
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Ticket not found"})
            return
        self._send_json(HTTPStatus.OK, ticket)

    def _send_json(self, status: HTTPStatus, data: object) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("", 3000), TicketingRequestHandler)
    print("Ticketing app available at http://localhost:3000")
    server.serve_forever()