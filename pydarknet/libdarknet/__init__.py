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

from ..config import config

from functools import wraps
from ..config import config

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

class Libdarknet(object):
    """Class for the libdarknet shared library."""

    def __init__(self, root=None, weight_dir=None):
        r"""Initialize a darknet object.

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