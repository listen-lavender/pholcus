#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
import urlparse
from model.setting import withBase, basecfg, pack
from flask import Blueprint, request, Response, render_template, g
from model.setting import withBase, withDataQuery, withDataCount, baseorm, basecfg
from model.base import Task, Article, Unit, Datamodel, Creator
from model.log import Logsummary
from bson import ObjectId
from views import task

@task.route('/<tid>/data', methods=['GET'])
@withBase(basecfg.R, resutype='DICT')
def taskdata(tid):
    from model.data import *
    if request.method == 'GET':
        user = request.user
    else:
        paras = dict(urlparse.parse_qsl(urlparse.urlparse(request.url).query))
        user = Creator.queryOne({}, {'username':paras['appKey']})
        # if checksign(paras, user['secret']):
        #     user['name'] = user['username']
        # else:
        #     user = {}
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 10))
    keyword = request.args.get('keyword')
    tid = baseorm.IdField.verify(tid)

    task = Task.queryOne(user, {'_id':tid}, projection={'aid':1})
    article = Article.queryOne(user, {'_id':task['aid']}, projection={'uid':1})
    unit = Unit.queryOne({'_id':article['uid']}, projection={'dmid':1})
    datamodel = Datamodel.queryOne({'_id':unit['dmid']}, projection={'name':1, 'table':1})
    model, table = datamodel['name'], datamodel['table']

    Cls = locals()[model]
    condition = {'tid':tid}
    if keyword:
        pack(Cls, keyword, condition)
    datas = withDataQuery(table, condition, sort=[('update_time', -1)], skip=skip, limit=limit, qt='all')

    datas = list(datas)

    if datas:
        total = withDataCount(table, condition)
        columns = Cls.__mappings__.keys()
        columns.sort()
        columns.insert(0, '_id')
    else:
        total = 0
        columns = []
    
    result = {"appname":g.appname, "user":user, "data":datas, 'column':columns, "total":total}
    result = json.dumps({'code':1, 'msg':'', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result
