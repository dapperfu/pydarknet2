#!/usr/bin/env bash

# Clone
darknet.py darknet clone
# Build with OpenCV, OpenMP, GPU and cudNN support.
darknet.py darknet build --opencv --openmp --gpu --cudnn
