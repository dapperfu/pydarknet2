#!/bin/sh
#autopep8 --in-place --max-line-length 79 \
#	 --aggressive --aggressive --aggressive $1
black --py36 --line-length=79 $1
isort --line-width 79 --multi-line 3 --dont-skip __init__.py $1

COMMIT_MSG="`whoami`@`hostname`: `date --universal`"
echo
echo --- Committing ${COMMIT_MSG}  ---
echo
git commit --all --message "${COMMIT_MSG}"
