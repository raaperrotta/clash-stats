# from flask import Flask, request
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from clash_stats import plots

# app = Flask(__name__)
app = FastAPI()


# @app.route('/activity')
@app.get("/activity", response_class=HTMLResponse)
def a(
    days: float = 0,
    seconds: float = 0,
    minutes: float = 0,
    hours: float = 0,
    weeks: float = 0,
):
    return plots.activity(
        days=days, seconds=seconds, minutes=minutes, hours=hours, weeks=weeks
    )


@app.get("/weekly_activity", response_class=HTMLResponse)
def b():
    return plots.weekly_activity()


@app.get("/loot_gained", response_class=HTMLResponse)
def c(
    days: float = 0,
    seconds: float = 0,
    minutes: float = 0,
    hours: float = 0,
    weeks: float = 0,
):
    return plots.loot_gained(
        days=days, seconds=seconds, minutes=minutes, hours=hours, weeks=weeks
    )


# if __name__ == '__main__':
#     app.run(debug=True)
