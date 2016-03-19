#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
from model.setting import withBase, basecfg
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from rest import api, format_datetime
from model.base import Config, Creator
from model.log import Statistics

@api.route('/config', methods=['POST'])
@api.route('/config/<cid>', methods=['POST'])
@withBase(basecfg.R, resutype='DICT')
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
        result = json.dumps({'stat':1, 'desc':'Config is set successfully.', 'cid':cid}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        if limit == 'one':
            result = Config.queryOne(condition, projection=projection)
            result = format_datetime(result)
        else:
            result = []
            for one in Config.queryAll(condition, projection=projection):
                one = format_datetime(one)
                result.append(one)
        result = json.dumps({'stat':1, 'desc':'', 'config':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result
        