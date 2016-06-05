#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
import pickle
from model.setting import withBase, basecfg
from flask import Blueprint, request, Response, render_template, g
from webcrawl.queue.mongo import Queue
from model.setting import WORKQUEUE
from views import task

DESCRIBE = {0:'ERROR', 1:'COMPLETED', 2:'WAIT', 3:'RUNNING', 4:'RETRY', 5:'ABANDONED'}
q = Queue(host=WORKQUEUE['host'], port=WORKQUEUE['port'], db=WORKQUEUE['db'], tube=WORKQUEUE['tube'], init=False)
q = q.mc[q.tube]

@task.route('/activity', methods=['GET'])
def taskactivity():
    from model.data import *
    user = request.user
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 10))

    tasks = []
    for one in q.find({}, sort=[('priority', 1)], skip=skip, limit=limit):
        txt = one.pop('txt')
        txt = pickle.loads(txt.encode('utf-8'))
        one['args'] = str(txt['args'])
        one['kwargs'] = json.dumps(txt['kwargs'], ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
        one['status'] = DESCRIBE.get(one['status'], '')
        one['times'] = one['times'] + 1
        tasks.append(one)

    if tasks:
        total = q.find().count()
    else:
        total = 0

    result = {"appname":g.appname, "user":user, "work":tasks, "total":total}
    return json.dumps({'code':1, 'desc':'success', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
