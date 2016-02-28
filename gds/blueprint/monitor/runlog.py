#!/usr/bin/env python
# coding=utf8
import json, urlparse
import time, datetime
from model.setting import withBase, withData, base, data, _BASE_R, _BASE_W, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from views import monitor
from model.base import Task
from model.log import RunLog


@monitor.route('/task/runlog/<tid>', methods=['GET', 'POST'])
@withBase(RDB, resutype='DICT', autocommit=True)
@withData(RDB)
def runlog(tid):
    if request.method == 'GET':
        user = request.user
    else:
        user = {}
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = int(request.args.get('total', 0))
    count = (total - 1)/pagetotal + 1
    logs = RunLog.queryAll({'tid':tid}, sort=[('_id', -1)], skip=(page-1)*pagetotal, limit=pagetotal)
    if total == 0:
        total = logs.count()
    count = (total - 1)/pagetotal + 1
    logs = list(logs)
    oc = []
    dtc = []
    lc = []
    dc = []
    if logs:
        columns = logs[0].keys()
        columns.remove('_id')
        columns.remove('tid')
        for one in logs[0]:
            if type(logs[0][one]) == ObjectId:
                oc.append(one)
            elif type(logs[0][one]) == datetime.datetime:
                dtc.append(one)
            elif type(logs[0][one]) == list:
                lc.append(one)
            elif type(logs[0][one]) == dict:
                dc.append(one)
    else:
        columns = []
    for one in logs:
        for c in oc:
            one[c] = str(c)
        for c in dtc:
            one[c] = one[c].strftime('%Y-%m-%d %H:%M:%S')
        for c in lc:
            one[c] = ','.join([str(item) for item in one[c]])
        for c in dc:
            one[c] = json.dumps(one[c], ensure_ascii=False)
    if request.method == 'GET':
        return render_template('task/data.html', appname=g.appname, user=user, title=model['name'], columns=columns, rows=logs, pagetotal=pagetotal, page=page, total=total, count=count)
    else:
        return json.dumps({'stat':1, 'desc':'success', 'logs':logs, 'pagetotal':pagetotal, 'page':page, 'total':total, 'count':count}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
