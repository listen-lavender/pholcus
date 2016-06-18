#!/usr/bin/env python
# coding=utf8

"""
    安装依赖
"""
from setuptools import setup, find_packages

requires = [
    'dbskit>=0.0.2',
    'webcrawl>=0.0.2'
    ]

setup(packages=find_packages(),
    install_requires=requires)
