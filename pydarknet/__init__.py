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

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

"""
    @cached_property
    def lib(self):
        lib_ = ctypes.CDLL(self.lib_path, ctypes.RTLD_GLOBAL)
        lib_.network_width.argtypes = [ctypes.c_void_p]
        lib_.network_width.restype = ctypes.c_int
        lib_.network_height.argtypes = [ctypes.c_void_p]
        lib_.network_height.restype = ctypes.c_int
        return lib_"""
