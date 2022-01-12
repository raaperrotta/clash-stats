from environs import Env

env = Env()

CLASH_API_URL = env.str("CLASH_API_URL")
CLASH_API_KEY = env.str("CLASH_API_KEY")
