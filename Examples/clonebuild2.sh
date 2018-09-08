#!/usr/bin/env bash

# Set the root path.
export DARKNET_ROOT=/tmp/darknet
# Remove if it exists
rm -rf ${DARKNET_ROOT}
# Clone
darknet.py darknet clone
# Build with OpenCV
darknet.py darknet build --opencv
