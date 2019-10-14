#coding:utf-8

from os import path
from codecs import open
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = "Laka",
    version = "0.1.2",
    author = "Gaojian",
    license = "MIT",
    packages = ["laka"],
    author_email = "olivetree123@163.com",
    url = "https://github.com/olivetree123/Laka",
    description = "Micro Service Framework for Python",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    install_requires = [
        "redis",
    ],
)
