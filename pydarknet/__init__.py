# -*- coding: utf-8 -*-
"""pydarknet summon darknet from Python.

This is the docstring for the example.py module.  Modules names should
have short, all-lowercase names.  The module name may have underscores if
this improves readability.

Every module should have a docstring at the very top of the file.  The
module's docstring may extend over multiple lines.  If your docstring does
extend over multiple lines, the closing three quotation marks must be on
a line by itself, preferably preceded by a blank line.

"""

import sys

from ._version import get_versions
from .darknet import Darknet
from .libdarknet import Libdarknet

from cached_property import cached_property

__version__ = get_versions()["version"]
del get_versions


if sys.version_info[0] < 3:
    raise Exception("Python2. No. https://pythonclock.org/")

from cac

class Classifier(Libdarknet, object):
    """Classify an image."""

    def __init__(self, metadata_path, cfg_path, weights_path, **kwargs):
        super().__init__(**kwargs)
        self.metadata_path=metadata
        self.network=network



    def detect(self, image):
