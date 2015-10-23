#!/usr/bin/python
# coding=utf8
import json
from datakit.mysql.suit import withMysql, dbpc, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template
from views import produce

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
        total = dbpc.handler.queryOne(""" select count(gt.id) as total from grab_task gt; """)['total']
    count = (total - 1)/pagetotal + 1
    tasks = dbpc.handler.queryAll(""" select gt.id, gt.name as task_name from grab_task gt order by gt.update_time desc limit %s, %s; """, ((page-1)*pagetotal, pagetotal))
    return render_template('tasklist.html', tasks=tasks, pagetotal=pagetotal, page=page, total=total, count=count)

@produce.route('/task/detail', methods=['GET', 'POST'])
@produce.route('/task/detail/<tid>', methods=['GET', 'POST'])
@withMysql(WDB, resutype='DICT', autocommit=True)
def taskdetail(tid=None):
    if request.method == 'GET':
        if tid is None:
            task = {'id':'', 'aid':'', 'sid':'', 'task_name':'', 'extra':'', 'flow':'', 'params':'', 'worknum':6, 'queuetype':'P', 'worktype':'THREAD', 'trace':0, 'timeout':30, 'category':'', 'tag':''}
        else:
            task = dbpc.handler.queryOne(""" select gt.id, gt.aid, concat(gc.val, gu.dirpath, ga.filepath) as article_name, gs.name as section_name, gt.sid, gt.name as task_name, gt.extra, gt.flow, gt.params, gt.worknum, gt.queuetype, gt.worktype, gt.trace, gt.timeout, gt.category, gt.tag from grab_task gt join grab_article ga on gt.aid = ga.id join grab_section gs  on gt.sid = gs.id join grab_unit gu on ga.uid =gu.id join grab_config gc on gc.type='ROOT' and gc.key ='dir' where gt.id = %s; """, (tid,))
        task['queuetype_name'] = QUEUETYPE.get(task['queuetype'], '')
        task['worktype_name'] = WORKTYPE.get(task['worktype'], '')
        task['trace_name'] = TRACE.get(task['trace'], '')
        return render_template('taskdetail.html', task=task)
    elif request.method == 'POST':
        task_name = request.form.get('task_name')
        extra = request.form.get('extra')
        category = request.form.get('category')
        tag = request.form.get('tag')
        aid = request.form.get('aid')
        flow = request.form.get('flow')
        sid = request.form.get('sid')
        params = request.form.get('params')
        timeout = request.form.get('timeout')
        worknum = request.form.get('worknum')
        queuetype = request.form.get('queuetype')
        worktype = request.form.get('worktype')
        trace = request.form.get('trace')
        if tid is None:
            dbpc.handler.insert(""" insert into `grab_task` (`name`,`extra`,`category`,`tag`,`aid`,`flow`,`sid`,`params`,`timeout`,`worknum`,`queuetype`,`worktype`,`trace`, `creator`, `updator`, `create_time`)
                                                      values(%s,                %s,         %s,    %s,    %s,     %s,    %s,       %s,        %s,        %s,          %s,         %s,     %s,         0,         0,         now()); """, 
                                                         (aid, sid, task_name, flow, params, worknum, queuetype, worktype, trace, timeout, category, tag))
            tid = dbpc.handler.queryOne(""" select * from grab_task where `name` = %s """, (task_name,))['id']
        else:
            dbpc.handler.update(""" update `grab_task` set `name`=%s,`extra`=%s,`category`=%s,`tag`=%s,`aid`=%s,`flow`=%s,`sid`=%s,`params`=%s,`timeout`=%s,`worknum`=%s,`queuetype`=%s,`worktype`=%s,`trace`=%s, update_time=now() where `id` = %s """, (task_name,extra,category,tag,aid,flow,sid,params,timeout,worknum,queuetype,worktype,trace, tid))
        return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        pass

@produce.route('/task/articles', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def taskarticles():
    articles = dbpc.handler.queryAll(""" select ga.id, concat(gc.val, gu.dirpath, ga.filepath) as article_name from grab_unit gu join grab_config gc join grab_article ga on gc.type='ROOT' and gc.key ='dir' and ga.uid =gu.id; """)
    # return jsonify(articles)
    return json.dumps(articles, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')

@produce.route('/task/flows', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def taskflows():
    aid = request.args.get('aid', 0)
    flows = dbpc.handler.queryAll(""" select distinct flow from grab_section where aid = %s; """, (aid, ))
    return json.dumps(flows, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    # return jsonify(flows)

@produce.route('/task/sections', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def tasksections():
    aid = request.args.get('aid', 0)
    flow = request.args.get('flow', '')
    sections = dbpc.handler.queryAll(""" select `id`, `name` as section_name from grab_section where aid = %s and flow = %s; """, (aid, flow))
    return json.dumps(sections, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    # return jsonify(sections)
