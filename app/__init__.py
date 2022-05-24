from flask import Flask
from flask_apscheduler import APScheduler
from app.static.py.badgecraft import BadgeCraft

app = Flask(__name__)


def scheduled(token):
    badgecraft.fetched_amount = badgecraft.fetched_amount + 1
    print(badgecraft.fetched_amount)

    badgecraft.fetch(token)


scheduler = APScheduler()
scheduler.add_job(id='Fetches Data from Badgecraft', func=scheduled, trigger='interval', seconds=600)
scheduler.start()
badgecraft = BadgeCraft()
