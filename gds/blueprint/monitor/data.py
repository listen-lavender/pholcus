#!/usr/bin/env python
# coding=utf8
import json, urlparse
import time, datetime
from model.setting import withBase, withDataQuery, withDataCount, base, data, _BASE_R, _BASE_W, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from views import monitor
from model.base import Task, Article, Unit, Datamodel, Creator
from model.log import Statistics
from util.validate import checksign
from model import data as grabdata
from bson import ObjectId


@monitor.route('/task/data/<tid>', methods=['GET', 'POST'])
@withBase(RDB, resutype='DICT', autocommit=True)
def taskdata(tid):
    if request.method == 'GET':
        user = request.user
    else:
        paras = dict(urlparse.parse_qsl(urlparse.urlparse(request.url).query))
        user = Creator.queryOne({}, {'username':paras['appKey']})
        if checksign(paras, user['secret']):
            user['name'] = user['username']
        else:
            user = {}
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = int(request.args.get('total', 0))
    count = (total - 1)/pagetotal + 1
    # tid = Task.__mappings__['tid'].verify(tid)
    tid = int(tid)
    task = Task.queryOne(user, {'_id':tid}, projection={'aid':1})
    article = Article.queryOne(user, {'_id':task['aid']}, projection={'uid':1})
    unit = Unit.queryOne({'_id':article['uid']}, projection={'dmid':1})
    datamodel = Datamodel.queryOne({'_id':unit['dmid']}, projection={'name':1, 'table':1})
    datas = withDataQuery(datamodel['table'], {'tid':tid}, sort=[('_id', -1)], skip=(page-1)*pagetotal, limit=pagetotal, qt='all')
    if total == 0:
        total = withDataCount(datamodel['table'], {'tid':tid})
    count = (total - 1)/pagetotal + 1
    datas = list(datas)
    oc = []
    dtc = []
    lc = []
    dc = []
    if datas:
        columns = datas[0].keys()
        columns.remove('_id')
        columns.remove('tid')
        for one in datas[0]:
            if type(datas[0][one]) == ObjectId:
                oc.append(one)
            elif type(datas[0][one]) == datetime.datetime:
                dtc.append(one)
            elif type(datas[0][one]) == list:
                lc.append(one)
            elif type(datas[0][one]) == dict:
                dc.append(one)
    else:
        columns = []
    for one in datas:
        for c in oc:
            one[c] = str(c)
        for c in dtc:
            one[c] = one[c].strftime('%Y-%m-%d %H:%M:%S')
        for c in lc:
            one[c] = ','.join([str(item) for item in one[c]])
        for c in dc:
            one[c] = json.dumps(one[c], ensure_ascii=False)
    if request.method == 'GET':
        return render_template('task/data.html', appname=g.appname, user=user, title=datamodel['name'], columns=columns, rows=datas, pagetotal=pagetotal, page=page, total=total, count=count)
    else:
        return json.dumps({'stat':1, 'desc':'success', 'datas':datas, 'pagetotal':pagetotal, 'page':page, 'total':total, 'count':count}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
