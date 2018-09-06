import click

from .config import default_darknet_clone_url, default_darknet_root


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
def clone(url, root):
    """Creates a new ship."""
    click.echo("URL: %s" % url)
    click.echo("Root: %s" % url)
