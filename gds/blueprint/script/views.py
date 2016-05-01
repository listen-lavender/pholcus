#!/usr/bin/env python
# coding=utf8
import json
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g

script = Blueprint('script', __name__, template_folder='template')

@monitor.route('/list', methods=['GET'])
def index():
    result = json.dumps({'code':1, 'msg':'', 'res':{'script':[]}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result