from environs import Env

env = Env()

SQLITE_FILE = env.str("SQLITE_FILE")
REDIS_URL = env.str("REDIS_URL")
