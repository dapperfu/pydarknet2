# -*- coding: utf-8 -*-
"""```pydarknet``` utilities module.

Generic utilities for use in ```pydarknet.```

"""

import ctypes
import os
import urllib.request
from functools import wraps

import numpy as np

from .libdarknet.structs import Image


# darknet gets angry if you don't use the darknet directory as 'root'.
def chroot(f):
    """Decorator to change current directory.

    darknet loads stuff relative to its directory. This decorator
    changes the current working directory to the Darknet or Libdarknet
    root directory before executing a function.
    """
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

def c_array(values, ctype=ctypes.c_float):
    """Return a ctypes array of values."""
    arr = (ctype * len(values))()
    arr[:] = values
    return arr

def array_to_image(arr):
    """Convert the array to a darknet Image.

    Parameters
    ----------
    array : numpy.array
        numpy array of image data.

    Returns
    -------
    img: Image
        Darknet image object.
    """
    arr = arr.transpose(2, 0, 1)
    c = arr.shape[0]
    h = arr.shape[1]
    w = arr.shape[2]
    arr = (arr.astype(np.float) / 255.0).flatten()
    data = c_array(arr)
    im = Image(w, h, c, data)
    return im


def url_is_alive(url):
    r"""Initialize a darknet object.

    Parameters
    ----------
    url : str
        URL to check.

    Returns
    -------
    alive: bool
        True if the URL does not return an error.
    """
    request = urllib.request.Request(url)
    request.get_method = lambda: "HEAD"
    try:
        urllib.request.urlopen(request)
        return True
    except urllib.request.HTTPError:
        return False
