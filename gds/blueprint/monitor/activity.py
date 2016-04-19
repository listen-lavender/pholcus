#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
from model.setting import withBase, basecfg
from flask import Blueprint, request, Response, render_template, g
from webcrawl.pjq import RedisQueue
from model.setting import WORKQUEUE
from views import monitor
from . import CJsonEncoder, allow_cross_domain

STATDESC = {0:'stopped', 1:'started', 2:'running', 3:'error'}
q = RedisQueue(host=WORKQUEUE['host'], port=WORKQUEUE['port'], db=WORKQUEUE['db'], tube=WORKQUEUE['tube'], init=False)

@monitor.route('/task/activity', methods=['GET'])
@allow_cross_domain
def taskactivity():
    from model.data import *
    user = request.user
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = q.total()
    count = (total - 1)/pagetotal + 1
    tasks = q.traversal((page-1)*pagetotal, pagetotal)
    print tasks
    if request.headers.get('User-Agent') == 'test':
        result = {"appname":g.appname, "user":user, "tasks":tasks, "pagetotal":pagetotal, "page":page, "total":total, "count":count}
        return json.dumps({'stat':1, 'desc':'success', 'result':result}, ensure_ascii=False, sort_keys=True, indent=4, cls=CJsonEncoder).encode('utf8')
    else:
        return render_template('task/activity.html', appname=g.appname, user=user, tasks=tasks, pagetotal=pagetotal, page=page, total=total, count=count)

