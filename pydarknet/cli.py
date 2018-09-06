import click


@click.group()
@click.version_option()
def cli():
    """Naval Fate.
    This is the docopt example adopted to Click but with some actual
    commands implemented and not just the empty parsing which really
    is not all that interesting.
    """


@cli.group()
def ship():
    """Manages ships."""


@ship.command("new")
@click.argument("name")
def ship_new(name):
    """Creates a new ship."""
    click.echo("Created ship %s" % name)
