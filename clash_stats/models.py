from datetime import datetime

from pony.orm import Database, Optional, PrimaryKey, Required, Set

from . import SQLITE_FILE  # PSQL_DB, PSQL_HOST, PSQL_PASSWORD, PSQL_USER

db = Database()
db.bind(provider="sqlite", filename=SQLITE_FILE, create_db=True)
# db.bind(
#     provider="postgres",
#     database=PSQL_DB,
#     user=PSQL_USER,
#     host=PSQL_HOST,
#     password=PSQL_PASSWORD,
# )


class Player(db.Entity):
    id = PrimaryKey(int, auto=True)
    tag = Required(str)
    name = Required(str)
    townHallLevel = Required(int)
    townHallWeaponLevel = Optional(int)
    expLevel = Required(int)
    trophies = Required(int)
    bestTrophies = Required(int)
    warStars = Required(int)
    attackWins = Required(int)
    defenseWins = Required(int)
    builderHallLevel = Optional(int)
    versusTrophies = Required(int)
    bestVersusTrophies = Required(int)
    versusBattleWins = Required(int)
    donations = Required(int)
    donationsReceived = Required(int)
    clan = Optional("Clan")
    achievements = Set("Achievement")
    datetime = Required(datetime)
    troops = Set("Troop")
    spells = Set("Spell")


class Clan(db.Entity):
    id = PrimaryKey(int, auto=True)
    tag = Optional(str)
    name = Optional(str)
    clanLevel = Optional(int)
    player = Required(Player)


class Achievement(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    stars = Optional(int)
    value = Optional(int)
    target = Optional(int)
    info = Optional(str)
    completionInfo = Optional(str)
    village = Optional(str)
    player = Required(Player)


class Troop(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    level = Required(int)
    maxLevel = Required(int)
    village = Required(str)
    player = Required(Player)


class Spell(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    level = Required(int)
    maxLevel = Required(int)
    village = Required(str)
    player = Required(Player)


db.generate_mapping(create_tables=True)
