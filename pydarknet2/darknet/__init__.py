# -*- coding: utf-8 -*-
"""darknet module.

This is the docstring for the example.py module.  Modules names should
have short, all-lowercase names.  The module name may have underscores if
this improves readability.

Every module should have a docstring at the very top of the file.  The
module's docstring may extend over multiple lines.  If your docstring does
extend over multiple lines, the closing three quotation marks must be on
a line by itself, preferably preceded by a blank line.

"""

import glob
import os
import subprocess
import time

from ..config import config
from ..utils import chroot
from .exceptions import BuildException, CloneException


class Darknet(object):
    """Class for the darknet source directory."""

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

        Raises
        ------
        BadException
            Because you shouldn't have done that.


        Examples
        --------
        >>> from pydarknet.darknet import Darknet
        >>> dn = Darknet(root="/tmp/darknet")
        >>> dn.exists
        False
        >>> dn.clone()
        >>> dn.exists
        True

        >>> from pydarknet.darknet import Darknet
        >>> dn = Darknet()
        >>> dn.exists
        True
        >>> dn.build(gpu=True)
        """
        if root is None:
            root = config["darknet"]["root"]
        if weight_dir is None:
            weight_dir = config["darknet"]["weight_dir"]

        self.root = os.path.abspath(root)
        self.weight_dir = os.path.abspath(weight_dir)

    @property
    def cfg_dir(self):
        """Return darknet configuration directory."""
        return os.path.abspath(os.path.join(self.root, "cfg"))

    @property
    def cfgs(self):
        """Return the .cfg files."""
        files = glob.glob(os.path.join(self.cfg_dir, "*.cfg"))
        files.sort()
        return files

    @property
    def datas(self):
        """Return the .data files."""
        files = glob.glob(os.path.join(self.cfg_dir, "*.data"))
        return files

    @property
    def datasets(self):
        """Return the .dataset files."""
        files = glob.glob(os.path.join(self.cfg_dir, "*.dataset"))
        return files

    @property
    def exe(self):
        """Return path to the darknet binary."""
        return os.path.abspath(os.path.join(self.root, "darknet"))

    def clone(self, clone_url=None, force=False):
        """Clone darknet.

        Parameters
        ----------
        clone_url : bool
            Clone URL. [Default: {}]

        force : bool
            Force cloning darknet, even folder it exists. [Default: False]

        """.format(
            config["darknet"]["clone_url"]
        )
        if clone_url is None:
            clone_url = config["darknet"]["clone_url"]

        if os.path.isdir(self.root) and not force:
            raise CloneException(
                "{} already exists. Not forcing clone.".format(self.root)
            )

        if os.path.isdir(self.root) and force:
            import shutil
            try:
                shutil.rmtree(self.root)
            except FileNotFoundError:
                pass # yeah.
            except:
                raise

        cmd = [
            "git",
            "clone",
            "--recurse-submodules",
            "--depth",
            "1",
            clone_url,
            self.root,
        ]
        print("Starting clone ...", end="")
        self._clone_log=subprocess.check_output(cmd)
        print("... Done")
        return None

    @chroot
    def build(self, force=False, **kwargs):
        """Build darknet.

        Parameters
        ----------
        gpu : bool
            Build darknet with GPU support. [Default: False]

        cudnn : bool
            Build darknet with cudnn support. [Default: [gpu]]

        opencv : bool
            Build darknet with OpenCV support. [Default: False]

        openmp : bool
            Build darknet with OpenMP support. [Default: False]

        force : bool
            Force building darknet, even if it exists. [Default: False]

        Returns
        -------
        build_log: str
            Returns the output of running the make command.
        """
        # Check if the executable exists and it's not forcing a rebuild.
        if os.path.exists(self.exe) and not force:
            # Raise exception.
            raise BuildException("Executable exists and force flag not set")

        # Clean the output.
        out = subprocess.check_output(["make", "clean"])

        # venvs do things.
        if kwargs["gpu"]:
            os.environ["PATH"] = os.environ["PATH"]+os.pathsep+"/usr/local/cuda/bin"
        if kwargs["cudnn"]:
            if "LD_LIBRARY_PATH" in os.environ:
                os.environ["LD_LIBRARY_PATH"] = os.environ["LD_LIBRARY_PATH"]+os.pathsep+"/usr/local/cuda/lib64"
            else:
                os.environ["LD_LIBRARY_PATH"] = "/usr/local/cuda/lib64"

        # For each argument and its value
        for arg, value in kwargs.items():
            # If the value is set.
            if value:
                # Set the environment flag to 1.
                os.environ[arg.upper()] = "1"
            else:
                # Otherwise set the flag to 0.
                os.environ[arg.upper()] = "0"
        # Build darknet.
        print("Starting build (take a water break) ...", end="")
        out = subprocess.check_output(["make", "-j8"])
        print("... Done")
        # Assert that the binary was built.
        assert os.path.exists(self.exe)
        # Return the output as a string.
        self._clone_log=out.decode("UTF-8")
        return None

    @property
    def exists(self):
        """Check if the Darknet executable exists."""
        return os.path.exists(self.exe)

    @chroot
    def run(self, cmd, *args):
        """Run the given commands with darknet."""
        cmd_array = [self.exe, cmd, *args]
        t1 = time.time()
        out = subprocess.check_output(cmd_array, timeout=3600)
        t2 = time.time()
        return t2 - t1, out

    @property
    def weights(self):
        """Return all downloaded weights."""
        weights = glob.glob(os.path.join(self.weight_dir, "*.weights"))
        return weights

    def __repr__(self):
        """Return an ipython representation of Darknet."""
        return "Darknet<dir='{}', bin='{}'>".format(
            os.path.isdir(self.root), self.exists
        )


class Incantation(object):
    """Incantation pair.

    Conjure magic with a configuration and pretrained weights.
    """

    def __init__(self, weights, cfg=None, darknet=None):
        self.weights = os.path.abspath(weights)
        assert os.path.exists(weights)

        self.name = os.path.splitext(os.path.basename(self.weights))[0]
        self.root = os.path.abspath(
            os.path.join(os.path.dirname(weights), "..")
        )
        if cfg is None:
            self.cfg = os.path.join(
                self.root, "cfg", "{}.cfg".format(self.name)
            )
        else:
            self.cfg = cfg

        self.darknet = darknet

    def __repr__(self):
        """Representation of Incantation."""
        return "Incantation<spell={}, {}>".format(self.name, self.darknet)

    def cast(self, image):
        """Cast an image detection spell using the incantation."""
        image = os.path.abspath(image)
        assert os.path.exists(image)

        return self.darknet.run("detect", self.cfg, self.weights, image)
