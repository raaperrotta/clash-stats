from datetime import datetime
from urllib.parse import quote_plus

import requests

from . import CLASH_API_KEY, CLASH_API_URL

HEADERS = {"authorization": f"Bearer {CLASH_API_KEY}"}


def get_player(player_tag: str) -> dict:
    response = requests.get(
        f"{CLASH_API_URL}/v1/players/{quote_plus(player_tag)}", headers=HEADERS
    )
    response.raise_for_status()
    data = response.json()
    data["datetime"] = datetime.utcnow()
    return data


def get_clan_members(clan_tag: str) -> dict:
    response = requests.get(
        f"{CLASH_API_URL}/v1/clans/{quote_plus(clan_tag)}/members", headers=HEADERS
    )
    response.raise_for_status()
    return response.json()["items"]  # assumes one page
