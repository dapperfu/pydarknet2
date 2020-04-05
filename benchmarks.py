#!/usr/bin/env python3
import glob
import os
import sys
import time

import imageio
import PIL.Image

import pydarknet2


def benchmark_classifier(shared_lib):
    classifier = pydarknet2.Classifier(
        "cfg/coco.data",
        "cfg/yolov3.cfg",
        "weights/yolov3.weights",
        root=darknet_root,
        shared_lib=os.path.basename(shared_lib),
    )
    t1 = time.time()
    classifier.load()
    t2 = time.time()
    load_time = t2 - t1

    dog_path = os.path.join(classifier.root, "data/dog.jpg")

    t1 = time.time()
    objs = classifier.detect(dog_path)
    t2 = time.time()
    assert len(objs) == 3, "Inconnect number of identified objects."
    identify_time = t2 - t1

    return load_time, identify_time


def benchmark_wrapper(shared_lib):
    shared_lib_ = os.path.basename(shared_lib)
    load_time, identify_time = benchmark_classifier(shared_lib=shared_lib)
    try:
        _, compiler, version, opencv, openmp, gpu = shared_lib_.split(".")[0].split("-")
    except:
        compiler, version, opencv, openmp, gpu = "0", "0", "0", "0", "0"

    with open("results.csv", "a") as fid:
        result_list = [
            shared_lib_,
            compiler,
            version,
            opencv,
            openmp,
            gpu,
            str(load_time),
            str(identify_time),
        ]
        print(",".join(result_list), file=fid)


if __name__ == "__main__":
    darknet_root = "/tmp/darknet"
    shared_libs = glob.glob(os.path.join(darknet_root, "libdarknet-*-0.so"))
    for shared_lib in shared_libs:
        benchmark_wrapper(shared_lib)
