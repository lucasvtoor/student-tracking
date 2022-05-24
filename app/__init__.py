import click
from flask import Flask
from app.static.py.badgecraft import BadgeCraft

app = Flask(__name__)
badgecraft = BadgeCraft()
from . import routes, commands

app.cli.add_command(commands.scheduled)
