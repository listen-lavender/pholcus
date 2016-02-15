#!/usr/bin/python
# coding=utf8
import json
from settings import withBase, withData, base, data, _BASE_R, _BASE_W, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g

monitor = Blueprint('monitor', __name__, template_folder='template')

from task import *
from data import *

@monitor.route('/index', methods=['GET'])
def index():
    return render_template('mindex.html', appname=g.appname, logined=True)