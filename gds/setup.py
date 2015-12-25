#!/usr/bin/python
# coding=utf8

"""
    安装依赖
"""
from setuptools import setup, find_packages

requires = [
    'datakit',
    'flask-script',
    'flask-sqlalchemy',
    'datakit',
    'webcrawl'
    ]

setup(packages=find_packages(),
    install_requires=requires)
