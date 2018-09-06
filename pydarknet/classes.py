# -*- coding: utf-8 -*-
"""Custom classes.

Custom classes to abstract away darknet bits.
"""

from cached_property import cached_property


class Detections(object):
    """High level class for all found detected objects.

    Attributes
    ----------
    num : int
        Numbed of detections.
    detections_ptr : ctypes.c_void_p
        Pointer to detection array from darknet.
    """

    def __init__(self, num, detections_ptr):
        r"""Initialize a Detections object.

        Parameters
        ----------
        num : int
            Numbed of detections.
        detections_ptr : ctypes.c_void_p
            Pointer to detection array from darknet.
        """
        self.num = num
        self.detections_ptr = detections_ptr

    def __repr__(self):
        """IPython pretty representation."""
        return "Detections<{}>".format(self.num)

    def __iter__(self):
        """__iter__ function for using Detections in a loop."""
        self._idx = 0
        return self

    def __next__(self):
        """__next__ function for using Detections in a loop."""
        idx = self._idx
        if self._idx >= self.num:
            raise StopIteration
        else:
            self._idx += 1
            return self.detections_ptr[idx]

    def __getitem__(self, index):
        """Return detection object at given index."""
        return self.detections_ptr[index]


class ClassifiedImage(object):
    """High level class for a classified image object.

    Attributes
    ----------
    classification : str
        Classification string.
    detection : Detection
        Detection structure from Darknet.
    image : Image
        Darknet Image object.
    """

    def __init__(self, classification, detection, image):
        self.classification = classification
        self.detection = detection
        self.image = image.asimage()

    @cached_property
    def crop(self):
        """Return the image cropped to the classified object."""
        return self.image.crop(self.crop_box)

    @property
    def crop_box(self):
        """Shorthand to the pil_crop_box."""
        return self.detection.bbox.pil_crop_box

    def __repr__(self):
        """Return ipython representation."""
        return "Classified<{}, {}>".format(self.classification, self.crop_box)
