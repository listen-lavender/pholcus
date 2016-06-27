#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
from model.setting import withBase, basecfg
from flask import Blueprint, request, Response, render_template, g
from rest import api
from model.base import Task

@api.route('/task', methods=['POST'])
@api.route('/task/<tid>', methods=['POST'])
@withBase(basecfg.W, resutype='DICT', autocommit=True)
def task(tid=None):
    user = request.user
    condition = request.form.get('condition', '{}')
    condition = json.loads(condition)
    data = request.form.get('data', '{}')
    data = json.loads(data)
    projection = request.form.get('projection', '{}')
    projection = json.loads(projection)

    limit = request.form.get('limit', 'one')

    if tid is not None:
        condition['_id'] = tid
    if data:
        if '_id' in condition:
            Task.update(user, condition, data)
            tid = condition['_id']
        else:
            data = Task(**data)
            tid = Task.insert(user, data)
        result = json.dumps({'stat':1, 'desc':'Task is set successfully.', 'task':{'_id':tid}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        if limit == 'one':
            result = Task.queryOne(user, condition, projection=projection)
        else:
            result = list(Task.queryAll(user, condition, projection=projection))
        result = json.dumps({'stat':1, 'desc':'', 'task':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result
        