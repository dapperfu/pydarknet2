# pydarknet

pydarknet is a Python module for [Darknet, an open source neural network framework written in C and CUDA. It is fast, easy to install, and supports CPU and GPU computation](https://pjreddie.com/darknet/).

# Installation

In a virtual environment:

	python3 -mvenv venv
	source venv/bin/activate
	pip install git+https://github.com/jed-frey/pydarknet.git#egg=pydarknet


# Motivation

- I want to do image detection for my 2TB+ of photos I've taken.
- Darknet provided the best 'batteries included' tutorial, with weights.
- The Python examples were Python2 and ... lacking.
