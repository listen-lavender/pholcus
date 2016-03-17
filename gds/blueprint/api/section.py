#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
from model.setting import withBase, withData, base, data, _BASE_R, _BASE_W, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from views import monitor
from model.base import Section, Creator
from model.log import Statistics

@monitor.route('/section', methods=['POST'])
@monitor.route('/section/<sid>', methods=['POST'])
@withBase(RDB, resutype='DICT')
def section(sid=None):
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

    if sid is not None:
        condition['_id'] = sid
    if data:
        if '_id' in condition:
            Section.update(user, condition, data)
            sid = condition['_id']
        else:
            sid = Section.insert(data)
        result = json.dumps({'stat':1, 'desc':'Section %s is set successfully.' % name, 'sid':sid}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        if limit == 'one':
            result = Section.queryOne(user, condition)
        else:
            result = list(Section.queryAll(user, condition))
        result = json.dumps({'stat':1, 'desc':'', 'section':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result
        