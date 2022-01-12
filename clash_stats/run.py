import logging.handlers

from clash_stats import client

LOGGER = logging.getLogger(__name__)
LOGGER.info("Importing the %s module", __name__)


def get_and_write_player(player_tag):
    LOGGER.debug("Fetching player data for player tag %s", player_tag)
    player_data = client.get_player(player_tag)
    LOGGER.debug(
        "Writing player data to database for player tag %s (%s)",
        player_tag,
        player_data["name"],
    )
    client.write_player(player_data)


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


def _main():
    LOGGER.setLevel(logging.DEBUG)
    for handler in [
        logging.StreamHandler(),
        logging.handlers.RotatingFileHandler(
            "run.log", maxBytes=20_000, backupCount=10
        ),
    ]:
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(
            logging.Formatter("%(levelname).1s - %(asctime)s - %(name)s: %(message)s")
        )
        LOGGER.addHandler(handler)
    LOGGER.info("Fetching data for clan #8998L2GJ")
    get_and_write_clan("#8998L2GJ")


if __name__ == "__main__":
    _main()
