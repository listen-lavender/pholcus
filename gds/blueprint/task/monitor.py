#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
import urlparse
from model.setting import withBase, basecfg
from flask import Blueprint, request, Response, render_template, g
from model.setting import withBase, withDataQuery, withDataCount, baseorm, basecfg
from model.base import Task, Article, Unit, Datamodel, Creator
from model.log import Logsummary
from model import data as grabdata
from bson import ObjectId
from views import task

@task.route('/<tid>/data', methods=['GET'])
@withBase(basecfg.R, resutype='DICT')
def taskdata(tid):
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
    table = request.args.get('model')
    tid = baseorm.IdField.verify(tid)

    if not table:
        task = Task.queryOne(user, {'_id':tid}, projection={'aid':1})
        article = Article.queryOne(user, {'_id':task['aid']}, projection={'uid':1})
        unit = Unit.queryOne({'_id':article['uid']}, projection={'dmid':1})
        datamodel = Datamodel.queryOne({'_id':unit['dmid']}, projection={'name':1, 'table':1})
        table = datamodel['table']
    datas = withDataQuery(table, {'tid':tid}, sort=[('atime', -1)], skip=skip, limit=limit, qt='all')

    datas = list(datas)

    if datas:
        total = withDataCount(table, {'tid':tid})
        columns = datas[0].keys()
        columns.sort()
    else:
        total = 0
        columns = []
    
    result = {"appname":g.appname, "user":user, "data":datas, 'column':columns, "total":total, "model":table}
    result = json.dumps({'code':1, 'msg':'', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result
