# Clash Stats

Data collector for the [Clash of Clans API](https://developer.clashofclans.com/#/)

# The Stack

Data collection is scheduled with celery, using Redis as a broker, and written to a sqlite database using Pony ORM.

# Setup

To run locally following these instructions, you will need Docker and Python (tested with 3.9).

Create a `.env` file to manage your configuration with the following contents (replacing the ellipsis with your own API token)

```
CLASH_API_URL="https://api.clashofclans.com"
CLASH_API_KEY="..."
SQLITE_FILE="../clash.db"
```

Load the environment variables into your session (e.g. with `export $(grep -v '^#' .env | xargs)`)

Start redis using Docker with the following command: `docker up -d redis -p 6379:6379 -d redis`

Create a python virtual environment for this project
with pip (`python3.9 -m venv PATH/TO/VENV && source PATH/TO/VENV/bin/activate`) or
with conda (`conda create -n VENV_NAME python=3.9 pip && conda activate VENV_NAME`)

Install the project dependencies using pip
(even if you used conda to create the virtual environment):
`pip install -r requirements.txt`

Collect data one time by running `python main.py`

Set celery to continuously collect data using `celery -A clash_stats.tasks worker -B`
