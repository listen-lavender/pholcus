#!/usr/bin/python
# coding=utf-8
import time, datetime

from datakit.mysql.suit import withMysql, dbpc
from hawkeye import initDB
import task

WDB = 'local'
RDB = 'local'
initDB()

@withMysql(WDB, resutype='DICT', autocommit=True)
def log(tid, succ, fail, timeout, elapse=None, sname=None, create_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
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
    return dbpc.handler.queryAll(""" select gt.id, gt.aid, gt.sid, gt.flow, gt.params, gt.worknum, gt.queuetype, gt.worktype, gt.timeout, ga.name as a, ga.filepath, gu.name as u from grab_task gt join grab_article ga join grab_unit gu on gt.aid = ga.id and ga.uid = gu.id and gu.name = 'hotel' ; """)

def task():
    while True:
        for t in schedule():
            md = __import__('task.%s.%s' % (t['u'], t['filepath'].replace('.py', '')), fromlist=['task.%s' % t['u']])
            cls = getattr(md, 'Spider%s' % t['a'].capitalize())
            spider = cls(worknum=int(t['worknum']), queuetype=t['queuetype'], worktype=t['worktype'], tid=int(t['id']))
            spider.fetchDatas(t['flow'], t['params'])
            spider.statistic()
            gsid = log(t['id'], spider.stat['total']['succ'], spider.stat['total']['fail'], spider.stat['total']['timeout'], spider.totaltime)
            for name in spider.stat.keys():
                if not name == 'total':
                    log(gsid, spider.stat[name]['succ'], spider.stat[name]['fail'], spider.stat[name]['timeout'], sname=name.lower().replace('fetch', '').replace(t['flow'], ''))
        time.sleep(0.1)

if __name__ == '__main__':
    task()
