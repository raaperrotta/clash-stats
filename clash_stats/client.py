from datetime import datetime
from urllib.parse import quote_plus

import requests
from pony.orm import db_session

from . import CLASH_API_KEY, CLASH_API_URL, models

HEADERS = {"authorization": f"Bearer {CLASH_API_KEY}"}


def get_player(player_tag: str) -> dict:
    response = requests.get(
        f"{CLASH_API_URL}/v1/players/{quote_plus(player_tag)}", headers=HEADERS
    )
    response.raise_for_status()
    data = response.json()
    data["datetime"] = datetime.utcnow()
    return data


@db_session
def write_player(player_json: dict):
    player = models.Player(
        tag=player_json["tag"],
        name=player_json["name"],
        townHallLevel=player_json["townHallLevel"],
        townHallWeaponLevel=player_json.get("townHallWeaponLevel"),
        expLevel=player_json["expLevel"],
        trophies=player_json["trophies"],
        bestTrophies=player_json["bestTrophies"],
        warStars=player_json["warStars"],
        attackWins=player_json["attackWins"],
        defenseWins=player_json["defenseWins"],
        builderHallLevel=player_json.get("builderHallLevel"),
        versusTrophies=player_json["versusTrophies"],
        bestVersusTrophies=player_json["bestVersusTrophies"],
        versusBattleWins=player_json["versusBattleWins"],
        donations=player_json["donations"],
        donationsReceived=player_json["donationsReceived"],
        datetime=player_json["datetime"],
    )
    clan_json = player_json["clan"]
    if clan_json:
        models.Clan(
            player=player,
            tag=clan_json["tag"],
            name=clan_json["name"],
            clanLevel=clan_json["clanLevel"],
        )
    for achievement_json in player_json["achievements"]:
        models.Achievement(
            player=player,
            name=achievement_json["name"],
            stars=achievement_json["stars"],
            value=achievement_json["value"],
            target=achievement_json["target"],
            info=achievement_json["info"],
            completionInfo=achievement_json["completionInfo"] or "",
            village=achievement_json["village"],
        )
    for troop_json in player_json["troops"]:
        models.Troop(
            player=player,
            name=troop_json["name"],
            level=troop_json["level"],
            maxLevel=troop_json["maxLevel"],
            village=troop_json["village"],
        )
    for troop_json in player_json["heroes"]:
        models.Troop(
            player=player,
            name=troop_json["name"],
            level=troop_json["level"],
            maxLevel=troop_json["maxLevel"],
            village=troop_json["village"],
        )
    for spell_json in player_json["spells"]:
        models.Spell(
            player=player,
            name=spell_json["name"],
            level=spell_json["level"],
            maxLevel=spell_json["maxLevel"],
            village=spell_json["village"],
        )


def get_clan_members(clan_tag: str) -> dict:
    response = requests.get(
        f"{CLASH_API_URL}/v1/clans/{quote_plus(clan_tag)}/members", headers=HEADERS
    )
    response.raise_for_status()
    return response.json()["items"]  # assumes one page
