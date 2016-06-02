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
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = int(request.args.get('total', 0))
    count = (total - 1)/pagetotal + 1
    tid = baseorm.IdField.verify(tid)
    task = Task.queryOne(user, {'_id':tid}, projection={'aid':1})
    article = Article.queryOne(user, {'_id':task['aid']}, projection={'uid':1})
    unit = Unit.queryOne({'_id':article['uid']}, projection={'dmid':1})
    datamodel = Datamodel.queryOne({'_id':unit['dmid']}, projection={'name':1, 'table':1})
    datas = withDataQuery(datamodel['table'], {'tid':tid}, sort=[('atime', -1)], skip=(page-1)*pagetotal, limit=pagetotal, qt='all')
    if total == 0:
        total = withDataCount(datamodel['table'], {'tid':tid})
    count = (total - 1)/pagetotal + 1
    datas = list(datas)

    if datas:
        columns = datas[0].keys()
        columns.sort()
    else:
        columns = []
    
    result = {"appname":g.appname, "user":user, "data":datas, 'column':columns}
    result = json.dumps({'code':1, 'msg':'', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result
