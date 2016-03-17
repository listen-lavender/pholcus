#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
from model.setting import withBase, withData, base, data, _BASE_R, _BASE_W, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from views import monitor
from model.base import Task, Creator
from model.log import Statistics

@monitor.route('/task', methods=['POST'])
@monitor.route('/task/<tid>', methods=['POST'])
@withBase(RDB, resutype='DICT')
def task(tid=None):
    condition = request.form.get('condition', '{}')
    condition = json.loads(condition)
    data = request.form.get('data', '{}')
    data = json.loads(data)
    projection = request.form.get('projection', '{}')
    projection = json.loads(projection)

    limit = request.form.get('limit', 'one')

    user = Creator.queryOne({}, {'username':paras['appKey']})
    if checksign(paras, user['secret']):
        user['name'] = user['username']
    else:
        user = {}

    if tid is not None:
        condition['_id'] = tid
    if data:
        if '_id' in condition:
            Task.update(user, condition, data)
            tid = condition['_id']
        else:
            tid = Task.insert(data)
        result = json.dumps({'stat':1, 'desc':'Task %s is set successfully.' % name, 'tid':tid}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        if limit == 'one':
            result = Task.queryOne(user, condition)
        else:
            result = list(Task.queryAll(user, condition))
        result = json.dumps({'stat':1, 'desc':'', 'task':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result
        