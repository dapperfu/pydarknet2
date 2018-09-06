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
    default=default_darknet_clone_url,
    help="Speed in knots.",
)
@click.option(
    "--root",
    metavar="root",
    default=default_darknet_root,
    help="Darknet root directory",
)
def clone(root=default_darknet_root, url):
    """Clone a darknet repository"""
    click.echo("URL: %s" % url)
    click.echo("Root: %s" % root)
