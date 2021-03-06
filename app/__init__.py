import os

from flask import Flask
from flask_apscheduler import APScheduler
from app.static.py.badgecraft import BadgeCraft


def scheduled():
    token = os.environ.get('TOKEN')
    badgecraft.fetched_amount = badgecraft.fetched_amount + 1
    print(badgecraft.fetched_amount)

    badgecraft.fetch(token)


scheduler = APScheduler()
scheduler.add_job(id='Fetches Data from Badgecraft', func=scheduled, trigger='interval', seconds=1800)
scheduler.start()

app = Flask(__name__)

badgecraft = BadgeCraft()
badgecraft.fetch(os.environ.get('TOKEN'))
from . import routes
