#!/usr/bin/env python
# coding=utf8
import os
import json
import time, datetime
from model.setting import withBase, basecfg
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from rest import api, format_datetime
from model.base import Unit, Creator
from model.log import Logsummary
from . import exepath, allowed

INIT = """#!/usr/bin/env python
# coding=utf-8
"""

@api.route('/unit', methods=['POST'])
@api.route('/unit/<uid>', methods=['POST'])
@withBase(basecfg.W, resutype='DICT', autocommit=True)
def unit(uid=None):
    user = request.user
    condition = request.form.get('condition', '{}')
    condition = json.loads(condition)
    data = request.form.get('data', '{}')
    data = json.loads(data)
    pyfile = request.files.get('file')
    projection = request.form.get('projection', '{}')
    projection = json.loads(projection)

    limit = request.form.get('limit', 'one')

    if uid is not None:
        condition['_id'] = uid
    POST = False
    if pyfile:
        POST = True
        result = {'stat':0, 'desc':'请上传正确格式的python文件', 'datamodel':''}
        if pyfile and allowed(pyfile.filename):
            filename = pyfile.filename
            filepath = exepath(filename)
            pyfile.save(filepath)
            filepath = os.path.join(os.path.dirname(filepath), '__init__.py')
            if not os.path.exists(filepath):
                fi = open(filepath, 'w')
                fi.write(INIT)
                fi.close()
            result['stat'] = 1
            result['desc'] = '上传成功'
        result = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    if data:
        POST = True
        data['updator'] = user['_id']
        if '_id' in condition:
            Unit.update(condition, data)
            uid = condition['_id']
        else:
            data['creator'] = user['_id']
            data = Unit(**data)
            uid = Unit.insert(data)
        result = json.dumps({'stat':1, 'desc':'Unit is set successfully.', 'uid':uid}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    if not POST:
        if limit == 'one':
            result = Unit.queryOne(condition, projection=projection)
            if result:
                result = format_datetime(result)
        else:
            result = []
            for one in Unit.queryAll(condition, projection=projection):
                one = format_datetime(one)
                result.append(one)
        result = json.dumps({'stat':1, 'desc':'', 'unit':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result
        