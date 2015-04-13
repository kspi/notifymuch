#!/usr/bin/env python3
from setuptools import setup

setup(
    name="notifymuch",
    version="0.1",
    description="",
    long_description="",
    author="Kiprianas Spiridonovas",
    author_email="k.spiridonovas@gmail.com",
    url="",
    license="MPL",
    packages=['notifymuch'],
    scripts=["bin/notifymuch"],

    install_requires=[
        "pyxdg",
        "notmuch",
        "pygobject",
    ],
)
