#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
from model.setting import withBase, withData, base, data, _BASE_R, _BASE_W, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from rest import api
from model.base import Config, Creator
from model.log import Statistics

@api.route('/config', methods=['POST'])
@api.route('/config/<cid>', methods=['POST'])
@withBase(RDB, resutype='DICT')
def config(cid=None):
    user = request.user
    condition = request.form.get('condition', '{}')
    condition = json.loads(condition)
    data = request.form.get('data', '{}')
    data = json.loads(data)
    projection = request.form.get('projection', '{}')
    projection = json.loads(projection)

    limit = request.form.get('limit', 'one')

    if cid is not None:
        condition['_id'] = cid
    if data:
        if '_id' in condition:
            Config.update(condition, {'$set':data})
            cid = condition['_id']
        else:
            cid = Config.insert(data)
        result = json.dumps({'stat':1, 'desc':'Config %s is set successfully.' % name, 'cid':cid}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        if limit == 'one':
            result = Config.queryOne(condition, projection=projection)
        else:
            result = list(Config.queryAll(condition))
        result = json.dumps({'stat':1, 'desc':'', 'config':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result
        