#!/usr/bin/env python
# coding=utf8

"""
    安装依赖
"""
from setuptools import setup, find_packages

requires = [
    'Flask==0.10.1',
    'flask-script',
    'dbskit>=0.0.2',
    'webcrawl>=0.0.2'
    ]

setup(packages=find_packages(),
    install_requires=requires)
