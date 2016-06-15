#!/usr/bin/env python
# coding=utf8
from flask import Blueprint

running = Blueprint('running', __name__)

from snapshot import *
