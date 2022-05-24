import click
from app import app
from app.static.py.badgecraft import fetch


@app.cli.command("scheduled")
@click.argument('token')
def scheduled(token):
    print(token)
    fetch(token)
