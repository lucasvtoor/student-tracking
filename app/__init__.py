from flask import Flask
from flask_apscheduler import APScheduler
from app.static.py.badgecraft import BadgeCraft

app = Flask(__name__)
from . import routes, commands

scheduler = APScheduler()
scheduler.add_job(id='Fetches Data from Badgecraft', func=commands.scheduled, trigger='interval', seconds=600)
scheduler.start()
badgecraft = BadgeCraft()
