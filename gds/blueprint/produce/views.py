#!/usr/bin/python
# coding=utf8
import json
from settings import withBase, withData, baseConn, dataConn, _BASE_R, _BASE_W
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g

from hawkeye import init

produce = Blueprint('produce', __name__, template_folder='template')

from datamodel import *
from unit import *
from article import *
from section import *
from task import *

@withMysql(WDB, resutype='DICT', autocommit=True)
def codetree():
    init(baseConn)

codetree()

@produce.route('/index', methods=['GET'])
def index():
    return render_template('pindex.html', appname=g.appname, logined=True)