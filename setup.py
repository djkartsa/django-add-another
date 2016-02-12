#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import codecs
import os

from setuptools import find_packages, setup


def read(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    return codecs.open(file_path, encoding='utf-8').read()


PACKAGE = "add_another"
NAME = "django-add-another"
DESCRIPTION = "'Add another' functionality outside Django admin"
AUTHOR = "Karim Amzil"
AUTHOR_EMAIL = "djkartsa@gmail.com"
URL = "https://github.com/djkartsa/django-add-another"
VERSION = __import__(PACKAGE).__version__


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read("README.md"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="LICENSE.txt",
    url=URL,
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Framework :: Django",
    ],
    install_requires=[
        'Django',
    ],
    zip_safe=False,
)
