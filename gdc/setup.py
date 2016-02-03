#!/usr/bin/python
# coding=utf8

"""
    安装依赖
"""
from setuptools import setup, find_packages

requires = [
    'dbskit',
    'webcrawl'
    ]

setup(packages=find_packages(),
    install_requires=requires)
