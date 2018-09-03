# -*- coding: utf-8 -*-
"""libdarknet module.

This is the docstring for the example.py module.  Modules names should
have short, all-lowercase names.  The module name may have underscores if
this improves readability.

Every module should have a docstring at the very top of the file.  The
module's docstring may extend over multiple lines.  If your docstring does
extend over multiple lines, the closing three quotation marks must be on
a line by itself, preferably preceded by a blank line.

"""

import ctypes
import os

from cached_property import cached_property

from ..config import config
from ..utils import chroot
from .structs import Metadata


class Libdarknet(object):
    """Class for the libdarknet shared library.
    """

    def __init__(self, root=None, weight_dir=None):
        r"""Initialize a libdarknet object.

        Parameters
        ----------
        var1 : array_like
            Array_like means all those objects -- lists, nested lists, etc. --
            that can be converted to an array.  We can also refer to
            variables like `var1`.
        var2 : int
            The type above can either refer to an actual Python type
            (e.g. ``int``), or describe the type of the variable in more
            detail, e.g. ``(N,) ndarray`` or ``array_like``.
        long_var_name : {'hi', 'ho'}, optional
            Choices in brackets, default first when optional.

        """
        if root is None:
            root = config["darknet"]["root"]
        if weight_dir is None:
            weight_dir = config["darknet"]["weight_dir"]

        self.root = os.path.abspath(root)
        self.weight_dir = os.path.abspath(weight_dir)

    @property
    def _lib(self):
        """Return path to the darknet binary."""
        return os.path.abspath(os.path.join(self.root, "libdarknet.so"))

    @property
    def exists(self):
        """Determine if library exists"""
        return os.path.exists(self._lib)

    @cached_property
    def lib(self):
        lib_ = ctypes.CDLL(self._lib, ctypes.RTLD_GLOBAL)
        lib_.network_width.argtypes = [ctypes.c_void_p]
        lib_.network_width.restype = ctypes.c_int
        lib_.network_height.argtypes = [ctypes.c_void_p]
        lib_.network_height.restype = ctypes.c_int
        return lib_

    @chroot
    def get_metadata(self, path):
        path = os.path.abspath(path)
        self.lib.get_metadata.argtypes = [ctypes.c_char_p]
        self.lib.get_metadata.restype = Metadata
        metadata_=ctypes.c_char_p(path.encode("UTF-8"))
        metadata = self.lib.get_metadata(metadata_)
        return metadata

    @chroot
    def load_network(self, cfg_file, weight_file, clear=0):
        cfg_file=os.path.abspath(cfg_file)
        weight_file=os.path.abspath(weight_file)

        self.lib.load_network.argtypes = [
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_int,
        ]
        self.lib.load_network.restype = ctypes.c_void_p

        cfg_file_=ctypes.c_char_p(cfg_file.encode("UTF-8"))
        weight_file_=ctypes.c_char_p(weight_file.encode("UTF-8"))
        clear_=ctypes.c_int(clear)
        self.network = self.lib.load_network(cfg_file_, weight_file_, clear_)