import click
from app import app,badgecraft


@app.cli.command("scheduled")
@click.argument('token')
def scheduled(token):
    badgecraft.fetch(token)
