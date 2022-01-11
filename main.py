from pony.orm import set_sql_debug

from clash_stats import client, stats, tasks


def fetch_my_data():
    """Fetch player data for Robert and Colleen"""
    client.write_player(client.get_player("#RL2C0UYY"))
    client.write_player(client.get_player("#RULJG8Q9"))


def fetch_clan_data():
    """Fetch all FearTheClan members' data"""
    members = client.get_clan_members("#8998L2GJ")
    for member in members:
        print("Fetching data for", member["name"])
        client.write_player(client.get_player(member["tag"]))


def try_celery():
    # tasks.get_and_write_player.delay('#RL2C0UYY')
    tasks.get_and_write_clan("#8998L2GJ")


def main():
    set_sql_debug(True)
    try_celery()


if __name__ == "__main__":
    main()

# To fetch the latest results for each player tag
# SELECT DISTINCT ON (tag) tag, datetime, name, id FROM player ORDER BY tag, datetime desc;
