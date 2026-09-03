import json
import os

from datetime import datetime
from zoneinfo import ZoneInfo


LOG_FOLDER = "logs"
LOG_FILE = os.path.join(
    LOG_FOLDER,
    "agent_audit.jsonl"
)

LOCAL_TIMEZONE = ZoneInfo(
    "America/Los_Angeles"
)


def ensure_log_folder():
    os.makedirs(
        LOG_FOLDER,
        exist_ok=True
    )


def write_log(event_type, details):
    ensure_log_folder()

    log_entry = {
        "timestamp": datetime.now(
            LOCAL_TIMEZONE
        ).isoformat(),
        "event_type": event_type,
        "details": details
    }

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as file:
        file.write(
            json.dumps(log_entry)
            + "\n"
        )