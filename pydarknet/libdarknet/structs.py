# -*- coding: utf-8 -*-
"""Darknet ctypes structure typedefs."""

import ctypes

import numpy as np
import PIL


class BaseMixin(object):
    """Mixin for __repr__."""

    def __repr__(self):
        """Mixin __repr__."""
        return "{}<>".format(self.__class__.__name__)


class ArgumentArgs(ctypes.Structure, BaseMixin):
    """Argument Args."""

    _fields_ = [
        ("w", ctypes.c_int),
        ("h", ctypes.c_int),
        ("scale", ctypes.c_float),
        ("rad", ctypes.c_float),
        ("dx", ctypes.c_float),
        ("dy", ctypes.c_float),
        ("aspect", ctypes.c_float),
    ]


class UpdateArgs(ctypes.Structure, BaseMixin):
    """Update Args."""

    _fields_ = [
        ("batch", ctypes.c_int),
        ("learning_rate", ctypes.c_float),
        ("momentum", ctypes.c_float),
        ("decay", ctypes.c_float),
        ("adam", ctypes.c_int),
        ("B1", ctypes.c_float),
        ("B2", ctypes.c_float),
        ("eps", ctypes.c_float),
        ("t", ctypes.c_int),
    ]


class Image(ctypes.Structure):
    """Image structure."""

    _fields_ = [
        ("w", ctypes.c_int),
        ("h", ctypes.c_int),
        ("c", ctypes.c_int),
        ("float", ctypes.POINTER(ctypes.c_float)),
    ]

    def __repr__(self):
        """Return the size of the image."""
        return "{}<{}x{}x{}>".format(
            self.__class__.__name__, self.w, self.h, self.c
        )

    def __len__(self):
        """Return the length of the float array."""
        return self.w * self.h * self.c

    def asarray(self):
        """Return the image object as a numpy array."""
        # Pull all of the data out of the float 'into' a Python object.
        data = self.float[0:len(self)]
        # Multiply by 255 and change datatype.
        data_ = np.multiply(data, 255).astype(dtype=np.uint8)
        # Reshape the array into something.
        array_ = data_.reshape((self.c, self.h, self.w))
        # Un transpose it back to an image array.
        array = array_.transpose(1, 2, 0)
        return array

    def asimage(self):
        """Return the image as a PIL Image."""
        return PIL.Image.fromarray(self.asarray())


class Box(ctypes.Structure):
    """Box structure defines the coordinates of a detected object."""

    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("w", ctypes.c_float),
        ("h", ctypes.c_float),
    ]

    def __repr__(self):
        return "{}<{:.1f}, {:.1f}, {:.1f}, {:.1f}>".format(
            self.__class__.__name__, self.x, self.y, self.w, self.h
        )

    @property
    def left(self):
        """Left pixel for PIL cropping."""
        return self.x - self.w / 2

    @property
    def upper(self):
        """Upper pixel for PIL cropping."""
        return self.y - self.h / 2

    @property
    def right(self):
        """Right pixel for PIL cropping."""
        return self.x + self.w / 2

    @property
    def lower(self):
        """Lower pixel for PIL cropping."""
        return self.y + self.h / 2

    @property
    def pil_crop_box(self):
        """56"""
        return (self.left, self.upper, self.right, self.lower)


class Detection(ctypes.Structure, BaseMixin):
    """Detection structure."""

    _fields_ = [
        ("bbox", Box),
        ("classes", ctypes.c_int),
        ("prob", ctypes.POINTER(ctypes.c_float)),
        ("mask", ctypes.POINTER(ctypes.c_float)),
        ("objectness", ctypes.c_float),
        ("sort_class", ctypes.c_int),
    ]

    def __repr__(self):
        return "Detection<{}, {:.2f}>".format(self.bbox, self.objectness)


class Matrix(ctypes.Structure, BaseMixin):
    """Matrix structure."""

    _fields_ = [
        ("rows", ctypes.c_int),
        ("cols", ctypes.c_int),
        ("vals", ctypes.POINTER(ctypes.POINTER(ctypes.c_float))),
    ]


class Data(ctypes.Structure, BaseMixin):
    """Data structure."""

    _fields_ = [
        ("w", ctypes.c_int),
        ("h", ctypes.c_int),
        ("X", Matrix),
        ("y", Matrix),
        ("shallow", ctypes.c_int),
        ("num_boxes", ctypes.POINTER(ctypes.c_int)),
        ("box", ctypes.POINTER(ctypes.POINTER(Box))),
    ]


class Node(ctypes.Structure, BaseMixin):
    """Node structure."""

    pass


# Workaround because of self referencing.
Node._fields_ = [
    ("val", ctypes.c_void_p),
    ("next", ctypes.POINTER(Node)),
    ("prev", ctypes.POINTER(Node)),
]


class BoxLabel(ctypes.Structure, BaseMixin):
    """Box label structure."""

    _fields_ = [
        ("id", ctypes.c_int),
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("w", ctypes.c_float),
        ("h", ctypes.c_float),
        ("left", ctypes.c_float),
        ("right", ctypes.c_float),
        ("top", ctypes.c_float),
        ("bottom", ctypes.c_float),
    ]


class Tree(ctypes.Structure):
    """Tree structure."""

    _fields_ = [
        ("leaf", ctypes.POINTER(ctypes.c_int)),
        ("n", ctypes.c_int),
        ("parent", ctypes.POINTER(ctypes.c_int)),
        ("child", ctypes.POINTER(ctypes.c_int)),
        ("group", ctypes.POINTER(ctypes.c_int)),
        ("name", ctypes.POINTER(ctypes.c_char_p)),
        ("groups", ctypes.c_int),
        ("group_size", ctypes.POINTER(ctypes.c_int)),
        ("group_offset", ctypes.POINTER(ctypes.c_int)),
    ]

    def __repr__(self):
        """__repr__ function."""
        return "Tree<{}, {}>".format(self.n, self.groups)


class Metadata(ctypes.Structure):
    """Metadata structure."""

    _fields_ = [
        ("classes", ctypes.c_int),
        ("names", ctypes.POINTER(ctypes.c_char_p)),
    ]

    def __repr__(self):
        """__repr__ function for Metadata."""
        return "Metadata<{}>".format(len(self))

    def asgenerator(self):
        """Return the metadata classes as a generator."""
        for idx in range(self.classes):
            yield self.names[idx].decode("UTF-8")

    def aslist(self):
        """Return the metadata classes as a list."""
        return list(self.asgenerator())

    def __iter__(self):
        """__iter__ function to allow for looping."""
        self._idx = 0
        return self

    def __len__(self):
        """Return the number of classes for len(Metadata)."""
        return self.classes

    def __next__(self):
        """Get the next index point."""
        idx = self._idx
        if self._idx >= self.classes:
            raise StopIteration
        else:
            self._idx += 1
            return self[idx]

    def __getitem__(self, index):
        """Allow indexing of Metadata object."""
        assert index < self.classes, "Index out of range."
        return self.names[index].decode("UTF-8")
