#!/usr/bin/python
# coding=utf8
import json
from datakit.mysql.suit import withMysql, dbpc, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template

from hawkeye import init

produce = Blueprint('produce', __name__, template_folder='templates')

from datamodel import *
from unit import *
from article import *
from section import *
from task import *

@withMysql(WDB, resutype='DICT', autocommit=True)
def codetree():
    init(dbpc)

codetree()

@produce.route('/index', methods=['GET'])
def index():
    return render_template('pindex.html')