#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
from model.setting import withBase, basecfg
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from rest import api
from model.base import Section, Creator

@api.route('/section', methods=['POST'])
@api.route('/section/<sid>', methods=['POST'])
@withBase(basecfg.W, resutype='DICT', autocommit=True)
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
            data = Section(**data)
            sid = Section.insert(user, data)
        result = json.dumps({'stat':1, 'desc':'Section is set successfully.', 'section':{'_id':sid}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        if limit == 'one':
            result = Section.queryOne(user, condition, projection=projection)
        else:
            result = list(Section.queryAll(user, condition, projection=projection))
        result = json.dumps({'stat':1, 'desc':'', 'section':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result
        