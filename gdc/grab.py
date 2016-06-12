#!/usr/bin/env python
# coding=utf-8

import time, datetime, datetime, copy
import os, sys, json
import random
import traceback

from model.setting import withData, datacfg, WORKNUM, WORKQUEUE
from model.log import ProxyLog
from model.data import Proxy
from webcrawl.request import PROXY
from webcrawl import request
from webcrawl.task import Workflows, DataQueue

from setting import USER, SECRET, HOST
from log import Producer
from register import getSection, getArticle, getUnit, getDatamodel
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

def schedule():
    user_id = 0
    condition = {'status':{'$gt':0}}
    projection = {'_id':1, 'type':1, 'period':1, 'aid':1, 'sid':1, 'flow':1, 'params':1, 'worknum':1, 'queuetype':1, 'worktype':1, 'timeout':1, 'category':1, 'tag':1, 'name':1, 'extra':1, 'update_time':1, 'push_url':1}
    tasks = request.post('%sgdc/api/task' % HOST, {'condition':json.dumps(condition), 'projection':json.dumps(projection), 'limit':'all'}, format='JSON')
    tasks = tasks['task']
    for task in tasks:
        section = getSection(task['sid'])

        article = getArticle(task['aid'])

        unit = getUnit(article['uid'])
        
        datamodel = getDatamodel(unit['dmid'])
        
        task['step'] = section['step']
        task['index'] = section['index']
        task['additions'] = section.get('additions') or '{}'
        task['filepath'] = article['filepath']
        task['article'] = article['clsname']
        task['unit'] = unit['name']
    return tasks


def changestate(tid, status, extra=None):
    request.post('%sgdc/api/task/%s' % (HOST, str(tid)), {'data':json.dumps({'status':status})})


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
            spider = local_spider.get(cls_name, None)
            if spider is None:
                spider = cls(worknum=task['worknum'], queuetype='P', worktype='THREAD', tid=int(task['_id']))
                local_spider[cls_name] = spider

            if task.get('type', 'FOREVER') == 'FOREVER' and ((datetime.datetime.now() - task['update_time']).seconds)/3600 < task.get('period', 12):
                continue

            try:
                changestate(task['_id'], 2)
                step = task.get('step', 1) - 1
                additions = {}
                additions['name'] = task['name']
                additions['cat'] = task['category'].split(',')
                additions['tag'] = task['tag'].split(',')
                if task['params'].startswith('{') and task['params'].endswith('}'):
                    args = []
                    kwargs = json.loads(task['params'])
                elif task['index'] is None or task['index'].isdigit():
                    args = [task['params'], ]
                    kwargs = {}
                else:
                    args = []
                    kwargs = {task['index']:task['params']}
                kwargs['additions'] = dict(json.loads(task['additions']), **additions)

                args.insert(0, datetime.datetime.now().strftime('%Y%m%d'))

                if task.get('type', 'FOREVER') == 'FOREVER':
                    section = spider.section(task['flow'], step)
                    args.insert(0, task['_id'])
                    args.insert(0, section)
                    fun = workflow.task
                    workflow.task(weight, section, task['_id'], *tuple(task['params'][1:-1].split(',')), **{'additions':additions})
                else:
                    args.insert(0, step)
                    args.insert(0, task['flow'])
                    fun = spider.fetchDatas
                
                fun(*args, **kwargs)
            except:
                t, v, b = sys.exc_info()
                err_messages = traceback.format_exception(t, v, b)
                extra = ','.join(err_messages)
                changestate(task['_id'], 3, extra=extra)
                    
        time.sleep(60)

if __name__ == '__main__':
    task()
    