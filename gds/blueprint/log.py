#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
import pickle
from model.setting import withData, datacfg, baseorm
from flask import Blueprint, request, Response, render_template, g
from webcrawl.queue.mongo import Queue
from model.setting import WORKQUEUE
from model.log import Log
from views import running

q = Queue(host=WORKQUEUE['host'], port=WORKQUEUE['port'], db=WORKQUEUE['db'], tube=WORKQUEUE['tube'], init=False)
q = q.mc[q.tube]

@running.route('/log', methods=['GET'])
@running.route('/log/<ssid>', methods=['GET'])
@withData(datacfg.R, resutype='DICT')
def log(ssid=None):
    user = request.user
    if ssid is None:
        tid = request.args.get('tid')
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 10))
        condition = {'tid':baseorm.IdField.verify(tid)}
        total = Log.count(condition)
        log = list(Log.queryAll(condition, sort=[('create_time', -1), ], skip=skip, limit=limit))
        result = {"appname":g.appname, "user":user, "log":log, "total":total}
    else:
        snapshot = q.find_one({'_id':ssid}) or {'args':'', 'kwargs':''}
        log = Log.queryOne({'_id':ssid}) or {'desc':''}
        txt = snapshot['txt'].encode('utf-8')
        txt = pickle.loads(txt)
        args = str(txt['args'])
        kwargs = json.dumps(txt['kwargs'], ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
        result = {"appname":g.appname, "user":user, "log":{'args':args, 'kwargs':kwargs, 'exception':log['desc'], 'tid':snapshot['tid']}}
    return json.dumps({'code':1, 'desc':'success', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
