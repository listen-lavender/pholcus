#!/usr/bin/python
# coding=utf-8
import time, datetime
import sys, json
import random
import traceback
sys.path.append('../')

from dbskit.mysql.suit import withMysql, dbpc
from model.settings import withData, RDB, WDB
from model.base import Task, Section, Article, Unit,
from model.log import Proxy, ProxyLog, Statistics, Log
from hawkeye import initDB
from webcrawl.handleRequest import PROXY
from webcrawl.work import Workflows
import task

WDB = 'local'
RDB = 'local'
LIMIT = 600
initDB()

@withData(WDB, resutype='DICT', autocommit=True)
def choose():
    limit = datetime.datetime.now() - datetime.timedelta(days=3)
    # proxys = dbpc.handler.queryAll(""" select * from grab_proxy where usespeed < 1 and update_time > '2015-12-15 01:11:00' order by usespeed asc, refspeed asc limit 200; """)
    # proxys = Proxy.queryAll({'$and':[{'usespeed':{'$lt':1}}, {'usespeed':{'$gt':'2015-12-15 01:11:00'}}]}, sort=[('usespeed', 1), ('refspeed', 1)], skip=0, limit=200)
    # proxys = dbpc.handler.queryAll(""" select * from grab_proxy where usespeed < 1 and update_time > '2015-12-15 01:11:00' order by update_time desc; """)
    proxys = Proxy.queryAll({'$and':[{'usespeed':{'$lt':1}}, {'usespeed':{'$gt':'2015-12-15 01:11:00'}}]}, sort=[('update_time', -1)])
    # return random.choice(proxys)
    return proxys[0]

@withData(WDB, resutype='DICT', autocommit=True)
def log(pid, elapse):
    create_time = datetime.datetime.now()
    # dbpc.handler.insert(""" insert into grab_proxy_log(`pid`, `elapse`, `create_time`)values(%s, %s, %s) """, (pid, elapse, create_time))
    proxylog = ProxyLog(pid=pid, elapse=elapse, create_time=create_time)
    ProxyLog.insert(proxylog)
    
    proxy = Proxy.queryOne({'_id':pid})
    # proxy = dbpc.handler.queryOne(""" select * from grab_proxy where id = %s """, (pid, ))
    proxy['usespeed'] = (proxy['usespeed'] * proxy['usenum'] + elapse)/float(proxy['usenum']+1)
    proxy['usenum'] = proxy['usenum'] + 1
    # dbpc.handler.update(""" update grab_proxy_log set usespeed = %s, usenum = %s, update_time=now() where id = %s """, (usespeed, usenum, pid))
    Proxy.update({'_id':pid}, {'$set':{'usespeed':proxy['usespeed'], 'usenum':proxy['usenum'], 'update_time':create_time}})

# PROXY.use = True
# PROXY.choose = choose
# PROXY.log = log
# PROXY.worker.start()

@withData(WDB, resutype='DICT', autocommit=True)
def record(tid, succ, fail, timeout, elapse=None, sname=None, create_time=None):
    create_time = create_time or datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if sname is None:
        statistics = Statistics(tid=tid, succ=succ, fail=fail, timeout=timeout, elapse=elapse, create_time=create_time)
        # dbpc.handler.insert(""" insert into grab_statistics(`tid`,`succ`,`fail`,`timeout`,`elapse`,`create_time`)
        #                                             values( %s,   %s,    %s,    %s,   %s,        %s)""", (tid, succ, fail, timeout, elapse, create_time))
        return Statistics.insert(statistic)
    else:
        log = Log(gsid=gsid, sname=sname, succ=succ, fail=fail, timeout=timeout, create_time=create_time)
        # dbpc.handler.insert(""" insert into grab_log(`gsid`,`sname`,`succ`,`fail`,`timeout`,`create_time`)
        #                                             values( %s, %s,   %s,    %s,    %s,    %s)""", (tid, sname, succ, fail, timeout, create_time))
        Log.insert(log)

def stat(task, spider, create_time=None):
    create_time = create_time or datetime.datetime.now()
    gsid = record(task['id'], spider.stat['total']['succ'], spider.stat['total']['fail'], spider.stat['total']['timeout'], elapse=spider.totaltime, create_time=create_time)
    for name in spider.stat.keys():
        if not name == 'total':
            record(gsid, spider.stat[name]['succ'], spider.stat[name]['fail'], spider.stat[name]['timeout'], sname=name, create_time=create_time)

@withBase(WDB, resutype='DICT', autocommit=True)
def schedule():
    user_id = 0
    tasks = Task.queryAll(user_id, {'status':{'$gt':0}}, projection={'_id':1, 'type':1, 'period':1, 'aid':1, 'sid':1, 'flow':1, 'params':1, 'worknum':1, 'queuetype':1, 'worktype':1, 'timeout':1, 'category':1, 'tag':1, 'name':1, 'extra':1, 'update_time':1, 'push_url':1})
    for task in tasks:
        section = Section.queryOne(user_id, {'_id':task['sid']}, projection={'step':1, 'index':1})
        article = Article.queryOne(user_id, {'_id':task['aid']}, projection={'uid':1, 'filepath':1, 'name':1})
        unit = Unit.queryOne(user_id, {'_id':article['uid']}, projection={'name':1})
        task['step'] = section['step']
        task['index'] = section['index']
        task['filepath'] = article['filepath']
        task['a'] = article['name']
        task['u'] = unit['name']
    return tasks

@withBase(WDB, resutype='DICT', autocommit=True)
def changestate(tid, status, extra=None):
    Task.update(user['_id'], {'_id':tid}, {'$set':{'status':status}})

def task():
    workflow = Workflows(6, 'R', 'THREAD')
    workflow.start()
    last_stat = datetime.datetime.now()
    local_spider = {}
    while True:
        for task in schedule():
            module_name = 'task.%s.%s' % (task['u'], task['filepath'].replace('.py', ''))
            cls_name = 'Spider%s' % task['a'].capitalize()
            module = __import__(module_name, fromlist=['task.%s' % task['u']])
            cls = getattr(module, cls_name)
            if task.get('type', 'FOREVER') == 'FOREVER':
                spider = local_spider.get(cls_name, None)
                if spider is None:
                    spider = cls(worknum=20, queuetype='R', worktype='THREAD', tid=int(task['id']))
                    local_spider[cls_name] = spider
            else:
                spider = cls(worknum=6, queuetype='P', worktype='THREAD', tid=int(task['id']))
            try:
                changestate(task['id'], 2)
                step = task.get('step', 1) - 1
                if task.get('type', 'FOREVER') == 'FOREVER':
                    if ((datetime.datetime.now() - task['update_time']).seconds)/3600 < task.get('period', 12):
                        continue
                    weight = spider.weight(task['flow'], once=True)
                    section = spider.section(task['flow'], step)
                    if task['params'] is None or task['params'].strip() == '':
                        workflow.task(weight, section)
                    elif task['params'].startswith('{'):
                        workflow.task(weight, section, **json.loads(task['params']))
                    elif task['params'].startswith('('):
                        workflow.task(weight, section, *tuple(task['params'][1:-1].split(',')))
                    else:
                        workflow.task(weight, section, task['params'])
                else:
                    additions = {}
                    additions['name'] = task['name']
                    additions['cat'] = task['category'].split(',')
                    additions['tag'] = task['tag'].split(',')
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
                    changestate(task['id'], 0)
                    if task.get('push_url') is not None:
                        requests.post(task['push_url'], {'type':'video', 'tid':task['id']})
            except:
                t, v, b = sys.exc_info()
                err_messages = traceback.format_exception(t, v, b)
                extra = ','.join(err_messages)
                print extra
                changestate(task['id'], 3, extra=extra)
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
    