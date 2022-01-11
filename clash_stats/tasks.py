from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger

from . import client

LOGGER = get_task_logger(__name__)
LOGGER.info("Importing the %s module", __name__)

LOGGER.info("Connecting celery to redis")
app = Celery(
    "clash", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0"
)
LOGGER.info("Connected celery to redis")


@app.task
def get_and_write_player(player_tag):
    LOGGER.debug("Fetching player data for player tag %s", player_tag)
    player_data = client.get_player(player_tag)
    LOGGER.debug(
        "Writing player data to database for player tag %s (%s)",
        player_tag,
        player_data["name"],
    )
    client.write_player(player_data)


@app.task
def get_and_write_clan(clan_tag):
    LOGGER.debug("Fetching clan data for clan tag %s", clan_tag)
    members = client.get_clan_members(clan_tag)
    for member in members:
        LOGGER.debug("Fetching player data for player tag %s", member["tag"])
        player_data = client.get_player(member["tag"])
        LOGGER.debug(
            "Writing player data to database for player tag %s (%s)",
            member["tag"],
            member["name"],
        )
        client.write_player(player_data)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    LOGGER.info(
        "Setting up periodic task to fetch data for clan #8998L2GJ every 10 minutes"
    )
    sender.add_periodic_task(crontab(minute="*/10"), get_and_write_clan.si("#8998L2GJ"))
