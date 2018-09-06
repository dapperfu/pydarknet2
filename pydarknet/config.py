# -*- coding: utf-8 -*-
"""pydarknet configuration options.


"""

"""Configuration."""
import configparser
import os

"""Default settings."""
default_darknet_root = os.path.expanduser(os.path.join("~", ".darknet"))
default_darknet_weight_dir = os.path.join(default_darknet_root, "weights")
default_darknet_clone_url = "https://github.com/jed-frey/darknet.git"
default_darknet_weight_url = "https://pjreddie.com/media/files/"

config = configparser.ConfigParser()

config["darknet"] = dict()
config["weights"] = dict()

config["darknet"]["root"] = os.environ.get(
    key="DARKNET_ROOT", default=default_darknet_root
)
config["darknet"]["clone_url"] = os.environ.get(
    key="DARKNET_CLONE_URL", default=default_darknet_clone_url
)
config["darknet"]["weight_dir"] = os.environ.get(
    key="DARKNET_WEIGHT_DIR", default=default_darknet_weight_dir
)
config["weights"]["url_root"] = os.environ.get(
    key="DARKNET_WEIGHT_URL", default=default_darknet_weight_url
)
