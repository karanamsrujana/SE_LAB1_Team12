"""A simple helpdesk ticket management system."""

import json
import os
import platform
import re
import shutil
import subprocess  # nosec B404
from datetime import datetime
from itertools import count


# Global state
tickets = {}
_next_ticket_id = count(101)
ADMIN_PASSWORD = os.environ.get("HELPDESK_ADMIN_PASSWORD")


def raise_ticket(user, issue_type, urgency="3", audit_trail=None):
    """Create a new helpdesk ticket and return its ID."""
    ticket_id = next(_next_ticket_id)

    tickets[ticket_id] = {
        "user": user,
        "issue": issue_type,
        "priority": int(urgency),
        "tech": None,
        "notes": [],
    }

    if audit_trail is None:
        audit_trail = []

    audit_trail.append(
        f"{user} raised #{ticket_id} at {datetime.now()}"
    )
    return ticket_id


def assign_ticket(ticket_id, technician):
    """Assign a ticket to a technician."""
    tickets[ticket_id]["tech"] = technician


def add_note(ticket_id, note):
    """Add a note to a ticket; return False if it does not exist."""
    try:
        tickets[ticket_id]["notes"].append(note)
        return True
    except KeyError:
        return False


def close_ticket(ticket_id, password):
    """Close a ticket if the supplied password is correct."""
    if password == ADMIN_PASSWORD and ADMIN_PASSWORD:
        tickets.pop(ticket_id, None)


def unresolved_high_priority():
    """Return IDs of high-priority tickets without an assigned technician."""
    result = []

    for ticket_id, ticket in tickets.items():
        if ticket["priority"] >= 4 and ticket["tech"] is None:
            result.append(ticket_id)

    return result


def ping_user_machine(hostname):
    """Ping a validated hostname once."""
    if not isinstance(hostname, str):
        raise ValueError("Invalid hostname")

    if not re.fullmatch(r"[A-Za-z0-9.-]+", hostname):
        raise ValueError("Invalid hostname")

    ping_executable = shutil.which("ping")

    if ping_executable is None:
        return 1

    ping_option = "-n" if platform.system() == "Windows" else "-c"

    # Safe: validated hostname, resolved executable and shell=False.
    return subprocess.run(  # nosec B603
        [ping_executable, ping_option, "1", hostname],
        check=False,
        shell=False,
    ).returncode


def save_tickets(file="tickets.json"):
    """Save all tickets to a JSON file."""
    with open(file, "w", encoding="utf-8") as ticket_file:
        json.dump(tickets, ticket_file, indent=4)


def main():
    """Run a demonstration of the helpdesk ticket system."""
    ticket_1 = raise_ticket("anil", "printer", "5")
    ticket_3 = raise_ticket("joe", "vpn", "2")

    assign_ticket(ticket_1, "Tech-Kiran")
    add_note(999, "Called user")

    print(
        "Unassigned high priority:",
        unresolved_high_priority(),
    )

    level = (
        input("Urgency for a new laptop ticket (1-5, Enter for 3): ")
        or "3"
    )
    raise_ticket("sana", "laptop", level)

    if ADMIN_PASSWORD:
        close_ticket(ticket_3, ADMIN_PASSWORD)

    save_tickets()
    print("Open tickets:", list(tickets.keys()))


if __name__ == "__main__":
    main()
