from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from app.static.py.badgecraft import fetch, TOKEN
import time
import atexit



scheduler = BackgroundScheduler()
scheduler.add_job(func=lambda: fetch(TOKEN), trigger="interval", seconds=10800)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

app = Flask(__name__)
fetchData = fetch(TOKEN)


from . import routes
