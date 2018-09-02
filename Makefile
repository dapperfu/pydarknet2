VENV?=venv

.PHONY: all
all: ${VENV}

${VENV}:
	python3.6 -mvenv ${@}
	${@}/bin/pip install --upgrade setuptools wheel pip
	${@}/bin/pip install --upgrade jupyter notebook
	${@}/bin/pip install --editable .
