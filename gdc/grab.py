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
LIMIT = 600
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

def stat(task, spider, create_time):
    gsid = record(task['id'], spider.stat['total']['succ'], spider.stat['total']['fail'], spider.stat['total']['timeout'], spider.totaltime, create_time=create_time)
    for name in spider.stat.keys():
        if not name == 'total':
            record(gsid, spider.stat[name]['succ'], spider.stat[name]['fail'], spider.stat[name]['timeout'], sname=name, create_time=create_time)

@withMysql(WDB, resutype='DICT', autocommit=True)
def schedule():
    return dbpc.handler.queryAll(""" select gt.id, gt.type, gt.period, gt.aid, gt.sid, gt.flow, gs.step, gt.params, gt.worknum, gt.queuetype, gt.worktype, gt.timeout, ga.name as a, ga.filepath, gu.name as u, gt.update_time from grab_task gt join grab_section gs on gt.sid = gs.id join grab_article ga on gt.aid = ga.id join grab_unit gu on ga.uid = gu.id where gt.status > 0; """)

@withMysql(WDB, resutype='DICT', autocommit=True)
def changestate(tid, status, extra=None):
    return dbpc.handler.update(""" update grab_task set `status`=%s where id = %s; """, (status, tid))

def task():
    workflow = Workflows(6, 'R', 'THREAD')
    workflow.start()
    last_stat = datetime.datetime.now()
    local_spider = {}
    while True:
        for task in schedule():
            module_name = 'task.%s.%s' % (task['u'], task['filepath'].replace('.py', ''))
            cls_name = 'Spider%s' % task['a'].capitalize()
            if task.get('type', 'FOREVER') == 'FOREVER':
                spider = local_spider.get(cls_name, None)
                if spider is None:
                    module = __import__(module_name, fromlist=['task.%s' % task['u']])
                    cls = getattr(module, cls_name)
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
                        spider.fetchDatas(task['flow'], step, task['params'], **{'additions':additions})
                    spider.statistic()
                    changestate(task['id'], 0)
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
                        stat(task, spider, last_stat)
                    
        time.sleep(60)

if __name__ == '__main__':
    task()