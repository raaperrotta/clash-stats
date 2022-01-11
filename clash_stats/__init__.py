from environs import Env

env = Env()

CLASH_API_URL = env.str("CLASH_API_URL")
CLASH_API_KEY = env.str("CLASH_API_KEY")

PSQL_USER = env.str("PSQL_USER")
PSQL_HOST = env.str("PSQL_HOST")
PSQL_DB = env.str("PSQL_DB")
PSQL_PASSWORD = env.str("PSQL_PASSWORD")
