#!/usr/bin/env python
# coding=utf8
import json
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g

api = Blueprint('api', __name__)

def format_datetime(one):
    if 'create_time' in one:
        one['create_time'] = one['create_time'].strftime('%Y-%m-%d %H:%M:%S')
    if 'update_time' in one:
        one['update_time'] = one['update_time'].strftime('%Y-%m-%d %H:%M:%S')
    return one

from datamodel import *
from unit import *
from article import *
from section import *
from task import *
from config import *