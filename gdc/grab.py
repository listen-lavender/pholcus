#!/usr/bin/python
# coding=utf-8

from datakit.mysql.suit import withMysql, dbpc
from init import initDB
import task

WDB = 'local'
RDB = 'local'
initDB()
    
@withMysql(WDB, resutype='DICT')
def task():
    while True:
        for t in dbpc.handler.queryAll(""" select gt.id, gt.aid, gt.sid, gt.flow, gt.args, gt.kwargs, gt.worknum, gt.queuetype, gt.worktype, gt.timeout, ga.name as a, ga.filepath, gu.name as u from grab_task gt join grab_article ga join grab_unit gu on gt.aid = ga.id and ga.uid = gu.id and gu.name = 'hotel' ; """):
            md = __import__('task.%s.%s' % (t['u'], t['filepath'].replace('.py', '')), fromlist=['task.%s' % t['u']])
            cls = getattr(md, 'Spider%s' % t['a'].capitalize())
            spider = cls(worknum=int(t['worknum']), queuetype=t['queuetype'], worktype=t['worktype'], tid=int(t['id']))
            spider.fetchDatas(t['flow'], t['args'])
            spider.statistic()
            for name in spider.stat.keys():
                if not name == 'total':
                    dbpc.handler.insert(""" insert into grab_log(`tid`,`sname`,`succ`,`fail`,`timeout`,`create_time`)
                                                    values( %s,     %s,    %s,    %s,       %s,        now())""", (t['id'], key, spider.stat[name]['succ'], spider.stat[name]['fail'], spider.stat[name]['timeout']))
        time.sleep(0.1)

if __name__ == '__main__':
    task()
