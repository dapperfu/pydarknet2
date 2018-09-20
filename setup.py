import os
import sys

from setuptools import find_packages, setup

import versioneer

LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))

def read_requirements(path="requirements.txt"):
    """Read requirements file relative to setup.py"""
    full_path = os.path.join(LOCAL_DIR, path)
    def yield_line(path):
        with open(path, "r") as fid:
            for line in fid.readlines():
                yield line

    return [requirement.strip() for requirement in yield_line(full_path) if not requirement.startswith("#")]

requirements = read_requirements()
test_requirements = read_requirements(path="requirements_test.txt")

setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    name="pydarknet2",
    url="https://github.com/jed-frey/pydarknet2",
    author="Jed Frey",
    description="Python module for DarkNet, Too",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'darknet.py = pydarknet2.cli:cli',
        ],
    },
    extras_require={"test": test_requirements},
    include_package_data=True,
)
