import click

from .config import config


@click.group()
@click.version_option()
def cli():
    """darknet.py

    darknet.py is an attempt at darknet implemented in Python using libdarknet.
    """


@cli.group("darknet")
def darknet():
    """Manages cloned darknet repository."""


@darknet.command("clone")
@click.option(
    "--url",
    metavar="url",
    default=config["darknet"]["clone_url"],
    help="Clone URL",
)
@click.option(
    "--root",
    metavar="root",
    default=config["darknet"]["root"],
    help="Darknet root directory",
)
def clone(root=config["darknet"]["root"], url=config["darknet"]["clone_url"]):
    """Clone a darknet repository"""
    click.echo("URL: %s" % url)
    click.echo("Root: %s" % root)

    import pydarknet

    darknet = pydarknet.darknet.Darknet(root=root)
    darknet.clone(clone_url=url)
