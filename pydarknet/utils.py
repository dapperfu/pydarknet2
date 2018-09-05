# -*- coding: utf-8 -*-
"""Ipsum"""

import ctypes
import os
from functools import wraps

import numpy as np

from .libdarknet.structs import Image


# darknet gets angry if you don't use the darknet directory as 'root'.
def chroot(f):
    """Changeroot for functions to keep darknet happy."""

    @wraps(f)
    def wrapper(self, *args, **kwargs):
        """Wrap Function."""
        # Get the 'current' directory to the rest of Python.
        lwd = os.path.abspath(os.path.curdir)
        # Change root to the root directory of darknet.
        os.chdir(self.root)
        # Execute the function that got wrapped.
        ret = f(self, *args, **kwargs)
        # Change back to the 'last' working directory.
        os.chdir(lwd)
        # Return the function's output.
        return ret

    return wrapper


# Weight Downloader
def get_weight(network):
    pass


def c_array(values, ctype=ctypes.c_float):
    arr = (ctype * len(values))()
    arr[:] = values
    return arr


def array_to_image(arr):
    arr = arr.transpose(2, 0, 1)
    c = arr.shape[0]
    h = arr.shape[1]
    w = arr.shape[2]
    arr = (astype(np.float) / 255.0).flatten()
    data = c_array(dn.c_float, arr)
    im = Image(w, h, c, data)
    return im

def from(image):
    img_ = np.asarray(image, dtype=np.uint8)
    return array_to_image(img_)
