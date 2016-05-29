#!/usr/bin/env python
# coding=utf8
import os
import json
import time, datetime
from model.setting import withBase, basecfg
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from rest import api, format_datetime
from model.base import Datamodel, Creator
from model.log import Logsummary
from . import exepath, modelpath, allowed, store

@api.route('/datamodel', methods=['POST'])
@api.route('/datamodel/<dmid>', methods=['POST'])
@withBase(basecfg.R, resutype='DICT')
def datamodel(dmid=None):
    user = request.user
    condition = request.form.get('condition', '{}')
    condition = json.loads(condition)
    data = request.form.get('data', '{}')
    data = json.loads(data)
    pyfile = request.files.get('file')
    projection = request.form.get('projection', '{}')
    projection = json.loads(projection)

    limit = request.form.get('limit', 'one')

    if dmid is not None:
        condition['_id'] = dmid
    POST = False
    if pyfile:
        POST = True
        result = {'stat':0, 'desc':'请上传正确格式的python文件', 'datamodel':''}
        if pyfile and allowed(pyfile.filename):
            filename = pyfile.filename
            model = pyfile.stream.read()
            store(exepath(filename), model)
            store(modelpath(filename), model)
            result['stat'] = 1
            result['desc'] = '上传成功'
        result = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    if data:
        POST = True
        data['updator'] = user['_id']
        if '_id' in condition:
            Datamodel.update(condition, {'$set':data})
            dmid = condition['_id']
        else:
            data['creator'] = user['_id']
            data = Datamodel(**data)
            dmid = Datamodel.insert(data)
        result = json.dumps({'stat':1, 'desc':'Datamodel is set successfully.', 'dmid':dmid}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    if not POST:
        if limit == 'one':
            result = Datamodel.queryOne(condition, projection=projection)
            if result:
                result = format_datetime(result)
        else:
            result = []
            for one in Datamodel.queryAll(condition, projection=projection):
                one = format_datetime(one)
                result.append(one)
        result = json.dumps({'stat':1, 'desc':'', 'datamodel':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result
        