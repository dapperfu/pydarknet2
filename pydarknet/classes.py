from cached_property import cached_property


class Detections(object):
    def __init__(self, num, detections_ptr):
        self.num = num
        self.detections_ptr = detections_ptr

    def __repr__(self):
        return "Detections<{}>".format(self.num)

    def __iter__(self):
        self._idx = 0
        return self

    def __next__(self):
        idx = self._idx
        if self._idx >= self.num:
            raise StopIteration
        else:
            self._idx += 1
            return self.detections_ptr[idx]

    def __getitem__(self, index):
        return self.detections_ptr[index]


class ClassifiedImage(object):
    def __init__(self, classification, detection, image):
        self.classification = classification
        self.detection = detection
        self.image = image.asimage()

    @cached_property
    def crop(self):
        return self.image.asimage().crop(self.crop_box)

    @property
    def crop_box(self):
        return self.detection.bbox.pil_crop_box

    def __repr__(self):
        return "Classified<{}, {}>".format(self.classification, self.crop_box)
