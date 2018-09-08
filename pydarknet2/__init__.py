# -*- coding: utf-8 -*-
"""pydarknet: summon darknet from Python.

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

from ._version import get_versions
from .classes import ClassifiedImage, Detections
from .darknet import Darknet
from .libdarknet import Libdarknet
from .libdarknet.structs import Image
from .utils import array_to_image

# Versioneer version.
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

    def __del__(self):
        """Object deletion cleanup."""
        pass

    @cached_property
    def metadata(self):
        """Return metadata object at ```metadata_path```."""
        print("Loading metadata...", end="")
        m = self.get_metadata(self.metadata_path)
        print("...Done")
        return m

    @cached_property
    def network(self):
        """Return network object specified class attributes."""
        print("Loading network...", end="")
        n = self.load_network(self.cfg_path, self.weights_path, 0)
        print("...Done")
        return n

    def load(self, cfg_path=None, weights_path=None, metadata_path=None):
        """Explicitly load the network with a function call."""
        if cfg_path is not None:
            self.cfg_path=cfg_path
        if weights_path is not None:
            self.weights_path=weights_path
        if metadata_path is not None:
            self.metadata_path = metadata_path
        _ = self.metadata
        _ = self.network

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
            Return a list of ClassifiedImage objects.
        """
        # Convert the passed in image variable to a darknet Image
        if isinstance(image, Image):
            img = image
        elif isinstance(image, str):
            img = self.load_image_color(image)
        else:
            img = array_to_image(np.asarray(image))

        # Use the network to predict image object.
        self.network_predict_image(self.network, img)

        # Get the number of detected objects and a pointer to the
        # detection array.
        num, detections_ptr = self.get_network_boxes(self.network, img)

        # Do a nms sort.
        self.do_nms_sort(detections_ptr, num, self.metadata.classes, nms)

        # Construct a detections object from the result.
        dets = Detections(num, detections_ptr)

        # Empty list for results.
        res = []
        # For each detected object in the detection objects.
        for det in dets:
            # Ensure that the number of detected classes is the same
            # as in the metadata file.
            assert det.classes == self.metadata.classes
            # For each number of metadata classes.
            for i in range(self.metadata.classes):
                # If the probability of the detection for the given
                # classification is greater than 0.
                if det.prob[i] > 0:
                    # Add it to the list of results.
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

    # TODO: Allow with:
    def __enter__(self, *args, **kwargs):
        for idx, arg in enumerate(args):
            print("{}: {}".format(idx,arg))

        for arg, value in kwargs.items():
            print("{}: {}".format(arg,value))

        print("__enter__")

    def __exit__(self, *args, **kwargs):
        for idx, arg in enumerate(args):
            print("{}: {}".format(idx,arg))

        for arg, value in kwargs.items():
            print("{}: {}".format(arg,value))
        print("__exit__")
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
