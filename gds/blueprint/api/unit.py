#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
from model.setting import withBase, withData, base, data, _BASE_R, _BASE_W, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from rest import api, format_datetime
from model.base import Unit, Creator
from model.log import Statistics

@api.route('/unit', methods=['POST'])
@api.route('/unit/<uid>', methods=['POST'])
@withBase(RDB, resutype='DICT')
def unit(uid=None):
    user = request.user
    condition = request.form.get('condition', '{}')
    condition = json.loads(condition)
    data = request.form.get('data', '{}')
    data = json.loads(data)
    projection = request.form.get('projection', '{}')
    projection = json.loads(projection)

    limit = request.form.get('limit', 'one')

    if uid is not None:
        condition['_id'] = uid
    if data:
        if '_id' in condition:
            Unit.update(condition, {'$set':data})
            uid = condition['_id']
        else:
            uid = Unit.insert(data)
        result = json.dumps({'stat':1, 'desc':'Unit is set successfully.', 'uid':uid}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        if limit == 'one':
            result = Unit.queryOne(condition, projection=projection)
            result = format_datetime(result)
        else:
            result = []
            for one in Unit.queryAll(condition, projection=projection):
                one = format_datetime(one)
                result.append(one)
        result = json.dumps({'stat':1, 'desc':'', 'unit':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result
        