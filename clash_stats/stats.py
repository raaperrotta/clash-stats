from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
from pony.orm import db_session, select

from .models import Achievement


@db_session
def get_total_loot_over_time_all(max_age: Optional[timedelta] = None):

    relevant_achievements = {"Gold Grab", "Elixir Escapade", "Heroic Heist"}

    columns = [
        "player_name",
        "player_tag",
        "datetime",
        "achievement_name",
        "achievement_value",
    ]

    min_datetime = (datetime.now() - max_age) if max_age else datetime.min

    return pd.DataFrame(
        select(
            (a.player.name, a.player.tag, a.player.datetime, a.name, a.value)
            for a in Achievement
            if a.name in relevant_achievements and a.player.datetime >= min_datetime
        )[:],
        columns=columns,
    )


@db_session
def any_achievements_changed(max_age: Optional[timedelta] = None):

    irrelevant_achievements = {
        "Unbreakable",
        "Next Generation Model",
        "Master Engineer",
        "Bigger & Better",
        "Hidden Treasures",
        "Release the Beasts",
        "Empire Builder",
        "Bigger Coffers",
    }

    columns = [
        "player_name",
        "player_tag",
        "datetime",
        "achievement_name",
        "achievement_value",
    ]

    min_datetime = (datetime.now() - max_age) if max_age else datetime.min

    return pd.DataFrame(
        select(
            (a.player.name, a.player.tag, a.player.datetime, a.name, a.value)
            for a in Achievement
            if a.name not in irrelevant_achievements
            and a.player.datetime >= min_datetime
        )[:],
        columns=columns,
    )
