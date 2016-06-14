#!/usr/bin/env python
# coding=utf8
import os
import json
import time, datetime
from model.setting import withBase, basecfg
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from rest import api
from model.base import Article, Creator
from . import exepath, allowed

@api.route('/article', methods=['POST'])
@api.route('/article/<aid>', methods=['POST'])
@withBase(basecfg.W, resutype='DICT', autocommit=True)
def article(aid=None):
    user = request.user
    condition = request.form.get('condition', '{}')
    condition = json.loads(condition)
    data = request.form.get('data', '{}')
    data = json.loads(data)
    pyfile = request.files.get('file')
    projection = request.form.get('projection', '{}')
    projection = json.loads(projection)

    limit = request.form.get('limit', 'one')

    if aid is not None:
        condition['_id'] = aid
    POST = False
    if pyfile:
        POST = True
        result = {'stat':0, 'desc':'请上传正确格式的python文件', 'article':Article.queryOne(user, condition, projection=projection)}
        if pyfile and allowed(pyfile.filename):
            filename = pyfile.filename
            pyfile.save(exepath(filename))
            result['stat'] = 1
            result['desc'] = '上传成功'
        result = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    if data:
        POST = True
        if '_id' in condition:
            Article.update(user, condition, data)
            aid = condition['_id']
        else:
            data = Article(**data)
            aid = Article.insert(user, data)
        result = json.dumps({'stat':1, 'desc':'Article is set successfully.', 'article':{'_id':aid}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    if not POST:
        if limit == 'one':
            result = Article.queryOne(user, condition, projection=projection)
        else:
            result = list(Article.queryAll(user, condition, projection=projection))
        result = json.dumps({'stat':1, 'desc':'', 'article':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result
        