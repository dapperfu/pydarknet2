#!/bin/sh

pycodestyle --statistics --max-line-length=79 $1
pydocstyle  --convention=numpy --verbose $1
