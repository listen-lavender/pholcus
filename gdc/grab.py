#!/usr/bin/python
# coding=utf-8
import time, datetime
import sys, json
import random
import traceback

from datakit.mysql.suit import withMysql, dbpc
from hawkeye import initDB
from webcrawl.handleRequest import PROXY
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
        # return dbpc.handler.queryOne(""" select * from grab_log where gsid = %s and create_time = %s """, (tid, create_time))['id']
        return None

@withMysql(WDB, resutype='DICT', autocommit=True)
def schedule():
    return dbpc.handler.queryAll(""" select gt.id, gt.aid, gt.sid, gt.flow, gt.params, gt.worknum, gt.queuetype, gt.worktype, gt.timeout, ga.name as a, ga.filepath, gu.name as u from grab_task gt join grab_article ga join grab_unit gu on gt.aid = ga.id and ga.uid = gu.id and gt.status > 0; """)

@withMysql(WDB, resutype='DICT', autocommit=True)
def changestate(tid, status, extra=None):
    return dbpc.handler.update(""" update grab_task set `status`=%s where id = %s; """, (status, tid))

def task():
    while True:
        for task in schedule():
            md = __import__('task.%s.%s' % (task['u'], task['filepath'].replace('.py', '')), fromlist=['task.%s' % task['u']])
            cls = getattr(md, 'Spider%s' % task['a'].capitalize())
            try:
                changestate(task['id'], 2)
                spider = cls(worknum=int(task['worknum']), queuetype=task['queuetype'], worktype=task['worktype'], tid=int(task['id']))
                if '{' in task['params']:
                    spider.fetchDatas(task['flow'], **json.loads(task['params']))
                elif '(' in task['params']:
                    spider.fetchDatas(task['flow'], *tuple(task['params'][1:-1].split(',')))
                else:
                    spider.fetchDatas(task['flow'], task['params'])
                spider.statistic()
                changestate(task['id'], 1)
            except:
                t, v, b = sys.exc_info()
                err_messages = traceback.format_exception(t, v, b)
                extra = ','.join(err_messages)
                print extra
                changestate(task['id'], 3, extra=extra)
            print dir(spider)
            gsid = record(task['id'], spider.stat['total']['succ'], spider.stat['total']['fail'], spider.stat['total']['timeout'], spider.totaltime)
            for name in spider.stat.keys():
                if not name == 'total':
                    record(gsid, spider.stat[name]['succ'], spider.stat[name]['fail'], spider.stat[name]['timeout'], sname=name.lower().replace('fetch', '').replace(task['flow'], ''))
        time.sleep(60)

if __name__ == '__main__':
    task()
