#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
from model.setting import withBase, basecfg
from flask import Blueprint, request, Response, render_template, g
from rest import api
from model.base import Flow, Creator

@api.route('/flow', methods=['POST'])
@api.route('/flow/<fid>', methods=['POST'])
@withBase(basecfg.W, resutype='DICT', autocommit=True)
def flow(fid=None):
    user = request.user
    condition = request.form.get('condition', '{}')
    condition = json.loads(condition)
    data = request.form.get('data', '{}')
    data = json.loads(data)
    projection = request.form.get('projection', '{}')
    projection = json.loads(projection)

    limit = request.form.get('limit', 'one')

    if fid is not None:
        condition['_id'] = fid
    if data:
        data['updator'] = user['_id']
        if '_id' in condition:
            data['$set'] = data.get('$set', {})
            data['$set']['updator'] = user['_id']
            Flow.update(condition, data)
            fid = condition['_id']
        else:
            data['updator'] = user['_id']
            data['creator'] = user['_id']
            data = Flow(**data)
            fid = Flow.insert(data)
        result = json.dumps({'stat':1, 'desc':'Flow is set successfully.', 'flow':{'_id':fid}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        if limit == 'one':
            result = Flow.queryOne(condition, projection=projection)
        else:
            result = list(Flow.queryAll(condition, projection=projection))
        result = json.dumps({'stat':1, 'desc':'', 'flow':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result
        