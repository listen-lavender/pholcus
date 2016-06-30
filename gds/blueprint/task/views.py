#!/usr/bin/env python
# coding=utf8
import json
import urllib
from model.setting import withBase, basecfg, baseorm, pack
from model.base import Task, Section, Flow, Article, Permit
from flask import Blueprint, request, Response, render_template, g
from .. import select, unselect

task = Blueprint('task', __name__, template_folder='template')

from monitor import *
from statistics import *

@task.route('/list', methods=['GET'])
@withBase(basecfg.R, resutype='DICT')
def tasklist():
    user = request.user
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 10))
    keyword = request.args.get('keyword')

    condition = {'status':{'$gt':0}}
    if keyword:
        pack(Task, keyword, condition)
    total = Task.count(condition)
    tasks = Task.queryAll(user, condition, projection={'name':1, 'extra':1}, sort=[('update_time', -1)], skip=skip, limit=limit)
    result = {"appname":g.appname, "user":user, "task":tasks, 'total':total}
    result = json.dumps({'code':1, 'msg':'', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result

@task.route('/detail', methods=['DELETE', 'POST'])
@task.route('/detail/<tid>', methods=['GET', 'POST', 'DELETE'])
@withBase(basecfg.W, resutype='DICT', autocommit=True)
def taskdetail(tid=None):
    user = request.user
    tid = baseorm.IdField.verify(tid) if tid else tid
    if request.method == 'GET':
        user = request.user
        if tid is None:
            tid = request.args.get('tid')
        if tid is None:
            task = {'_id':'', 'aid':'', 'sid':'', 'name':'', 'extra':'', 'type':'ONCE', 'period':0, 'fid':'', 'params':'', 'worknum':6, 'queuetype':'M', 'worktype':'THREAD', 'timeout':30, 'category':'', 'push_url':'', 'pull_url':'', 'tag':'', 'own':True}
        else:
            projection = {'aid':1, 'sid':1, 'name':1, 'extra':1, 'type':1, 'period':1, 'fid':1, 'params':1, 'worknum':1, 'queuetype':1, 'worktype':1, 'timeout':1, 'category':1, 'push_url':1, 'tag':1, 'creator':1}
            task = Task.queryOne(user, {'_id':tid}, projection=projection)

            projection = {'name':1}
            task['article'] = {
                'label':'article',
                'key':'aid',
                'val':task['aid'],
                'url':'task/article',
                'options':[{'text':one['name'], 'value':one['_id']} for one in Article.queryAll(user, {}, projection=projection, limit=None)]
            }

            projection = {'name':1}
            task['flow'] = {
                'label':'flow',
                'key':'fid',
                'val':task['fid'],
                'url':'task/flow',
                'options':[{'text':one['name'], 'value':one['_id']} for one in Flow.queryAll(user, {'aid':task['aid']}, projection=projection)]
            }

            projection = {'name':1}
            task['section'] = {
                'label':'section',
                'key':'sid',
                'val':task['sid'],
                'url':'task/section',
                'options':[{'text':one['name'], 'value':one['_id']} for one in Section.queryAll(user, {'fid':task['fid']}, projection=projection)]
            }

            task['own'] = str(task['creator']) == user['_id']
            task['pull_url'] = 'http://%s/gdc/api/data/%s' % (request.host, str(task['_id']))
            del task['creator']
        task['queuetype'] = 'M' # QUEUETYPE.get(task['queuetype'], '')
        task['queuetype_options'] = [{'text':'local', 'value':'P'},
                                    {'text':'beanstalkd', 'value':'B'},
                                    {'text':'redis', 'value':'R'},
                                    {'text':'mongo', 'value':'M'}]
        task['worktype'] = 'THREAD' # WORKTYPE.get(task['worktype'], '')
        task['worktype_options'] = [{'text':'多线程', 'value':'THREAD'},
                                    {'text':'协程', 'value':'GEVENT'}]
        task['type_options'] = [{'text':'临时任务', 'value':'ONCE'},
                                {'text':'周期任务', 'value':'FOREVER'}]
        author = {}
        # for one in Permit.queryAll({'otype':'Task', 'oid':tid}, projection={'cid':1, '_id':0}):
        #     author[str(one['cid'])] = ''
        task['author'] = urllib.quote(json.dumps(author).encode('utf8'))

        projection = {'_id':1, 'username':1}
        task['creators'] = [{'text':one['username'], 'value':one['_id']} for one in Creator.queryAll(user, {'_id':{'$ne':user['_id']}}, projection=projection, limit=None)]
        task['select_updators'] = ','.join([str(one['cid']) for one in Permit.queryAll({'cid':{'$ne':user['_id']}, 'creator':user['_id'], 'oid':tid, 'otype':'Task', 'authority':{'$in':[2,3,6,7,10,11,14,15]}}, projection={'cid':1}, limit=None)])
        task['select_queryers'] = ','.join([str(one['cid']) for one in Permit.queryAll({'cid':{'$ne':user['_id']}, 'creator':user['_id'], 'oid':tid, 'otype':'Task', 'authority':{'$mod':[2, 1]}}, projection={'cid':1}, limit=None)])

        result = {"appname":g.appname, "user":user, "task":task}
        result = json.dumps({'code':1, 'msg':'', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
        return result
    elif request.method == 'POST':
        user = request.user
        name = request.form.get('name')
        extra = request.form.get('extra')
        category = request.form.get('category')
        tag = request.form.get('tag')
        period = request.form.get('period')
        push_url = request.form.get('push_url')
        aid = request.form.get('aid')
        fid = request.form.get('fid')
        sid = request.form.get('sid')
        params = request.form.get('params')
        timeout = request.form.get('timeout', 30)
        worknum = request.form.get('worknum', 6)
        queuetype = request.form.get('queuetype', 'P')
        worktype = 'THREAD'

        select_updators = request.form.get('select_updators')
        unselect_updators = request.form.get('unselect_updators')
        select_queryers = request.form.get('select_queryers')
        unselect_queryers = request.form.get('unselect_queryers')

        aid = baseorm.IdField.verify(aid) if aid is not None else aid
        fid = baseorm.IdField.verify(fid) if fid is not None else fid
        sid = baseorm.IdField.verify(sid) if sid is not None else sid

        if request.form.get('type') == 'ONCE':
            period = 0
            queuetype = 'P'
        else:
            queuetype = 'R'
        section = Section.queryOne(user, {'_id':sid})
        result = {'stat':1, 'desc':'success', 'data':{}}
        if tid is None:
            task = Task(name=name,
                extra=extra,
                category=category,
                tag=tag,
                type=request.form.get('type'),
                period=period,
                push_url=push_url,
                aid=aid,
                fid=fid,
                sid=sid,
                params=params,
                timeout=timeout,
                worknum=worknum,
                state=0,
                status=1,
                queuetype=queuetype,
                worktype=worktype,
                creator=user['_id'],
                updator=user['_id'],
                create_time=datetime.datetime.now())
            task['_id'] = Task.insert(user, task)
        else:
            task = {'name':name,
                'extra':extra,
                'category':category,
                'tag':tag,
                'type':request.form.get('type'),
                'period':period,
                'push_url':push_url,
                'params':params,
                'timeout':timeout,
                'worknum':worknum,
                'queuetype':queuetype,
                'worktype':worktype,
                'updator':user['_id'],
                'update_time':datetime.datetime.now()
            }
            if aid is not None:
                task['aid'] = aid
            if fid is not None:
                task['fid'] = fid
            if sid is not None:
                task['sid'] = sid
            Task.update(user, {'_id':tid}, {'$set':task})
            task['_id'] = tid
        unselect(unselect_queryers, 'Task', tid, user['_id'])
        unselect(unselect_updators, 'Task', tid, user['_id'])
        select(select_updators, 'Task', tid, user['_id'], 'update')
        select(select_queryers, 'Task', tid, user['_id'], 'query')
        result = {"appname":g.appname, "user":user, "task":task}
        result = json.dumps({'code':1, 'msg':'', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
        return result
    elif request.method == 'DELETE':
        if tid:
            Task.update(user, {'_id':tid}, {'$set':{'status':0}})
        else:
            ids = request.form.get('ids')
            for tid in ids.split(','):
                tid = baseorm.IdField.verify(tid)
                Task.update(user, {'_id':tid}, {'$set':{'status':0}})
        result = {"appname":g.appname, "user":user, "task":{}}
        result = json.dumps({'code':1, 'msg':'Delete it successfully.', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
        return result
    else:
        pass


@task.route('/article', methods=['GET'])
@withBase(basecfg.R, resutype='DICT')
def taskarticle():
    user = request.user
    uid = request.args.get('uid')
    if uid is None:
        articles = Article.queryAll(user, {}, projection={'name':1})
    else:
        uid = baseorm.IdField.verify(uid)
        articles = Article.queryAll(user, {'uid':uid}, projection={'name':1})
    result = {"appname":g.appname, "user":user, "options":[{'text':one['name'], 'value':one['_id']} for one in articles]}
    result = json.dumps({'code':1, 'msg':'', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result


@task.route('/flow', methods=['GET'])
@withBase(basecfg.R, resutype='DICT')
def taskflow():
    user = request.user
    aid = request.args.get('aid')
    if aid is None:
        flows = Flow.queryAll(user, {}, projection={'name':1})
    else:
        aid = baseorm.IdField.verify(aid)
        flows = Flow.queryAll(user, {'aid':aid}, projection={'name':1})
    result = {"appname":g.appname, "user":user, "options":[{'text':one['name'], 'value':one['_id']} for one in flows]}
    result = json.dumps({'code':1, 'msg':'', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result


@task.route('/section', methods=['GET'])
@withBase(basecfg.R, resutype='DICT')
def tasksection():
    user = request.user
    fid = request.args.get('fid')
    if fid is None:
        sections = Section.queryAll(user, {}, projection={'name':1})
    else:
        fid = baseorm.IdField.verify(fid)
        sections = Section.queryAll(user, {'fid':fid}, projection={'name':1})
    result = {"appname":g.appname, "user":user, "options":[{'text':one['name'], 'value':one['_id']} for one in sections]}
    result = json.dumps({'code':1, 'msg':'', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result
