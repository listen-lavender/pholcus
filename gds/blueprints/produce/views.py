#!/usr/bin/python
# coding=utf8
import json
from datakit.mysql.suit import withMysql, dbpc, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template

produce = Blueprint('produce', __name__, template_folder='templates')

from datamodel import *
from unit import *
from article import *
from section import *
from datasource import *
from dataextract import *

@produce.route('/index', methods=['GET'])
def index():
    return render_template('index.html')