# -*- coding: utf-8 -*-
"""libdarknet module.

Low level module for interacting with ```libdarknet.so``` static library.




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
from .structs import Detection, Image, Metadata


class Libdarknet(object):
    """Class for libdarknet.so shared library.

    If the class has public attributes, they may be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section. Alternatively, attributes may be documented
    inline with the attribute's declaration (see __init__ method below).

    Properties created with the ``@property`` decorator should be documented
    in the property's getter method.

    Attributes
    ----------
    root : str, optional
        Root directory for darknet. Default: ~/.darknet

    weight_dir : str, optional
        Description of `attr2`.

    Adapted From:
    https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html

    # Documentation is Attribution-NonCommercial-ShareAlike 4.0
    # International (CC BY-NC-SA 4.0)
    # Copyright (c) 2018, Jed Frey.
    """

    def __init__(self, root=None, weight_dir=None, shared_lib="libdarknet.so"):
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

        self.shared_lib = shared_lib

    @property
    def _lib(self):
        """Return path to the darknet shared library."""
        return os.path.abspath(os.path.join(self.root, self.shared_lib))

    @property
    def exists(self):
        """Determine if shared library exists."""
        return os.path.exists(self._lib)

    @cached_property
    def lib(self):
        """Return CDLL shared library."""
        lib_ = ctypes.CDLL(self._lib, ctypes.RTLD_GLOBAL)
        lib_.network_width.argtypes = [ctypes.c_void_p]
        lib_.network_width.restype = ctypes.c_int
        lib_.network_height.argtypes = [ctypes.c_void_p]
        lib_.network_height.restype = ctypes.c_int
        return lib_

    @chroot
    def get_metadata(self, path):
        """Get metadata from a path."""
        path = os.path.abspath(path)
        self.lib.get_metadata.argtypes = [ctypes.c_char_p]
        self.lib.get_metadata.restype = Metadata
        metadata_ = ctypes.c_char_p(path.encode("UTF-8"))
        metadata = self.lib.get_metadata(metadata_)
        return metadata

    @chroot
    def load_network(self, cfg_file, weight_file, clear=0):
        """Load a darknet network.

        Parameters
        ----------
        cfg_file : str
            Config file to load. Relative paths are relative to the
            darknet directory.
        weight_file : str
            Weight file to load. Relative paths are relative to the
            darknet directory.
        clear : int
            Clear network.

        Returns
        -------
        network_ptr: ctypes.c_void_p
            Pointer to the loaded network.
        """
        cfg_file = os.path.abspath(cfg_file)
        weight_file = os.path.abspath(weight_file)

        assert os.path.exists(cfg_file), "Configuration file not found."
        assert os.path.exists(weight_file), "Weight file not found."

        # Specify the shared library argument types.
        self.lib.load_network.argtypes = [
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_int,
        ]
        # Specify the shared library return type.
        self.lib.load_network.restype = ctypes.c_void_p

        # Cast the inputs to their ctypes.
        cfg_file_ = ctypes.c_char_p(cfg_file.encode("UTF-8"))
        weight_file_ = ctypes.c_char_p(weight_file.encode("UTF-8"))
        clear_ = ctypes.c_int(clear)
        # Return the output of load_network.
        return self.lib.load_network(cfg_file_, weight_file_, clear_)

    @chroot
    def load_image_color(self, path, width=0, height=0, colors=0):
        """Load an image from a path.

        Parameters
        ----------
        path : str
            Image file to load. Relative paths are relative to the
            darknet directory.
        width : int
            Image width
        height : int
            Image height.
        colors : int
            Number of image colors.

        Returns
        -------
        img : Image
            Loaded image structure.
        """
        path = os.path.abspath(path)

        assert os.path.exists(path)

        load_image_ = self.lib.load_image_color
        load_image_.argtypes = [
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
        ]
        load_image_.restype = Image

        path_ = ctypes.c_char_p(path.encode("UTF-8"))
        width_ = ctypes.c_int(width)
        height_ = ctypes.c_int(height)
        colors_ = ctypes.c_int(colors)

        img = load_image_(path_, width_, height_, colors_)
        return img

    @chroot
    def network_predict_image(self, network_ptr, image):
        """Load an image from a path.

        Parameters
        ----------
        network_ptr : ctypes.c_void_p
            Pointer to darknet network object.
        image: Image
            Darknet Image.

        Returns
        -------
        detections : Detections
            Loaded image structure.
        """
        self.lib.network_predict_image.argtypes = [ctypes.c_void_p, Image]
        self.lib.network_predict_image.restype = ctypes.POINTER(ctypes.c_float)
        return self.lib.network_predict_image(network_ptr, image)

    @chroot
    def get_network_boxes(
        self, network, image, threshold=0.5, heir_thresh=0.5
    ):
        """Get network boxes for a given image classified by network.

        Parameters
        ----------
        network : Network
            Pointer to darknet network object.
        image : Image
            Darknet Image object.
        height : int
            Image height.
        colors : int
            Number of image colors.

        Returns
        -------
        img : Image
            Loaded image structure.

        C Definition of ```get_network_boxes```
        get_network_boxes(
                network *net,
                int w,
                int h,
                float
                thresh,
                float hier,
                int *map,
                int relative,
                int *num)
        """
        # Alias C-function.
        get_network_boxes_ = self.lib.get_network_boxes

        # Argument and return types:
        get_network_boxes_.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.POINTER(ctypes.c_int),
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_int),
        ]
        get_network_boxes_.restype = ctypes.POINTER(Detection)

        # Create a number and pointer to that number for pass by ref.
        num = ctypes.c_int(0)
        pnum = ctypes.pointer(num)

        # Get the detections and
        dets = get_network_boxes_(
            network, image.w, image.h, threshold, heir_thresh, None, 0, pnum
        )

        return num.value, dets

    @chroot
    def get_labels(self, path):
        """Get labels from a path.

        Parameters
        ----------
        path : str
            Label file to load. Relative paths are relative to the
            darknet directory.

        Returns
        -------
        labels : ctypes.POINTER(ctypes.c_char_p)
            List of strings of labels.
        """
        path = os.path.abspath(path)

        assert os.path.exists(path), "Label file does not exist"

        get_labels_ = self.lib.get_labels
        # Set ctypes argument & return types.
        get_labels_.argtypes = [ctypes.c_char_p]
        get_labels_.restype = ctypes.POINTER(ctypes.c_char_p)

        path_ = ctypes.c_char_p(path.encode("UTF-8"))

        return get_labels_(path_)

    @chroot
    def do_nms_obj(self, dets, total, classes, thresh):
        """Do a nms obj.

        C Definition of ```do_nms_obj```
        void do_nms_obj(
            detection *dets,
            int total,
            int classes,
            float thresh);
        """
        self.lib.do_nms_obj.argtypes = [
            ctypes.POINTER(Detection),
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_float,
        ]
        self.lib.do_nms_obj.restype = None
        self.lib.do_nms_obj(dets, total, classes, thresh)
        return None

    @chroot
    def do_nms_sort(self, dets, total, classes, thresh):
        """Do a nms sort.

        C Definition of ```do_nms_sort```
        do_nms_sort(
            detection *dets,
            int total,
            int classes,
            float thresh);
        """
        self.lib.do_nms_sort.argtypes = [
            ctypes.POINTER(Detection),
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_float,
        ]
        self.lib.do_nms_sort.restype = None
        self.lib.do_nms_sort(dets, total, classes, thresh)
        return None

    @chroot
    def free_image(self, image):
        """Free image."""
        self.lib.free_image.argtypes = [Image]
        self.lib.free_image(image)

    @chroot
    def free_detections(self, dets, num):
        """Free Detections."""
        self.lib.free_detections.argtypes = [
            ctypes.POINTER(Detection),
            ctypes.c_int,
        ]
        self.lib.free_detections(dets, num)
