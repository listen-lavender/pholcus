#!/usr/bin/env python
# coding=utf8
import json
from model.setting import withBase, basecfg
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g

task = Blueprint('task', __name__, template_folder='template')

from activity import *

@task.route('/<_id>', methods=['GET'])
def task_detail(_id):
    result = json.dumps({'code':1, 'msg':'', 'res':{'task':[]}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result