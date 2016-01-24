#!/usr/bin/python
# coding=utf-8
import time, datetime
import sys, json
import random
import traceback

from datakit.mysql.suit import withMysql, dbpc
from hawkeye import initDB
from webcrawl.handleRequest import PROXY
from webcrawl.work import Workflows
import task

WDB = 'local'
RDB = 'local'
initDB()

@withMysql(WDB, resutype='DICT', autocommit=True)
def choose():
    limit = datetime.datetime.now() - datetime.timedelta(days=3)
    # proxys = dbpc.handler.queryAll(""" select * from grab_proxy where usespeed < 1 and update_time > '2015-12-15 01:11:00' order by usespeed asc, refspeed asc limit 200; """)
    proxys = dbpc.handler.queryAll(""" select * from grab_proxy where usespeed < 1 and update_time > '2015-12-15 01:11:00' order by update_time desc; """)
    # return random.choice(proxys)
    return proxys[0]

@withMysql(WDB, resutype='DICT', autocommit=True)
def log(pid, elapse):
    create_time = datetime.datetime.now()
    dbpc.handler.insert(""" insert into grab_proxy_log(`pid`, `elapse`, `create_time`)values(%s, %s, %s) """, (pid, elapse, create_time))
    proxy = dbpc.handler.queryOne(""" select * from grab_proxy_log where id = %s """, (pid, ))
    proxy['usespeed'] = (proxy['usespeed'] * proxy['usenum'] + elapse)/float(proxy['usenum']+1)
    proxy['usenum'] = proxy['usenum'] + 1
    dbpc.handler.update(""" update grab_proxy_log set usespeed = %s, usenum = %s, update_time=now() where id = %s """, (usespeed, usenum, pid))

# PROXY.use = True
# PROXY.choose = choose
# PROXY.log = log
# PROXY.worker.start()

@withMysql(WDB, resutype='DICT', autocommit=True)
def record(tid, succ, fail, timeout, elapse=None, sname=None, create_time=None):
    create_time = create_time or datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if sname is None:
        dbpc.handler.insert(""" insert into grab_statistics(`tid`,`succ`,`fail`,`timeout`,`elapse`,`create_time`)
                                                    values( %s,   %s,    %s,    %s,   %s,        %s)""", (tid, succ, fail, timeout, elapse, create_time))
        return dbpc.handler.queryOne(""" select * from grab_statistics where tid = %s and create_time = %s """, (tid, create_time))['id']
    else:
        dbpc.handler.insert(""" insert into grab_log(`gsid`,`sname`,`succ`,`fail`,`timeout`,`create_time`)
                                                    values( %s, %s,   %s,    %s,    %s,    %s)""", (tid, sname, succ, fail, timeout, create_time))

@withMysql(WDB, resutype='DICT', autocommit=True)
def schedule():
    return dbpc.handler.queryAll(""" select gt.id, gt.aid, gt.sid, gt.flow, gt.params, gt.worknum, gt.queuetype, gt.worktype, gt.timeout, ga.name as a, ga.filepath, gu.name as u, gt.update_time from grab_task gt join grab_article ga join grab_unit gu on gt.aid = ga.id and ga.uid = gu.id and gt.status > 0; """)

@withMysql(WDB, resutype='DICT', autocommit=True)
def changestate(tid, status, extra=None):
    return dbpc.handler.update(""" update grab_task set `status`=%s where id = %s; """, (status, tid))

def task():
    workflow = Workflows(20, 'R', 'THREAD')
    workflow.start()
    load_spider = {}
    while True:
        for task in schedule():
            module_name = 'task.%s.%s' % (task['u'], task['filepath'].replace('.py', ''))
            cls_name = 'Spider%s' % task['a'].capitalize()
            spider = local_spider.get(cls_name)
            if spider is None:
                module = __import__(module_name, fromlist=['task.%s' % task['u']])
                cls = getattr(module, cls_name)
                spider = cls(worknum=int(task['worknum']), queuetype=task['queuetype'], worktype=task['worktype'], tid=int(task['id']))
                local_spider.set(cls_name, spider)
            try:
                changestate(task['id'], 2)
                if task.get('type', 'forever') == 'forever':
                    span = ((datetime.datetime.now() - task['update_time']).seconds)/3600
                    if span < task.get('period', 12):
                        continue
                    weight = spider.weight(task['flow'], once=True)
                    section = spider.section(task['flow'], task.get('step', 0))
                    if task['params'] is None or task['params'].strip() == '':
                        workflow.task(weight, task['flow'], task.get('step', 0))
                    elif task['params'].startswith('{'):
                        workflow.task(weight, task['flow'], task.get('step', 0), **json.loads(task['params']))
                    elif task['params'].startswith('('):
                        workflow.task(weight, task['flow'], task.get('step', 0), *tuple(task['params'][1:-1].split(',')))
                    else:
                        workflow.task(weight, task['flow'], task.get('step', 0), task['params'])
                else:
                    if task['params'] is None or task['params'].strip() == '':
                        spider.fetchDatas(task['flow'], task.get('step', 0))
                    elif task['params'].startswith('{'):
                        spider.fetchDatas(task['flow'], task.get('step', 0), **json.loads(task['params']))
                    elif task['params'].startswith('('):
                        spider.fetchDatas(task['flow'], task.get('step', 0), *tuple(task['params'][1:-1].split(',')))
                    else:
                        spider.fetchDatas(task['flow'], task.get('step', 0), task['params'])
                    spider.statistic()
                    changestate(task['id'], 0)
            except:
                t, v, b = sys.exc_info()
                err_messages = traceback.format_exception(t, v, b)
                extra = ','.join(err_messages)
                print extra
                changestate(task['id'], 3, extra=extra)
            else:
                gsid = record(task['id'], spider.stat['total']['succ'], spider.stat['total']['fail'], spider.stat['total']['timeout'], spider.totaltime)
                for name in spider.stat.keys():
                    if not name == 'total':
                        record(gsid, spider.stat[name]['succ'], spider.stat[name]['fail'], spider.stat[name]['timeout'], sname=name.lower().replace('fetch', '').replace(task['flow'], ''))
        time.sleep(60)

if __name__ == '__main__':
    task()