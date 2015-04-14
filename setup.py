#!/usr/bin/env python3
from setuptools import setup


def readme():
    with open("README.rst", "r") as f:
        return f.read()


setup(
    name="notifymuch",
    version="0.1",
    description="Display desktop notifications for unread mail in notmuch "
                "database",
    long_description=readme(),
    author="Kiprianas Spiridonovas",
    author_email="k.spiridonovas@gmail.com",
    url="https://github.com/kspi/notifymuch",
    license="GPL3",
    packages=['notifymuch'],
    scripts=["bin/notifymuch"],

    install_requires=[
        "pyxdg",
        "notmuch",
        "pygobject",
    ],
)
