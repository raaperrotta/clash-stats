from datetime import timedelta

import holoviews as hv
from bokeh import themes

from .stats import any_achievements_changed, get_total_loot_over_time_all

hv.extension("bokeh")
RENDERER = hv.renderer("bokeh")
# RENDERER.theme = themes.built_in_themes['dark_minimal ,']


def activity(**kwargs):
    data = any_achievements_changed(max_age=timedelta(**kwargs))
    names = data.groupby("player_tag")["player_name"].last().to_dict()
    data["value_changed"] = (
        data.sort_values("datetime")
        .groupby(["player_tag", "achievement_name"], sort=False)["achievement_value"]
        .diff()
    )
    data = (
        data.groupby(["player_tag", "datetime"])["value_changed"].any()
    ).reset_index()
    data["player_tag"] = data["player_tag"].apply(lambda t: f"{t} ({names[t]})")
    data.set_index("player_tag", inplace=True)

    sorted_tags = (
        data.groupby("player_tag").sum().sort_values("value_changed", ascending=True)
    )
    data = data.loc[sorted_tags.index].reset_index()
    plot = hv.Scatter(
        data.loc[data["value_changed"]], "datetime", "player_tag"
    ).options(height=650, responsive=True, marker="diamond", size=5)
    return RENDERER.static_html(plot)


def weekly_activity():
    n_per_day = 6  # should be a factor of 24
    hours_per_bin = 24 / n_per_day

    data = any_achievements_changed()
    names = data.groupby("player_tag")["player_name"].last().to_dict()
    data["value_changed"] = (
        data.sort_values("datetime")
        .groupby(["player_tag", "achievement_name"], sort=False)["achievement_value"]
        .diff()
    )
    data = (
        data.groupby(["player_tag", "datetime"])["value_changed"].any()
    ).reset_index()
    data["player_tag"] = data["player_tag"].apply(lambda t: f"{t} ({names[t]})")
    data.set_index("player_tag", inplace=True)

    sorted_tags = (
        data.groupby("player_tag").sum().sort_values("value_changed", ascending=True)
    )
    data = data.loc[sorted_tags.index].reset_index()

    data["day_of_week"] = data["datetime"].dt.day_name()
    data["part_of_day"] = data["datetime"].dt.hour // hours_per_bin

    def bin_label(row):
        day_name = row["day_of_week"]
        part_of_day = row["part_of_day"]
        hour_start = hours_per_bin * part_of_day
        hour_end = hour_start + hours_per_bin
        return f"{day_name} {hour_start:02.0f}00 - {hour_end:02.0f}00"

    data["time_bin"] = data.apply(bin_label, axis=1)

    data = (
        data.groupby(["player_tag", "time_bin"], sort=False)["value_changed"]
        .sum()
        .reset_index()
    )

    plot = hv.Scatter(data, "time_bin", ["player_tag", "value_changed"]).options(
        height=1200,
        responsive=True,
        marker="o",
        size=16,
        padding=0.02,
        color_index="value_changed",
        cmap="greens",
        xrotation=45,
    )
    return RENDERER.static_html(plot)


def loot_gained(**kwargs):
    def plot(data, achievement_name, axis_name):
        data = data.loc[data["achievement_name"] == achievement_name].sort_values(
            "datetime"
        )

        groups = data.groupby(["player_tag", "achievement_name"])
        data[axis_name] = (
            data["achievement_value"] - groups.transform("first")["achievement_value"]
        )

        last = (
            data.groupby(["achievement_name", "player_tag"])
            .last()
            .reset_index()  # so the player_tag is a regular column accessible to the hv.Labels object
            .sort_values(
                "player_tag"
            )  # so colors are applied in same order in labels and curves
        )

        xmin = data["datetime"].min()
        xmax = data["datetime"].max()
        newmax = xmax + (xmax - xmin) * 0.20

        curves = (
            hv.Curve(
                data, [("datetime", "Time"), axis_name], ["player_name", "player_tag"]
            )
            .redim.range(datetime=(xmin, newmax))
            .groupby("player_tag")
            .options(color=hv.Cycle("Category10"))
            .overlay()
        )
        labels = hv.Labels(
            last, ["datetime", axis_name], ["player_name", "player_tag"]
        ).options(text_align="left", text_color="player_tag", cmap="Category10")

        return (curves * labels).options(
            height=950, padding=0.05, yformatter="%d", width=600
        )

    data = get_total_loot_over_time_all(timedelta(**kwargs))

    plot = hv.Layout(
        [
            plot(data, achievement_name, axis_name)
            for achievement_name, axis_name in [
                ("Gold Grab", "Gold Looted"),
                ("Elixir Escapade", "Elixir Looted"),
                ("Heroic Heist", "Dark Elixir Looted"),
            ]
        ]
    ).options(width=1800)
    return RENDERER.static_html(plot)
