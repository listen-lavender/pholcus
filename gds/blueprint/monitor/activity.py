#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
from model.setting import withBase, withData, base, data, _BASE_R, _BASE_W, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from views import monitor
from model.base import Task
from model.log import Statistics, RunLog

STATDESC = {0:'stopped', 1:'started', 2:'running', 3:'error'}

@monitor.route('/task/activity', methods=['GET'])
@withBase(RDB, resutype='DICT')
@withData(RDB, resutype='DICT')
def taskactivity():
    user = request.user
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = int(request.args.get('total', 0))
    if total == 0:
        total = Task.count(user, {})
    count = (total - 1)/pagetotal + 1
    tasks = Task.queryAll(user, {}, sort=[('update_time', -1)], skip=(page-1)*pagetotal, limit=pagetotal)
    for one in tasks:
        one['change'] = (one['status'] in (0, 1, 2) and one['type'] == 'FOREVER') or (one['status'] in (0, 1) and one['type'] == 'ONCE')
        one['status_desc'] = STATDESC.get(one['status'], '')
        one['max'] = (Statistics.queryOne({'tid':one['_id']}, projection={'succ':1}, sort=[('succ', -1)]) or {'succ':0})['succ']
    return render_template('task/activity.html', appname=g.appname, user=user, tasks=tasks, pagetotal=pagetotal, page=page, total=total, count=count)

