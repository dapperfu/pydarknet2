#!/bin/sh

# Fix all files in a given directory (and below)

# Not ready.
find pydarknet -name "*.py" | xargs -n1 -P8 ./fix.sh
exit 0
