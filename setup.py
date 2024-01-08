# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in kepin_loyalty/__init__.py
from kepin_loyalty import __version__ as version

setup(
	name="kepin_loyalty",
	version=version,
	description="Kepin Loyalty System",
	author="James Riady",
	author_email="jamesriady1998@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
