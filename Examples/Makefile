IPYNBS=$(wildcard *.ipynb)
PDFS=$(patsubst %.ipynb,%.pdf, ${IPYNBS})


.PHONY: debug
debug:
	$(info $${IPYNBS}=${IPYNBS})
	$(info $${PDFS}=${PDFS})

.PHONY: pdfs
pdfs: ${PDFS}

%.pdf: %.ipynb
	jupyter-nbconvert --config jupyter.cfg.py ${^}
