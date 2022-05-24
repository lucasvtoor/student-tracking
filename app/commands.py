import click
from app import app, badgecraft


@app.cli.command("scheduled")
@click.argument('token')
def scheduled(token):
    badgecraft.fetched_amount = badgecraft.fetched_amount + 1
    print(badgecraft.fetched_amount)

    badgecraft.fetch(token)


