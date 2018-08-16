#!/usr/bin/env python3

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='store_ops',
    version='0.1',
    author='Celso Providelo',
    author_email='celso.providelo@canonical.com',
    url="https://github.com/cprov/store_ops",
    license='LICENSE',
    description='Snap Store Operations.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        "surl",
    ],
    scripts=['store_ops.py'],
    packages=setuptools.find_packages(),
)
