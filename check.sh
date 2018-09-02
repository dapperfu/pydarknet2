#!/bin/sh

flake8 --statistics --count "$1"
pycodestyle --statistics --max-line-length=79 "$1"
pydocstyle  --convention=numpy --verbose "$1"
