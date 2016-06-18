#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
import pickle
from model.setting import withData, datacfg, baseorm
from flask import Blueprint, request, Response, render_template, g
from webcrawl.queue.mongo import Queue
from model.setting import WORKQUEUE, TIMEND
from model.log import Logsummary
from views import task

q = Queue(host=WORKQUEUE['host'], port=WORKQUEUE['port'], db=WORKQUEUE['db'], tube=WORKQUEUE['tube'], init=False)
q = q.mc[q.tube]

@task.route('/timeline', methods=['GET'])
@withData(datacfg.R, resutype='DICT')
def timeline():
    user = request.user
    tid = request.args.get('tid')
    end = request.args.get('end')
    if end:
        end = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S')
    else:
        end = datetime.datetime.now()
    start = end - datetime.timedelta(hours=8)
    cond = {'tid':baseorm.IdField.verify(tid), 
        '$and':[{'create_time':{'$gte':start.strftime('%Y-%m-%d %H:%M:%S')}},
                {'create_time':{'$lt':end.strftime('%Y-%m-%d %H:%M:%S')}}]}
    timeline = []
    peak = 0
    for one in Logsummary.queryAll(cond, projection={'_id':0, 'create_time':1, 'elapse':1}, sort=[('create_time', 1)]):
        one['create_time'] = one['create_time'][11:TIMEND]
        peak = max(one['elapse'], peak)
        timeline.append(one)
    peak = max(0.25, round(peak/2.0, 2))
    result = {"appname":g.appname, "user":user, "timeline":timeline, "peak":peak}
    return json.dumps({'code':1, 'desc':'success', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')

@task.route('/quantityline', methods=['GET'])
@withData(datacfg.R, resutype='DICT')
def quantityline():
    user = request.user
    tid = request.args.get('tid')
    end = request.args.get('end')
    if end:
        end = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S')
    else:
        end = datetime.datetime.now()
    start = end - datetime.timedelta(hours=8)
    cond = {'tid':baseorm.IdField.verify(tid), 
        '$and':[{'create_time':{'$gte':start.strftime('%Y-%m-%d %H:%M:%S')}},
                {'create_time':{'$lt':end.strftime('%Y-%m-%d %H:%M:%S')}}]}
    quantityline = []
    peak = 0
    for one in Logsummary.queryAll(cond, projection={'_id':0, 'create_time':1, 'succ':1, 'fail':1, 'timeout':1}, sort=[('create_time', 1)]):
        one['total'] = one['succ'] + one['fail'] + one['timeout']
        one['create_time'] = one['create_time'][11:TIMEND]
        peak = max(one['total'], peak)
        quantityline.append(one)
    peak = (peak-1)/2 + 1
    result = {"appname":g.appname, "user":user, "quantityline":quantityline, "peak":peak}
    return json.dumps({'code':1, 'desc':'success', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')

