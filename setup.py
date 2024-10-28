#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="ruter-api",
    version="0.1",
    packages=find_packages(),
    install_requires=["requests"],
    description="Python wrapper for the Ruter API",
    author="Mazunki Hoksaas",
    author_email="rolfern@gmail.com",
    url="https://github.com/mazunki/ruter-api",
)

