#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
from model.setting import withBase, withData, base, data, _BASE_R, _BASE_W, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from rest import api
from model.base import Datamodel, Creator
from model.log import Statistics

@api.route('/datamodel', methods=['POST'])
@api.route('/datamodel/<dmid>', methods=['POST'])
@withBase(RDB, resutype='DICT')
def datamodel(dmid=None):
    user = request.user
    condition = request.form.get('condition', '{}')
    condition = json.loads(condition)
    data = request.form.get('data', '{}')
    data = json.loads(data)
    projection = request.form.get('projection', '{}')
    projection = json.loads(projection)

    limit = request.form.get('limit', 'one')

    if dmid is not None:
        condition['_id'] = dmid
    if data:
        if '_id' in condition:
            Datamodel.update(condition, {'$set':data})
            dmid = condition['_id']
        else:
            dmid = Datamodel.insert(data)
        result = json.dumps({'stat':1, 'desc':'Datamodel %s is set successfully.' % name, 'dmid':dmid}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        if limit == 'one':
            result = Datamodel.queryOne(user, condition)
        else:
            result = list(Datamodel.queryAll(user, condition))
        result = json.dumps({'stat':1, 'desc':'', 'datamodel':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result
        