#!/usr/bin/python
# coding=utf8
import json
from model.setting import withBase, withData, base, data, _BASE_R, _BASE_W, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g

from hawkeye import init

produce = Blueprint('produce', __name__, template_folder='template')

from datamodel import *
from unit import *
from article import *
from section import *
from task import *

@withBase(WDB, resutype='DICT', autocommit=True)
def codetree():
    # init(baseConn)
    pass

codetree()

@produce.route('/index', methods=['GET'])
def index():
    return render_template('index.html', appname=g.appname, user=user)