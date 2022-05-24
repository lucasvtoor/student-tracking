import click
from flask import Flask
from app.static.py.badgecraft import fetch, TOKEN

app = Flask(__name__)
fetchData = fetch()

from . import routes


@app.cli.command("scheduled")
@click.option('--token')
def scheduled(token):
    print(token)
    fetch(token)


app.cli.add_command(scheduled)
