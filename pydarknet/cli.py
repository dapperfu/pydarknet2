import click


@click.group()
@click.version_option()
def cli():
    """darknet.py

    darknet.py is an attempt at darknet implemented in Python using libdarknet.
    """


@cli.group("darknet")
def darknet():
    """Manages cloned darknet repository."""


@ship.command("new")
@click.argument("name")
def ship_new(name):
    """Creates a new ship."""
    click.echo("Created ship %s" % name)
