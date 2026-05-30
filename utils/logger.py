import requests

from database.db import SUPABASE_URL
from utils.config import HEADERS


def write_log(
    action_type,
    module_name,
    user_name,
    record_id,
    description
):

    payload = {

        "action_type": action_type,
        "module_name": module_name,
        "user_name": user_name,
        "record_id": record_id,
        "description": description

    }

    try:

        requests.post(
            f"{SUPABASE_URL}/rest/v1/audit_logs",
            headers=HEADERS,
            json=payload
        )

    except Exception:
        pass