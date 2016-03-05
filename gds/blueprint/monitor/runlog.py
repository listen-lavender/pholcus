#!/usr/bin/env python
# coding=utf8
import json, urlparse
import time, datetime
from bson import ObjectId
from model.setting import withBase, withData, base, data, _BASE_R, _BASE_W, RDB, WDB
from model.setting import baseorm
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from views import monitor
from model.log import RunLog


@monitor.route('/task/runlog/<tid>', methods=['GET'])
@withData(RDB, resutype='DICT')
def taskrunlog(tid):
    user = request.user
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = int(request.args.get('total', 0))
    count = (total - 1)/pagetotal + 1
    tid = baseorm.IdField.verify(tid)
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
    return render_template('task/runlog.html', appname=g.appname, user=user, title='RunLog', columns=columns, rows=logs, pagetotal=pagetotal, page=page, total=total, count=count)
