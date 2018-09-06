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

import numpy as np
from cached_property import cached_property
from PIL import Image

from ._version import get_versions
from .classes import ClassifiedImage, Detections
from .darknet import Darknet
from .libdarknet import Libdarknet
from .libdarknet.structs import Image
from .utils import array_to_image

__version__ = get_versions()["version"]
del get_versions

if sys.version_info[0] < 3:
    raise Exception("Python2. No. https://pythonclock.org/")


class Classifier(Libdarknet, object):
    """High level wrapper for detecting objects in an image.

    Abstraction layer on top of ```Libdarknet``` object to classify
    images from python.

    Attributes
    ----------
    metadata_path : str
        Path to metadata.
    cfg_path : str
        Path to darknet cfg file.
    weights_path : str
        Path to pretrained weights.
    """
    def __init__(self, metadata_path, cfg_path, weights_path, **kwargs):
        r"""Initialize a libdarknet object.

        Parameters
        ----------
        metadata_path : str
            Path to metadata.
        cfg_path : str
            Path to darknet cfg file.
        weights_path : str
            Path to pretrained weights.

        """
        # Pass any extra keyword arguments into the Libdarknet init.
        super().__init__(**kwargs)
        # Assign attributes.
        self.metadata_path = metadata_path
        self.cfg_path = cfg_path
        self.weights_path = weights_path

    @cached_property
    def metadata(self):
        """ Property pointing to the configured metadata."""
        print("Loading metadata...", end="")
        m = self.get_metadata(self.metadata_path)
        print("...Done")
        return m

    @cached_property
    def network(self):
        """ Property pointing to the configured network."""
        print("Loading network...", end="")
        n = self.load_network(self.cfg_path, self.weights_path, 0)
        print("...Done")
        return n

    def detect(self, image, nms=0.5):
        """Detect objects in image.

        Parameters
        ----------
        image : str, Image, PIL.Image, numpy array
            Image file to detect objects in.
        nms : float
            See darknet documentation.

        Returns
        -------
        detections : list of ClassifiedImages
            Return a list of classified images.
        """
        if isinstance(image, Image):
            img = image
        elif isinstance(image, str):
            img = self.load_image_color(image)
        else:
            img = array_to_image(np.asarray(image))

        self.network_predict_image(self.network, img)

        num, detections_ptr = self.get_network_boxes(self.network, img)
        dets = Detections(num, detections_ptr)

        self.do_nms_sort(detections_ptr, num, self.metadata.classes, nms)

        res = []
        for det in dets:
            assert det.classes == self.metadata.classes
            for i in range(self.metadata.classes):
                if det.prob[i] > 0:
                    res.append(
                        ClassifiedImage(
                            self.metadata.names[i].decode(), det, img
                        )
                    )
        return res

    def __repr__(self):
        """Return a representation of the Classifier object."""
        return "Classifier<{}, {}, {}>".format(
            self.metadata_path, self.cfg_path, self.weights_path
        )
