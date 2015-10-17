# from task.hotel.spiderWeiye import SpiderWyn88
#!/usr/bin/python
# coding=utf-8
import time
from datakit.mysql.suit import withMysql, dbpc
from task.config.db.mysql import RDB, WDB
from task.model.mysql import initDB
# from task.hotel.spiderRujia import SpiderHomeinns
import task

# initDB()
    
# @withMysql(WDB, resutype='DICT')
# def taskget():
#     md = dbpc.handler.queryOne(""" select gt.id, gt.aid, gt.sid, gt.flow, gt.args, gt.kwargs, gt.worknum, gt.queuetype, gt.worktype, gt.timeout, ga.name as a, ga.filepath, gu.name as u from grab_task gt join grab_article ga join grab_unit gu on gt.aid = ga.id and ga.uid = gu.id where ga.name = 'homeinns'; """)
#     return md

from task.hotel.spiderRujia import SpiderHomeinns

if __name__ == '__main__':
    # t = taskget()
    # print 'task.%s.%s' % (t['u'], t['filepath'].replace('.py', ''))
    # md = __import__('task.%s.%s' % (t['u'], t['filepath'].replace('.py', '')), fromlist=['task.%s' % t['u']])
    # cls = getattr(md, 'Spider%s' % t['a'].capitalize())
    # spider = cls(worknum=int(t['worknum']), queuetype=t['queuetype'], worktype=t['worktype'], tid=int(t['id']))
    # spider.fetchDatas(t['flow'], t['args'])
    # spider.statistic()
    spider = SpiderHomeinns(worknum=6, queuetype='P', worktype='THREAD')
    spider.fetchDatas('www', 'http://www.homeinns.com/hotel')
    spider.statistic()
