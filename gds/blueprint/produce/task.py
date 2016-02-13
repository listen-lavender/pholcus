#!/usr/bin/python
# coding=utf8
import json, datetime
from settings import withBase, withData, baseConn, dataConn, _BASE_R, _BASE_W
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from views import produce
from model.base import Task, Section, Article, Unit, Config

QUEUETYPE = {'P':'本地队列', 'B':'beanstalk队列'}
WORKTYPE = {'THREAD':'线程', 'COROUTINE':'协程'}
TRACE = {0:'否', 1:'是'}

@produce.route('/task/list', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def tasklist():
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = int(request.args.get('total', 0))
    if total == 0:
        total = Task.count({})
    count = (total - 1)/pagetotal + 1
    tasks = Task.queryAll({}, projection={'id':1, 'name':1}, sort=[('update_time', -1)], skip=(page-1)*pagetotal, limit=pagetotal)
    return render_template('ptasklist.html', appname=g.appname, logined=True, tasks=tasks, pagetotal=pagetotal, page=page, total=total, count=count)

@produce.route('/task/detail', methods=['GET', 'POST'])
@produce.route('/task/detail/<tid>', methods=['GET', 'POST'])
@withMysql(WDB, resutype='DICT', autocommit=True)
def taskdetail(tid=None):
    if request.method == 'GET':
        if tid is None:
            tid = request.args.get('tid')
        if tid is None:
            task = {'id':'', 'aid':'', 'sid':'', 'task_name':'', 'extra':'', 'type':'ONCE', 'period':0, 'flow':'', 'params':'', 'worknum':6, 'queuetype':'P', 'worktype':'THREAD', 'trace':0, 'timeout':30, 'category':'', 'tag':''}
        else:
            projection = {'id':1, 'aid':1, 'sid':1, 'name':1, 'extra':1, 'type':1, 'period':1, 'flow':1, 'params':1, 'worknum':1, 'queuetype':1, 'worktype':1, 'trace':1, 'timeout':1, 'category':1, 'tag':1}
            task = Task.queryOne({'id':tid}, projection=projection)
            task['task_name'] = task['name']
            projection = {'name':1}
            section = Section.queryOne({'id':task['sid']}, projection=projection)
            projection = {'filepath':1, 'uid':1}
            article = Article.queryOne({'id':task['aid']}, projection=projection)
            projection = {'dirpath':1}
            unit = Unit.queryOne({'id':article['uid']}, projection=projection)
            projection = {'val':1}
            config = Config.queryOne({'type':'ROOT', 'key':'dir'}, projection=projection)
            task['section_name'] = section['name']
            task['article_name'] = config['val'] + unit['dirpath'] + article['filepath']
        task['queuetype_name'] = QUEUETYPE.get(task['queuetype'], '')
        task['worktype_name'] = WORKTYPE.get(task['worktype'], '')
        task['trace_name'] = TRACE.get(task['trace'], '')
        return render_template('ptaskdetail.html', appname=g.appname, logined=True, task=task)
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
        trace = request.form.get('trace', 0)
        if tasktype == 'ONCE':
            period = 0
            queuetype = 'P'
        else:
            queuetype = 'R'
        if tid is None:
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
                trace=trace,
                creator=user['id'],
                updator=user['id'],
                create_time=datetime.datetime.now())
            tid = Task.insert(task)
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
                'trace':trace,
                'updator':user['id'],
                'update_time':datetime.datetime.now()
            }
            Task.update({'id':tid}, doc)
        return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        pass

@produce.route('/task/articles', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def taskarticles():
    articles = baseConn.handler.queryAll(""" select ga.id, concat(gc.val, gu.dirpath, ga.filepath) as article_name from grab_unit gu join grab_config gc join grab_article ga on gc.type='ROOT' and gc.key ='dir' and ga.uid =gu.id; """)
    # return jsonify(articles)
    return json.dumps(articles, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')

@produce.route('/task/flows', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def taskflows():
    aid = request.args.get('aid', 0)
    flows = baseConn.handler.queryAll(""" select distinct flow from grab_section where aid = %s; """, (aid, ))
    return json.dumps(flows, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    # return jsonify(flows)

@produce.route('/task/sections', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def tasksections():
    aid = request.args.get('aid', 0)
    flow = request.args.get('flow', '')
    sections = baseConn.handler.queryAll(""" select `id`, `name` as section_name from grab_section where aid = %s and flow = %s; """, (aid, flow))
    return json.dumps(sections, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    # return jsonify(sections)
