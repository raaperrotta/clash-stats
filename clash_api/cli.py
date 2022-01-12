from pprint import pprint

import click

from . import client


@click.group()
def cli():
    pass


@cli.command()
@click.argument("player_tag", type=str)
def player(player_tag):
    player_json = client.get_player(player_tag)
    pprint(player_json)


@cli.command()
@click.argument("clan_tag", type=str)
def clan(clan_tag):
    clan_json = client.get_clan_members(clan_tag)
    pprint(clan_json)


if __name__ == "__main__":
    cli()
