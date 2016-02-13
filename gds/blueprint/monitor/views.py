#!/usr/bin/python
# coding=utf8
import json
from settings import withBase, withData, baseConn, dataConn, _BASE_R, _BASE_W
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g

monitor = Blueprint('monitor', __name__, template_folder='template')

from task import *

@monitor.route('/index', methods=['GET'])
def index():
    return render_template('mindex.html', appname=g.appname, logined=True)