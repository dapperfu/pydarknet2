import os

import click

from .config import config
from .utils import url_is_alive

import pydarknet


@click.group()
@click.version_option()
def cli():
    """darknet.py

    darknet.py is a tool for interacting with pydarknet from the
    command line.
    """


@cli.group("darknet")
def darknet():
    """Manages local darknet folder."""

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
def clone(
    root=config["darknet"]["root"],
    url=config["darknet"]["clone_url"],
    force=False,
):
    """Clone a darknet repository"""
    click.echo("URL: %s" % url)
    click.echo("Root: %s" % root)

    import pydarknet

    darknet = pydarknet.darknet.Darknet(root=root)
    darknet.clone(clone_url=url, force=force)


@darknet.command("build")
@click.option(
    "--root",
    metavar="root",
    default=config["darknet"]["root"],
    help="Darknet root directory",
)
@click.option("--gpu", is_flag=True, help="Compile with GPU support.")
@click.option("--cudnn", is_flag=True, help="Compile with cudnn support.")
@click.option("--opencv", is_flag=True, help="Compile with OpenCV support.")
@click.option("--openmp", is_flag=True, help="Compile with OpenMP support.")
@click.option("--force", is_flag=True, help="Do it.")
def build(gpu, cudnn, opencv, openmp, force, root):
    """Build """
    import pydarknet

    darknet = pydarknet.darknet.Darknet(root=root)
    darknet.build(gpu=gpu, cudnn=cudnn, opencv=opencv, openmp=openmp, force=force)


@cli.group("weights")
def weights():
    """Manages darknet weights."""


@weights.command("list")
@click.option(
    "--root",
    metavar="root",
    default=config["darknet"]["root"],
    help="Darknet root directory",
)
@click.option(
    "--weights",
    metavar="weights",
    default=config["darknet"]["weight_dir"],
    help="Darknet root directory",
)
def list_weights(
    root=config["darknet"]["root"], weights=config["darknet"]["weight_dir"]
):
    darknet = pydarknet.darknet.Darknet(root=root, weight_dir=weights)
    for weight in darknet.weights:
        print(weight)


@weights.command("available")
@click.option(
    "--root",
    metavar="root",
    default=config["darknet"]["root"],
    help="Darknet root directory",
)
@click.option(
    "--weight_url",
    metavar="weight_url",
    default=config["weights"]["url_root"],
    help="Darknet root directory",
)
def available(
    root=config["darknet"]["root"], weight_url=config["weights"]["url_root"]
):
    import pydarknet

    darknet = pydarknet.darknet.Darknet(root=root)
    for cfg in darknet.cfgs:
        basename = ".".join(os.path.basename(cfg).split(".")[0:-1])
        alive = url_is_alive(weight_url + basename + ".weights")
        print("{}: {}".format(basename, alive))


@weights.command("download")
@click.argument("weight")
@click.option(
    "--root",
    metavar="root",
    default=config["darknet"]["root"],
    help="Darknet root directory",
)
@click.option(
    "--weight_url",
    metavar="weight_url",
    default=config["weights"]["url_root"],
    help="Darknet root directory",
)
@click.option(
    "--weights",
    metavar="weights",
    default=config["darknet"]["weight_dir"],
    help="Darknet root directory",
)
def available(
    weight,
    root=config["darknet"]["root"],
    weight_url=config["weights"]["url_root"],
    weights=config["darknet"]["weight_dir"],
):
    import pydarknet

    darknet = pydarknet.darknet.Darknet(root=root, weight_dir=weights)

    cfgs = [
        ".".join(os.path.basename(cfg).split(".")[0:-1])
        for cfg in darknet.cfgs
    ]

    assert weight in cfgs
    url = weight_url + weight + ".weights"
    assert url_is_alive(url)
    print("# Copy and paste this. Still manumatic")
    print("cd {} && axel -n20 {}".format(weights, url))
