# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('rester/rester.py').read(),
    re.M
    ).group(1)


with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name="rester-http",
    packages=["rester"],
    entry_points={
        "console_scripts": ['rester = rester.rester:main']
        },
    version=version,
    description="HTTP client library and command line tool.",
    long_description=long_descr,
    author="PJ Dietz",
    author_email="pjdietz@gmail.com",
    url="https://github.com/pjdietz/rester",
    )
