#!/usr/bin/python
# coding=utf-8
import time, datetime
import sys
import traceback

from datakit.mysql.suit import withMysql, dbpc
from hawkeye import initDB
import task

WDB = 'local'
RDB = 'local'
initDB()

@withMysql(WDB, resutype='DICT', autocommit=True)
def log(tid, succ, fail, timeout, elapse=None, sname=None, create_time=None):
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
        for t in schedule():
            md = __import__('task.%s.%s' % (t['u'], t['filepath'].replace('.py', '')), fromlist=['task.%s' % t['u']])
            cls = getattr(md, 'Spider%s' % t['a'].capitalize())
            try:
                changestate(t['id'], 2)
                spider = cls(worknum=int(t['worknum']), queuetype=t['queuetype'], worktype=t['worktype'], tid=int(t['id']))
                spider.fetchDatas(t['flow'], t['params'])
                spider.statistic()
                changestate(t['id'], 1)
            except:
                t, v, b = sys.exc_info()
                err_messages = traceback.format_exception(t, v, b)
                extra = ','.join(err_messages)
                changestate(t['id'], 3, extra=extra)
            gsid = log(t['id'], spider.stat['total']['succ'], spider.stat['total']['fail'], spider.stat['total']['timeout'], spider.totaltime)
            for name in spider.stat.keys():
                if not name == 'total':
                    log(gsid, spider.stat[name]['succ'], spider.stat[name]['fail'], spider.stat[name]['timeout'], sname=name.lower().replace('fetch', '').replace(t['flow'], ''))
        time.sleep(60)

if __name__ == '__main__':
    task()
