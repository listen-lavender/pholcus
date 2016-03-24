#!/usr/bin/env python
# coding=utf8
import json, datetime, urllib, urlparse
from model.setting import withBase, basecfg
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g, redirect
from views import produce
from model.base import Task, Section, Article, Unit, Permit, Creator
from model.setting import baseorm

QUEUETYPE = {'P':'本地队列', 'B':'beanstalk队列'}
WORKTYPE = {'THREAD':'线程', 'COROUTINE':'协程'}
TRACE = {0:'否', 1:'是'}
EXETYPE = {'ONCE':'临时任务', 'FOREVER':'周期任务'}


@produce.route('/task/list', methods=['GET'])
@withBase(basecfg.R, resutype='DICT')
def tasklist():
    user = request.user
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = int(request.args.get('total', 0))
    if total == 0:
        total = Task.count(user, {})
    count = (total - 1)/pagetotal + 1
    tasks = Task.queryAll(user, {}, projection={'_id':1, 'name':1}, sort=[('update_time', -1)], skip=(page-1)*pagetotal, limit=pagetotal)
    return render_template('task/list.html', appname=g.appname, user=user, tasks=tasks, pagetotal=pagetotal, page=page, total=total, count=count)


@produce.route('/task/detail', methods=['GET', 'POST'])
@produce.route('/task/detail/<tid>', methods=['GET', 'POST'])
@withBase(basecfg.W, resutype='DICT', autocommit=True)
def taskdetail(tid=None):
    if request.method == 'GET':
        user = request.user
        if tid is None:
            tid = request.args.get('tid')
        if tid is None:
            task = {'_id':'', 'aid':'', 'sid':'', 'task_name':'', 'extra':'', 'type':'ONCE', 'period':0, 'flow':'', 'params':'', 'worknum':6, 'queuetype':'P', 'worktype':'THREAD', 'trace':0, 'timeout':30, 'category':'', 'push_url':'', 'pull_url':'', 'tag':'', 'current':True}
        else:
            if request.referrer is not None and request.referrer.startswith('http'):
                urlparas = dict(urlparse.parse_qsl(urlparse.urlparse(request.referrer).query))
            else:
                urlparas = None
            projection = {'_id':1, 'aid':1, 'sid':1, 'name':1, 'extra':1, 'type':1, 'period':1, 'flow':1, 'params':1, 'worknum':1, 'queuetype':1, 'worktype':1, 'trace':1, 'timeout':1, 'category':1, 'push_url':1, 'tag':1, 'creator':1}
            task = Task.queryOne(user, {'_id':tid}, projection=projection)
            if task is None:
                if urlparas is None:
                    return redirect('/gds/a/login')
                urlparas['alert'] = urllib.quote('你没有该任务的权限')
                return redirect('%s?%s' % (request.referrer.split('?')[0], '&'.join('%s=%s' % (k, v) for k, v in urlparas.items())))
            task['task_name'] = task['name']
            projection = {'name':1}
            section = Section.queryOne(user, {'_id':task['sid']}, projection=projection)
            projection = {'filepath':1, 'uid':1}
            article = Article.queryOne(user, {'_id':task['aid']}, projection=projection)
            if article is None:
                if urlparas is None:
                    return redirect('/gds/a/login')
                urlparas['alert'] = urllib.quote('你没有该任务的权限')
                return redirect('%s?%s' % (request.referrer.split('?')[0], '&'.join('%s=%s' % (k, v) for k, v in urlparas.items())))
            projection = {'val':1}
            task['section_name'] = section['name']
            task['article_name'] = article['filepath']
            task['current'] = str(task['creator']) == user['_id']
            task['pull_url'] = 'http://%s/gds/m/task/data/%s' % (request.host, str(task['_id']))
            del task['creator']
        task['queuetype_name'] = QUEUETYPE.get(task['queuetype'], '')
        task['worktype_name'] = WORKTYPE.get(task['worktype'], '')
        task['type_name'] = EXETYPE.get(task['type'], '')
        task['trace_name'] = TRACE.get(task['trace'], '')
        author = {}
        for one in Permit.queryAll({'otype':'Task', 'oid':tid}, projection={'cid':1, '_id':0}):
            author[str(one['cid'])] = ''
        task['author'] = urllib.quote(json.dumps(author).encode('utf8'))
        return render_template('task/detail.html', appname=g.appname, user=user, task=task)
    elif request.method == 'POST':
        user = request.user
        task_name = request.form.get('task_name')
        extra = request.form.get('extra')
        tasktype = request.form.get('type')
        period = request.form.get('period')
        category = request.form.get('category')
        tag = request.form.get('tag')
        aid = request.form.get('aid')
        flow = request.form.get('flow')
        sid = request.form.get('sid')
        params = request.form.get('params')
        timeout = request.form.get('timeout', 30)
        worknum = request.form.get('worknum', 6)
        queuetype = request.form.get('queuetype', 'P')
        worktype = request.form.get('worktype', 'THREAD')
        push_url = request.form.get('push_url')
        trace = request.form.get('trace', 0)
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
                trace=trace,
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
                'trace':trace,
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


@produce.route('/task/articles', methods=['GET'])
@withBase(basecfg.R, resutype='DICT')
def taskarticles():
    user = request.user
    articles = Article.queryAll(user, {}, projection={'uid':1, '_id':1, 'filepath':1})
    for article in articles:
        article['article_name'] = article['filepath']
    return json.dumps(articles, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')


@produce.route('/task/flows', methods=['GET'])
@withBase(basecfg.R, resutype='DICT')
def taskflows():
    user = request.user
    aid = request.args.get('aid') or 0
    article = Article.queryOne(user, {'_id':aid}, projection={'_id':1})
    if article is None:
        flows = []
    else:
        sections = Section.queryAll(user, {'aid':aid}, projection={'flow':1})
        flows = list(set([section['flow'] for section in sections]))
    return json.dumps(flows, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')


@produce.route('/task/sections', methods=['GET'])
@withBase(basecfg.R, resutype='DICT')
def tasksections():
    user = request.user
    aid = request.args.get('aid') or 0
    flow = request.args.get('flow') or ''
    sections = Section.queryAll(user, {'aid':aid, 'flow':flow}, projection={'_id':1, 'name':1})
    for section in sections:
        section['section_name'] = section['name']
    return json.dumps(sections, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
