#!/usr/bin/env python
# coding=utf8
import json
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g

monitor = Blueprint('monitor', __name__, template_folder='template')

from task import *
from data import *
from activity import *
from runlog import *

@monitor.route('/index', methods=['GET'])
def index():
    return render_template('index.html', appname=g.appname, user=user)