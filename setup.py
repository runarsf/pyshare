# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

import re
import os
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('pyshare/pyshare.py').read(),
    re.M
    ).group(1)

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pyshare",
    packages = ["pyshare"],
    entry_points = {
        "console_scripts": ['pyshare = pyshare.pyshare:main']
	},
    version = version,
    description = ("A terminal based file uploader."),
    long_description=read('README.rst'),
    author = "runarsf",
    author_email = "runarsf@protonmail.com",
    url = "https://github.com/runarsf/pyshare",

    keywords = "open-source",
    license = "GPLv3",
    # https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: End Users/Desktop"
    ],
)

