#!/usr/bin/env python
# coding=utf-8

import os, sys
import cPickle as pickle
sys.path.append('../')

from webcrawl.daemon import Daemon
from kokolog import KokologHandler, logging
from kokolog.prettyprint import CFG
from model.log import RunLog
from webcrawl.daemon import Daemon
from setting import DQ

path = os.path.abspath('.')


class Producer(KokologHandler):

    def __init__(self, queue_config=DQ['redis']['log']):
        self._name = 'koko'
        self.q = redis.StrictRedis(**{'host':queue_config['host'], 'port':queue_config['port'], 'db':queue_config['db']})
        self.tube = queue_config['tube']
        Handler.__init__(self)

    def emit(self, record):
        data = {'tid':record.kwargs['tid'], 
            'sid':record.kwargs['sid'],
            'sname':record.kwargs['sname'],
            'priority':record.kwargs['priority'],
            'times':record.kwargs['times'],
            'args':record.kwargs['args'],
            'kwargs':record.kwargs['kwargs'],
            'txt':record.kwargs['txt'],
        }        
        self.q.put(pickle.dumps(data))


hdr = Producer()
frt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
hdr.setFormatter(frt)
CFG.handlers.append(hdr)


class Consumer(Thread):
    def __init__(self, q):
        super(Consumer, self).__init__()
        self.q = q

    def _run(self):
        while True:
            if self.q.empty():
                time.sleep(SLEEP)
            else:
                data = self.q.get()
                data['atime'] = datetime.datetime.now()
                RunLog.insert(RunLog(**data))


from webcrawl.daemon import Daemon
from grab import task

path = os.path.abspath('.')

class PeriodMonitor(Daemon):

    def _run(self):
        task()

def main():
    moni = PeriodMonitor(os.path.join(path, 'log', 'moni.pid'), stdout=os.path.join(
        path, 'log', 'moni.out'), stderr=os.path.join(path, 'log', 'moni.err'))
    if os.path.exists(os.path.join(path, 'log', 'moni.pid')):
        print "PeriodMonitor stop successfully."
        moni.stop()
    else:
        print "PeriodMonitor start successfully."
        moni.start()

if __name__ == '__main__':
    main()

    # print '====start moefou'
    # spider = SpiderMoefou(worknum=6, queuetype='P', worktype='THREAD')
    # spider.fetchDatas('www', **{'url':'http://api.moefou.org/wikis.json?wiki_type=music&initial=&tag=&wiki_id=&api_key={{api_key}}&page=1'})
    # spider.statistic()
    # print '====end moefou'

    # print '====start bili'
    # from task.video.spiderBili import SpiderBilibili
    # spider = SpiderBilibili(worknum=6, queuetype='P', worktype='THREAD')
    # spider.fetchDatas('www', 'http://www.bilibili.com/html/js/types.json')
    # spider.statistic()
    # print '====end bili'

    # print 'start'
    # spider = SpiderXicidaili(worknum=6, queuetype='P', worktype='THREAD')
    # spider.fetchDatas('www', **{'url':'http://www.xicidaili.com/nn/1'})
    # spider.statistic()
    # print 'end'
