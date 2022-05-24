from flask import Flask
from flask_apscheduler import APScheduler
from app.static.py.badgecraft import BadgeCraft

app = Flask(__name__)

scheduler = APScheduler()
scheduler.add_job(id='Fetches Data from Badgecraft', func=commands.scheduled, trigger='interval', seconds=600)
scheduler.start()
badgecraft = BadgeCraft()


def scheduled(token):
    badgecraft.fetched_amount = badgecraft.fetched_amount + 1
    print(badgecraft.fetched_amount)

    badgecraft.fetch(token)
