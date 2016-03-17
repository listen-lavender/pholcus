#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
from model.setting import withBase, withData, base, data, _BASE_R, _BASE_W, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from rest import api, format_datetime
from model.base import Section, Creator
from model.log import Statistics

@api.route('/section', methods=['POST'])
@api.route('/section/<sid>', methods=['POST'])
@withBase(RDB, resutype='DICT')
def section(sid=None):
    user = request.user
    condition = request.form.get('condition', '{}')
    condition = json.loads(condition)
    data = request.form.get('data', '{}')
    data = json.loads(data)
    projection = request.form.get('projection', '{}')
    projection = json.loads(projection)

    limit = request.form.get('limit', 'one')

    if sid is not None:
        condition['_id'] = sid
    if data:
        if '_id' in condition:
            Section.update(user, condition, data)
            sid = condition['_id']
        else:
            sid = Section.insert(user, data)
        result = json.dumps({'stat':1, 'desc':'Section is set successfully.', 'sid':sid}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        if limit == 'one':
            result = Section.queryOne(user, condition, projection=projection)
            result = format_datetime(result)
        else:
            result = []
            for one in Section.queryAll(user, condition, projection=projection):
                one = format_datetime(one)
                result.append(one)
            print '----2', result
        result = json.dumps({'stat':1, 'desc':'', 'section':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result
        