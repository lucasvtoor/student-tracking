import click
from flask import Flask
from app.static.py.badgecraft import fetch, TOKEN

app = Flask(__name__)
# fetchData = fetch()

from . import routes, commands

print("starting")

app.cli.add_command(commands.scheduled)
