#!/usr/bin/python
# coding=utf-8

"""
   从 如家官网 渠道抓取酒店数据
"""
import time
# import datakit.mysql.suit as mydb
# import gevent
# from gevent.queue import Queue
import datakit.mysql.suit as suit
from webcrawl.work import Workflows
from webcrawl.work import initflow, index, retry, next, timelimit
from task.config.db.mysql import RDB, WDB, LIMIT, _DBCONN, USE
from datakit.mysql.suit import dbpc, withMysql, DBPoolCollector
from datakit.mysql.handler import DBHandler
from task.keep import Keeper
# import threading
# print Queue
# mydb.Queue = gevent.queue

class SpiderText(Workflows):
    def __init__(self, worknum=30, queuetype='P', worktype='COROUTINE', timeout=-1):
        Workflows.__init__(self, worknum=worknum, queuetype=queuetype, worktype=worktype)
        print '>>>>>>a'
        # Keeper.__init__(self)
        print '>>>>>>b'
        self.timeout = timeout
        self.dones = set()
        suit.dbpc = DBPoolCollector(DBHandler, delegate=True)
        suit.dbpc.addDB(RDB, LIMIT, host=_DBCONN[USE]['host'],
                    port=_DBCONN[USE]['port'],
                    user=_DBCONN[USE]['user'],
                    passwd=_DBCONN[USE]['passwd'],
                    db=_DBCONN[USE]['db'],
                    charset=_DBCONN[USE]['charset'],
                    use_unicode=_DBCONN[USE]['use_unicode'],
                    override=False)
        suit.dbpc.addDB(WDB, LIMIT, host=_DBCONN[USE]['host'],
                            port=_DBCONN[USE]['port'],
                            user=_DBCONN[USE]['user'],
                            passwd=_DBCONN[USE]['passwd'],
                            db=_DBCONN[USE]['db'],
                            charset=_DBCONN[USE]['charset'],
                            use_unicode=_DBCONN[USE]['use_unicode'],
                            override=False)

    def step3(self, url):
        # print gevent.getcurrent()
        # print threading.currentThread()
        for k in range(3):
            time.sleep(0.5)
            print 'result', url*10 + k
            # print gevent.getcurrent()
            # print threading.currentThread()

    # @next(step3)
    @withMysql(WDB)
    def step2(self, url):
        # print gevent.getcurrent()
        # print threading.currentThread()
        for k in range(3):
            time.sleep(0.5)
            yield {'url':url*10 + k}
            # print gevent.getcurrent()
            # print threading.currentThread()

    @next(step2)
    @initflow('www')
    def step1(self):
        # print gevent.getcurrent()
        # print threading.currentThread()
        for k in range(3):
            time.sleep(0.5)
            yield {'url':k}
            # print gevent.getcurrent()
            # print threading.currentThread()

    def do(self, flow, *args, **kwargs):
        try:
            self.extractFlow()
            start = time.time()
            self.fire(flow, *args, **kwargs)
            if self.timeout > -1:
                def check(self, timeout):
                    time.sleep(timeout)
                    self.exit()
                    print 'Time out of %s. ' % str(self.timeout)
                import threading
                wather = threading.Thread(target=check, args=(self, self.timeout - (time.time() - start)))
                wather.setDaemon(True)
                wather.start()
            self.waitComplete()
            self.dones.add(flow)
            end = time.time()
            self.totaltime = end - start
            return True
        except:
            return False

    def statistic(self):
        for flow in self.dones:
            it = self.tinder(flow)
            print '==============Statistics of flow %s==============' % flow
            stat = {'total':{'succ':0, 'fail':0, 'timeout':0}} 
            total = {'succ':0, 'fail':0, 'timeout':0}
            stat[it.__name__] = {}
            stat[it.__name__]['succ'] = it.succ
            stat[it.__name__]['fail'] = it.fail
            stat[it.__name__]['timeout'] = it.timeout
            stat['total']['succ'] = stat['total']['succ'] + it.succ
            stat['total']['fail'] = stat['total']['fail'] + it.fail
            stat['total']['timeout'] = stat['total']['timeout'] + it.timeout
            print it.__name__, 'succ: ', it.succ
            print it.__name__, 'fail: ', it.fail
            print it.__name__, 'timeout: ', it.timeout
            while hasattr(it, 'next'):
                stat[it.next.__name__] = {}
                stat[it.next.__name__]['succ'] = it.next.succ
                stat[it.next.__name__]['fail'] = it.next.fail
                stat[it.next.__name__]['timeout'] = it.next.timeout
                stat['total']['succ'] = stat['total']['succ'] + it.next.succ
                stat['total']['fail'] = stat['total']['fail'] + it.next.fail
                stat['total']['timeout'] = stat['total']['timeout'] + it.next.timeout
                print it.next.__name__, 'succ: ', it.next.succ
                print it.next.__name__, 'fail: ', it.next.fail
                print it.next.__name__, 'timeout: ', it.next.timeout
                it = it.next
            print 'total succ: ', stat['total']['succ']
            print 'total fail: ', stat['total']['fail']
            print 'total timeout: ', stat['total']['timeout']
            print 'total time: ', self.totaltime

if __name__ == '__main__':

    print 'start'
    spider = SpiderText(worknum=6, queuetype='P', worktype='THREAD')
    print dir(spider)
    spider.do('www')
    spider.statistic()
    print 'end'
