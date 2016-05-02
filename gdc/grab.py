#!/usr/bin/env python
# coding=utf-8

import time, datetime, copy
import os, sys, json
import random
import traceback

from model.setting import withData, datacfg, WORKNUM, WORKQUEUE
from model.log import ProxyLog, Statistics, Log
from model.data import Proxy
from webcrawl.request import PROXY, requGet, requPost
from webcrawl.task import Workflows, DataQueue

from setting import USER, SECRET, HOST
from log import Producer
import task

CURRPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))

DataQueue.update(**WORKQUEUE)

LIMIT = 600

INIT = """#!/usr/bin/env python
# coding=utf-8
"""

@withData(datacfg.W, resutype='DICT', autocommit=True)
def choose():
    limit = datetime.datetime.now() - datetime.timedelta(days=3)
    # proxys = dbpc.handler.queryAll(""" select * from grab_proxy where usespeed < 1 and update_time > '2015-12-15 01:11:00' order by usespeed asc, refspeed asc limit 200; """)
    # proxys = Proxy.queryAll({'$and':[{'usespeed':{'$lt':1}}, {'usespeed':{'$gt':'2015-12-15 01:11:00'}}]}, sort=[('usespeed', 1), ('refspeed', 1)], skip=0, limit=200)
    # proxys = dbpc.handler.queryAll(""" select * from grab_proxy where usespeed < 1 and update_time > '2015-12-15 01:11:00' order by update_time desc; """)
    proxys = Proxy.queryAll({'$and':[{'usespeed':{'$lt':1}}, {'usespeed':{'$gt':'2015-12-15 01:11:00'}}]}, sort=[('update_time', -1)])
    # return random.choice(proxys)
    return proxys[0]

@withData(datacfg.W, resutype='DICT', autocommit=True)
def log(pid, elapse):
    create_time = datetime.datetime.now()
    proxylog = ProxyLog(pid=pid, elapse=elapse, create_time=create_time)
    ProxyLog.insert(proxylog)
    
    proxy = Proxy.queryOne({'_id':pid})
    proxy['usespeed'] = (proxy['usespeed'] * proxy['usenum'] + elapse)/float(proxy['usenum']+1)
    proxy['usenum'] = proxy['usenum'] + 1
    Proxy.update({'_id':pid}, {'$set':{'usespeed':proxy['usespeed'], 'usenum':proxy['usenum'], 'update_time':create_time}})

# PROXY.use = True
# PROXY.choose = choose
# PROXY.log = log
# PROXY.worker.start()

@withData(datacfg.W, resutype='DICT', autocommit=True)
def record(tid, succ, fail, timeout, elapse=None, sname=None, create_time=None):
    create_time = create_time or datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if sname is None:
        statistics = Statistics(tid=tid, succ=succ, fail=fail, timeout=timeout, elapse=elapse, create_time=create_time)
        return Statistics.insert(statistics)
    else:
        log = Log(gsid=tid, sname=sname, succ=succ, fail=fail, timeout=timeout, create_time=create_time)
        Log.insert(log)

def stat(task, spider, create_time=None):
    create_time = create_time or datetime.datetime.now()
    gsid = record(task['_id'], spider.stat['total']['succ'], spider.stat['total']['fail'], spider.stat['total']['timeout'], elapse=spider.totaltime, create_time=create_time)
    for name in spider.stat.keys():
        if not name == 'total':
            record(gsid, spider.stat[name]['succ'], spider.stat[name]['fail'], spider.stat[name]['timeout'], sname=name, create_time=create_time)

def schedule():
    user_id = 0
    condition = {'status':{'$gt':0}}
    projection = {'_id':1, 'type':1, 'period':1, 'aid':1, 'sid':1, 'flow':1, 'params':1, 'worknum':1, 'queuetype':1, 'worktype':1, 'timeout':1, 'category':1, 'tag':1, 'name':1, 'extra':1, 'update_time':1, 'push_url':1}
    tasks = requPost('%sgdc/api/task' % HOST, {'condition':json.dumps(condition), 'projection':json.dumps(projection), 'limit':'all'}, format='JSON')
    tasks = tasks['task']
    for task in tasks:
        projection = {'step':1, 'index':1, 'additions':1}
        section = requPost('%sgdc/api/section/%s' % (HOST, str(task['sid'])), {'projection':json.dumps(projection), 'limit':'one'}, format='JSON')
        section = section['section']

        projection = {'uid':1, 'filepath':1, 'name':1, 'clsname':1, 'filepath':1, 'fileupdate':1}
        article = requPost('%sgdc/api/article/%s' % (HOST, str(task['aid'])), {'projection':json.dumps(projection), 'limit':'one'}, format='JSON')
        article = article['article']
        if article['fileupdate']:
            result = requGet('%sgds/static/exe/%s' % (HOST, article['filepath']), format='TEXT')
            filepath = article['filepath']
            fi = open(os.path.join(CURRPATH, filepath), 'w')
            fi.write(result)
            fi.close()
            requPost('%sgdc/api/article/%s' % (HOST, str(task['aid'])), {'data':json.dumps({'fileupdate':0})})

        projection = {'name':1, 'filepath':1, 'fileupdate':1, 'dmid':1}
        unit = requPost('%sgdc/api/unit/%s' % (HOST, str(article['uid'])), {'projection':json.dumps(projection), 'limit':'one'}, format='JSON')
        unit = unit['unit']
        if unit['fileupdate']:
            result = requGet('%sgds/static/exe/%s' % (HOST, unit['filepath']), format='TEXT')
            filepath = unit['filepath']
            fi = open(os.path.join(CURRPATH, filepath), 'w')
            fi.write(result)
            fi.close()
            fi = open(os.path.join(os.path.dirname(os.path.join(CURRPATH, filepath)), "__init__.py"), 'w')
            fi.write('#!/usr/bin/env python\n# coding=utf8')
            fi.close()
            requPost('%sgdc/api/unit/%s' % (HOST, str(article['uid'])), {'data':json.dumps({'fileupdate':0})})
            filepath = os.path.join(os.path.dirname(filepath), '__init__.py')
            if not os.path.exists(filepath):
                fi = open(os.path.join(CURRPATH, filepath), 'w')
                fi.write(INIT)
                fi.close()

        projection = {'filepath':1, 'fileupdate':1}
        datamodel = requPost('%sgdc/api/datamodel/%s' % (HOST, str(unit['dmid'])), {'projection':json.dumps(projection), 'limit':'one'}, format='JSON')
        datamodel = datamodel['datamodel']
        if datamodel['fileupdate']:
            result = requGet('%sgds/static/exe/%s' % (HOST, datamodel['filepath']), format='TEXT')
            filepath = datamodel['filepath']
            fi = open(os.path.join(CURRPATH, filepath), 'w')
            fi.write(result)
            fi.close()
            requPost('%sgdc/api/datamodel/%s' % (HOST, str(unit['dmid'])), {'data':json.dumps({'fileupdate':0})})

        task['step'] = section['step']
        task['index'] = section['index']
        task['additions'] = section.get('additions') or '{}'
        task['filepath'] = article['filepath']
        task['article'] = article['clsname']
        task['unit'] = unit['name']
    return tasks

def changestate(tid, status, extra=None):
    requPost('%sgdc/api/task/%s' % (HOST, str(tid)), {'data':json.dumps({'status':status})})

def task():
    workflow = Workflows(WORKNUM, 'R', 'THREAD')
    workflow.start()
    last_stat = datetime.datetime.now()
    local_spider = {}
    while True:
        for task in schedule():
            module_name = task['filepath'].replace('.py', '').replace('/', '.')
            task['update_time'] = datetime.datetime.strptime(task['update_time'], '%Y-%m-%d %H:%M:%S')
            cls_name = task['article']
            module = __import__(module_name, fromlist=['task.%s' % task['unit']])
            cls = getattr(module, cls_name)
            if task.get('type', 'FOREVER') == 'FOREVER':
                spider = local_spider.get(cls_name, None)
                if spider is None:
                    spider = cls(worknum=20, queuetype='R', worktype='THREAD', tid=int(task['_id']))
                    local_spider[cls_name] = spider
            else:
                spider = cls(worknum=task['worknum'], queuetype=task['queuetype'], worktype=task['worktype'], tid=int(task['_id']))
            try:
                changestate(task['_id'], 2)
                step = task.get('step', 1) - 1
                additions = {}
                additions['name'] = task['name']
                additions['cat'] = task['category'].split(',')
                additions['tag'] = task['tag'].split(',')
                additions = dict(json.loads(task['additions']), **additions)
                if task.get('type', 'FOREVER') == 'FOREVER':
                    if ((datetime.datetime.now() - task['update_time']).seconds)/3600 < task.get('period', 12):
                        continue
                    weight = spider.weight(task['flow'], once=True)
                    section = spider.section(task['flow'], step)
                    if task['params'] is None or task['params'].strip() == '':
                        workflow.task(weight, section, task['_id'], **{'additions':additions})
                    elif task['params'].startswith('{'):
                        workflow.task(weight, section, task['_id'], **dict(json.loads(task['params']), **{'additions':additions}))
                    elif task['params'].startswith('('):
                        workflow.task(weight, section, task['_id'], *tuple(task['params'][1:-1].split(',')), **{'additions':additions})
                    else:
                        if task['index'] is None or task['index'].isdigit():
                            workflow.task(weight, section, task['_id'], task['params'], **{'additions':additions})
                        else:
                            workflow.task(weight, section, task['_id'], **{task['index']:task['params'], 'additions':additions})
                else:
                    if task['params'] is None or task['params'].strip() == '':
                        spider.fetchDatas(task['flow'], step, **{'additions':additions})
                    elif task['params'].startswith('{'):
                        spider.fetchDatas(task['flow'], step, **dict(json.loads(task['params']), **{'additions':additions}))
                    elif task['params'].startswith('('):
                        spider.fetchDatas(task['flow'], step, *tuple(task['params'][1:-1].split(',')), **{'additions':additions})
                    else:
                        if task['index'] is None or task['index'].isdigit():
                            spider.fetchDatas(task['flow'], step, task['params'], **{'additions':additions})
                        else:
                            spider.fetchDatas(task['flow'], step, **{task['index']:task['params'], 'additions':additions})
                    spider.statistic()
                    changestate(task['_id'], 0)
                    if task.get('push_url') is not None:
                        requPost(task['push_url'], {'type':'video', 'tid':task['_id']})
            except:
                t, v, b = sys.exc_info()
                err_messages = traceback.format_exception(t, v, b)
                extra = ','.join(err_messages)
                print extra
                changestate(task['_id'], 3, extra=extra)
            else:
                if not task.get('type', 'FOREVER') == 'FOREVER':
                    stat(task, spider)
            finally:
                if ((datetime.datetime.now() - last_stat).seconds) >= LIMIT:
                    last_stat = datetime.datetime.now()
                    for spider in local_spider.values():
                        spider.statistic()
                        stat(task, spider, last_stat)
                    
        time.sleep(60)

if __name__ == '__main__':
    task()
    