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
from .classes import Detections
from cached_property import cached_property

from PIL import Image

__version__ = get_versions()["version"]
del get_versions

if sys.version_info[0] < 3:
    raise Exception("Python2. No. https://pythonclock.org/")

class Classifier(Libdarknet, object):
    """Classify an image."""

    def __init__(self, metadata_path, cfg_path, weights_path, **kwargs):
        super().__init__(**kwargs)
        self.metadata_path=metadata_path
        self.cfg_path=cfg_path
        self.weights_path=weights_path


    @cached_property
    def metadata(self):
        print("Loading metadata...", end="")
        m = self.get_metadata(self.metadata_path)
        print("...Done")
        return m

    @cached_property
    def network(self):
        print("Loading network...", end="")
        n = self.load_network(self.cfg_path, self.weights_path, 0)
        print("...Done")
        return n


    def detect(self, image_path, nms=0.5):
        img = self.load_image_color(image_path)
        self.network_predict_image(self.network, img)

        num, detections_ptr = self.get_network_boxes(self.network, img)
        dets = Detections(num, detections_ptr)

        self.free_image(img)

        self.do_nms_sort(detections_ptr, num, self.metadata.classes, nms);

        res = []
        for det in dets:
            assert det.classes == self.metadata.classes
            for i in range(self.metadata.classes):
                if det.prob[i] > 0:
                    b = det.bbox
                    res.append((self.metadata.names[i].decode(), det.prob[i], (b.left, b.upper, b.right, b.lower)))
        return res

    def __repr__(self):
        return "Classifier<{}, {}, {}>".format(self.metadata_path, self.cfg_path, self.weights_path)

