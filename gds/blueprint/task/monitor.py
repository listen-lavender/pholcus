#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
from model.setting import withBase, basecfg, withData, datacfg
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from views import monitor
from model.base import Task

STATDESC = {0:'stopped', 1:'started', 2:'running', 3:'error'}
EXETYPE = {'ONCE':'临时任务', 'FOREVER':'周期任务'}

@monitor.route('/monitor', methods=['GET'])
@withBase(basecfg.R, resutype='DICT')
def tasklist():
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
        one['type_name'] = EXETYPE.get(one['type'], '')

    result = {"appname":g.appname, "user":user, "task":tasks, "pagetotal":pagetotal, "page":page, "total":total, "count":count}
    return json.dumps({'stat':1, 'desc':'success', 'result':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
