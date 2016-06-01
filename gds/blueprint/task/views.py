#!/usr/bin/env python
# coding=utf8
import json
import urllib
from model.setting import withBase, basecfg, baseorm
from model.base import Task, Section, Flow, Article
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g

task = Blueprint('task', __name__, template_folder='template')

from activity import *

EXETYPE = {'ONCE':'临时任务', 'FOREVER':'周期任务'}

@task.route('/list', methods=['GET'])
@withBase(basecfg.R, resutype='DICT', autocommit=True)
def tasklist():
    user = request.user
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = int(request.args.get('total', 0))
    if total == 0:
        total = Task.count(user, {})
    count = (total - 1)/pagetotal + 1
    tasks = Task.queryAll(user, {}, projection={'_id':1, 'name':1, 'extra':1}, sort=[('update_time', -1)], skip=(page-1)*pagetotal, limit=pagetotal)
    result = {"appname":g.appname, "user":user, "task":tasks}
    result = json.dumps({'code':1, 'msg':'', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result


@task.route('/detail', methods=['GET', 'POST'])
@task.route('/detail/<tid>', methods=['GET', 'POST'])
@withBase(basecfg.W, resutype='DICT', autocommit=True)
def taskdetail(tid=None):
    user = request.user
    tid = baseorm.IdField.verify(tid)
    if request.method == 'GET':
        user = request.user
        if tid is None:
            tid = request.args.get('tid')
        if tid is None:
            task = {'_id':'', 'aid':'', 'sid':'', 'name':'', 'extra':'', 'type':'ONCE', 'period':0, 'flow':'', 'params':'', 'worknum':6, 'queuetype':'M', 'worktype':'THREAD', 'timeout':30, 'category':'', 'push_url':'', 'pull_url':'', 'tag':'', 'current':True}
        else:
            projection = {'_id':1, 'aid':1, 'sid':1, 'name':1, 'extra':1, 'type':1, 'period':1, 'flow':1, 'params':1, 'worknum':1, 'queuetype':1, 'worktype':1, 'timeout':1, 'category':1, 'push_url':1, 'tag':1, 'creator':1}
            task = Task.queryOne(user, {'_id':tid}, projection=projection)
            task['name'] = task['name']
            projection = {'name':1, 'fid':1}
            section = Section.queryOne(user, {'_id':task['sid']}, projection=projection)
            projection = {'name':1}
            flow = Flow.queryOne({'_id':section['fid']}, projection=projection)
            projection = {'filepath':1, 'uid':1}
            article = Article.queryOne(user, {'_id':task['aid']}, projection=projection)
            task['section_name'] = section['name']
            task['flow_name'] = flow['name']
            task['article_name'] = article['filepath']
            task['current'] = str(task['creator']) == user['_id']
            task['pull_url'] = 'http://%s/gdc/api/data/%s' % (request.host, str(task['_id']))
            del task['creator']
        task['queuetype_name'] = 'mongo' # QUEUETYPE.get(task['queuetype'], '')
        task['worktype_name'] = '多线程' # WORKTYPE.get(task['worktype'], '')
        task['type_name'] = EXETYPE.get(task['type'], '')
        author = {}
        # for one in Permit.queryAll({'otype':'Task', 'oid':tid}, projection={'cid':1, '_id':0}):
        #     author[str(one['cid'])] = ''
        task['author'] = urllib.quote(json.dumps(author).encode('utf8'))
        result = {"appname":g.appname, "user":user, "task":task}
        result = json.dumps({'code':1, 'msg':'', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
        return result
    elif request.method == 'POST':
        user = request.user
        name = request.form.get('name')
        extra = request.form.get('extra')
        category = request.form.get('category')
        tag = request.form.get('tag')
        tasktype = request.form.get('type')
        period = request.form.get('period')
        push_url = request.form.get('push_url')
        aid = request.form.get('aid')
        flow = request.form.get('flow')
        sid = request.form.get('sid')
        params = request.form.get('params')
        timeout = request.form.get('timeout', 30)
        worknum = request.form.get('worknum', 6)
        queuetype = request.form.get('queuetype', 'P')
        worktype = 'THREAD'
        addcid = request.form.get('addcid', '').split(',')
        delcid = request.form.get('delcid', '').split(',')
        if tasktype == 'ONCE':
            period = 0
            queuetype = 'P'
        else:
            queuetype = 'R'
        section = Section.queryOne(user, {'_id':sid})
        result = {'stat':1, 'desc':'success', 'data':{}}
        if section is None:
            result = {'stat':0, 'desc':'fail', 'data':{}}
        elif tid is None:
            task = Task(name=task_name,
                extra=extra,
                category=category,
                tag=tag,
                type=tasktype,
                period=period,
                aid=aid,
                flow=flow,
                sid=sid,
                params=params,
                timeout=timeout,
                worknum=worknum,
                queuetype=queuetype,
                worktype=worktype,
                push_url=push_url,
                creator=user['_id'],
                updator=user['_id'],
                create_time=datetime.datetime.now())
            tid = Task.insert(user, task)
        else:
            doc = {'name':task_name,
                'extra':extra,
                'category':category,
                'tag':tag,
                'type':tasktype,
                'period':period,
                'aid':aid,
                'flow':flow,
                'sid':sid,
                'params':params,
                'timeout':timeout,
                'worknum':worknum,
                'queuetype':queuetype,
                'worktype':worktype,
                'push_url':push_url,
                'updator':user['_id'],
                'update_time':datetime.datetime.now()
            }
            Task.update(user, {'_id':tid}, doc)
        for cid in addcid:
            if cid == '':
                continue
            cid = baseorm.IdField.verify(cid)
            if Permit.queryOne({'cid':cid, 'otype':'Task', 'oid':tid}) is None:
                permit = Permit(cid=cid, otype='Task', oid=baseorm.IdField.verify(tid), authority=1, desc='---q', status=1, creator=user['_id'], updator=user['_id'], create_time=datetime.datetime.now())
                Permit.insert(permit)
        for cid in delcid:
            if cid == '':
                continue
            Permit.delete({'cid':cid, 'otype':'Task', 'oid':tid})
        return json.dumps(result, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        pass

