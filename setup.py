from datetime import datetime
from os import getenv

from setuptools import setup, find_packages


def requires():
    return open("requirements.txt").readlines()


dev = []

if getenv("ENVIRON") != "PROD":
    dev = ["pgmigrate", "pyresttest"]

setup(
    name='ResetAPP',
    version=datetime.now().strftime("%Y%m.01"),
    description='▌│█║▌║▌║ Rɘset app ║▌║▌║█│▌',
    author='lootbox',
    url='github.com/lootbox',
    packages=find_packages(exclude=("test*",)),
    include_package_data=True,
    install_requires=requires() + dev,
    zip_safe=False,
    test_suite='tests',
)
