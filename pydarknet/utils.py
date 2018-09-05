# -*- coding: utf-8 -*-
"""Ipsum"""

import os
from functools import wraps


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
