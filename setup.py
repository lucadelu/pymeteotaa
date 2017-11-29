#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 10:32:07 2017

@author: lucadelu
"""

from setuptools import setup, find_packages
import os
import re

NAME='pymeteotaa'
HERE = os.path.abspath(os.path.dirname(__file__))

with open('README') as f:
    README = f.read()

with open('LICENSE') as f:
    LICENSE = f.read()

with open(os.path.join(HERE, NAME, '__init__.py')) as fp:
        VERSION = re.search("__version__ = '([^']+)'", fp.read()).group(1)

setup(
    name=NAME,
    version=VERSION,
    description='Weather data from Trento and South Tyrol Province',
    long_description=README,
    author='Luca Delucchi',
    author_email='luca.delucchi@fmach.it',
    url='https://github.com/lucadelu/pymeteotaa',
    license=LICENSE,
    packages=find_packages(),
    install_requires=['requests', 'geojson'],
    classifiers=[
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)