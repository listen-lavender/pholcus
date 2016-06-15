#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
import pickle
from model.setting import withBase, basecfg, baseorm
from flask import Blueprint, request, Response, render_template, g
from webcrawl.queue.mongo import Queue
from model.setting import WORKQUEUE
from views import running

DESCRIBE = {-2:'ABANDONED', -1:'ERROR', 0:'COMPLETED', 1:'RETRY', 2:'WAIT', 3:'RUNNING'}
q = Queue(host=WORKQUEUE['host'], port=WORKQUEUE['port'], db=WORKQUEUE['db'], tube=WORKQUEUE['tube'], init=False)
q = q.mc[q.tube]

@running.route('/snapshot', methods=['GET'])
def snapshot():
    user = request.user
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 10))
    keyword = request.args.get('keyword')

    if keyword is None:
        condition = {}
    elif keyword.isdigit() and len(keyword) == 8:
        condition = {'version':keyword}
    elif keyword.isdigit():
        condition = {'tid':baseorm.IdField.verify(keyword)}
    else:
        condition = {'methodName':{'$regex':keyword}}

    tasks = []
    for one in q.find(condition, sort=[('status', -1), ('priority', 1)], skip=skip, limit=limit):
        txt = one.pop('txt')
        txt = pickle.loads(txt.encode('utf-8'))
        one['methodName'] = one['methodName'].replace('task.', '')
        one['args'] = str(txt['args'])
        one['kwargs'] = json.dumps(txt['kwargs'], ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
        one['status'] = DESCRIBE.get(one['status'], '')
        one['times'] = one['times'] + 1
        tasks.append(one)

    if tasks:
        total = q.find(condition).count()
    else:
        total = 0

    result = {"appname":g.appname, "user":user, "work":tasks, "total":total}
    return json.dumps({'code':1, 'desc':'success', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
