#!/usr/bin/python
# coding=utf8
import json
import time, datetime
from settings import withBase, withData, base, data, _BASE_R, _BASE_W, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from views import monitor
from model.base import Task, Article, Unit, Datamodel, Statistics
from model import business


@monitor.route('/task/data/<tid>', methods=['GET'])
@withBase(RDB, resutype='DICT', autocommit=True)
@withData(RDB)
def taskdata(tid):
    user = request.user
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = int(request.args.get('total', 0))
    count = (total - 1)/pagetotal + 1
    task = Task.queryOne(user['_id'], {'_id':tid}, projection={'aid':1})
    article = Article.queryOne(user['_id'], {'_id':task['aid']}, projection={'uid':1})
    unit = Unit.queryOne(user['_id'], {'_id':article['uid']}, projection={'dmid':1})
    model = Datamodel.queryOne(user['_id'], {'_id':unit['dmid']}, projection={'name':1})
    datamodel = getattr(business, model['name'].capitalize())
    datas = datamodel.queryAll({'tid':tid}, sort=[('_id', -1)], skip=(page-1)*pagetotal, limit=pagetotal)
    if total == 0:
        total = datas.count()
    count = (total - 1)/pagetotal + 1
    datas = list(datas)
    dtc = []
    lc = []
    dc = []
    if datas:
        columns = datas[0].keys()
        columns.remove('_id')
        columns.remove('tid')
        for one in datas[0]:
            if type(datas[0][one]) == datetime.datetime:
                dtc.append(one)
            elif type(datas[0][one]) == list:
                lc.append(one)
            elif type(datas[0][one]) == dict:
                dc.append(one)
    else:
        columns = []
    for one in datas:
        for c in dtc:
            one[c] = one[c].strftime('%Y-%m-%d %H:%M:%S')
        for c in lc:
            one[c] = ','.join([str(item) for item in one[c]])
        for c in dc:
            one[c] = json.dumps(one[c], ensure_ascii=False)
    return render_template('mtaskdata.html', appname=g.appname, logined=True, title=model['name'], columns=columns, rows=datas, pagetotal=pagetotal, page=page, total=total, count=count)
