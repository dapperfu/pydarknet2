# -*- coding: utf-8 -*-
"""Module for the ```darknet.py``` command line interface.

An entrypoint for ```pydarknet2``` module.
"""

import os

import click

import pydarknet2

from .config import config
from .utils import url_is_alive


@click.group()
@click.version_option()
def cli():
    """```pydarknet2``` command line interface entry point.

    darknet.py is a utility for interacting with pydarknet from the
    command line.
    """


@cli.group("darknet")
def darknet():
    """Manage darknet folder."""


@darknet.command("clone")
@click.option(
    "--url",
    metavar="url",
    default=config["darknet"]["clone_url"],
    help="Darknet clone url. [Default: {}]".format(
        config["darknet"]["clone_url"]),
)
@click.option(
    "--root",
    metavar="root",
    default=config["darknet"]["root"],
    help="Darknet root directory. [Default: {}]".format(
        config["darknet"]["root"]),
)
def clone(
    root=config["darknet"]["root"],
    url=config["darknet"]["clone_url"],
    force=False,
):
    """Clone a darknet repository."""
    click.echo("URL: %s" % url)
    click.echo("Root: %s" % root)
    darknet = pydarknet2.Darknet(root=root)
    darknet.clone(clone_url=url, force=force)


@darknet.command("build")
@click.option(
    "--root",
    metavar="root",
    default=config["darknet"]["root"],
    help="Darknet root directory. [Default: {}]".format(
        config["darknet"]["root"])
)
@click.option("--gpu", is_flag=True, help="Compile with GPU support.")
@click.option("--cudnn", is_flag=True, help="Compile with cudnn support.")
@click.option("--opencv", is_flag=True, help="Compile with OpenCV support.")
@click.option("--openmp", is_flag=True, help="Compile with OpenMP support.")
@click.option("--force", is_flag=True, help="Do it.")
def build(gpu, cudnn, opencv, openmp, force, root):
    """Build darknet."""
    darknet = pydarknet2.Darknet(root=root)
    darknet.build(
        gpu=gpu, cudnn=cudnn, opencv=opencv, openmp=openmp, force=force
    )


@cli.group("weights")
def weights():
    """Manage darknet weights."""


@weights.command("list")
@click.option(
    "--root",
    metavar="root",
    default=config["darknet"]["root"],
    help="Darknet root directory. [Default: {}]".format(
        config["darknet"]["root"]),
)
@click.option(
    "--weights",
    metavar="weights",
    default=config["darknet"]["weight_dir"],
    help="Darknet weights directory [Default: {}]".format(
        config["darknet"]["weight_dir"]
    ),
)
def list_weights(
    root=config["darknet"]["root"], weights=config["darknet"]["weight_dir"]
):
    """List weights in weights directory."""
    darknet = pydarknet2.Darknet(root=root, weight_dir=weights)
    for weight in darknet.weights:
        print(weight)


@weights.command("available")
@click.option(
    "--root",
    metavar="root",
    default=config["darknet"]["root"],
    help="Darknet root directory. [Default: {}]".format(
        config["darknet"]["root"]),
)
@click.option(
    "--weight_url",
    metavar="weight_url",
    default=config["weights"]["url_root"],
    help="Pretrained weights url base. [Default: {}]".format(
        config["weights"]["url_root"]),
)
def available(
    root=config["darknet"]["root"], weight_url=config["weights"]["url_root"]
):
    """Display a list of available weights."""
    darknet = pydarknet2.darknet.Darknet(root=root)
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
    help="Darknet root directory. [Default: {}]".format(
        config["darknet"]["root"]),
)
@click.option(
    "--weight_url",
    metavar="weight_url",
    default=config["weights"]["url_root"],
    help="Pretrained weights url base. [Default: {}]".format(
        config["weights"]["url_root"]),
)
@click.option(
    "--weights",
    metavar="weights",
    default=config["darknet"]["weight_dir"],
    help="Pretrained weights directory. [Default: {}]".format(
        config["darknet"]["weight_dir"]),
)
def download(
    weight,
    root=config["darknet"]["root"],
    weight_url=config["weights"]["url_root"],
    weights=config["darknet"]["weight_dir"],
):
    """Print command to download weight."""
    darknet = pydarknet2.darknet.Darknet(root=root, weight_dir=weights)

    cfgs = [
        ".".join(os.path.basename(cfg).split(".")[0:-1])
        for cfg in darknet.cfgs
    ]
    assert weight in cfgs
    url = weight_url + weight + ".weights"
    referer = weight_url + "index.html"
    weight_file = os.path.join(weights, weight+".weights")
    assert url_is_alive(url)

    if not os.path.exists(weights):
        os.makedirs(weights)
    print("# Copy and paste this. Still manumatic")
    print("curl --referer {} --progress-bar --location --output {} {}".format(referer, weight_file, url))
