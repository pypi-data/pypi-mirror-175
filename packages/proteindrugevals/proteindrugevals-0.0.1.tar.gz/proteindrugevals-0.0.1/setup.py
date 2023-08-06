#!/usr/bin/env python
# coding=utf-8

from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
    name='proteindrugevals',
    version='0.0.1',
    description=(
        'drug evalutions from QHGG'
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='QHGG',
    author_email='qhonearth@sjtu.edu.cn',
    maintainer='QHGG',
    maintainer_email='qhonearth@sjtu.edu.cn',
    license='MIT License',
    packages=find_packages(),
    # packages=['common'],
    platforms=["all"],
    url='https://gitlab.com/BL-Lac149597870/drug_tools',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries'
    ],
)

