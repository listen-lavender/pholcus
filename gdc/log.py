#!/usr/bin/env python
# coding=utf-8

import os, sys
sys.path.append('../')

from webcrawl.daemon import Daemon
from kokolog import KokologHandler, logging
from kokolog.prettyprint import CFG
from model.log import RunLog
from Queue import Queue

path = os.path.abspath('.')

logqueue = Queue()

class Producer(KokologHandler):

    def __init__(self):
        self._name = ''
        Handler.__init__(self)

    def emit(self, record):
        logqueue.put(record.kwargs)


hdr = Producer()
frt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
hdr.setFormatter(frt)
CFG.handlers.append(hdr)


class Consumer(Daemon):

    def _run(self):
        while True:
            if logqueue.empty():
                time.sleep(SLEEP)
            else:
                data = logqueue.get()
                RunLog.insert(RunLog(**data))

def main():
    log = Consumer(os.path.join(path, 'log', 'log.pid'), stdout=os.path.join(
        path, 'log', 'log.out'), stderr=os.path.join(path, 'log', 'log.err'))
    if os.path.exists(os.path.join(path, 'log', 'log.pid')):
        print "Consumer stop successfully."
        log.stop()
    else:
        print "Consumer start successfully."
        log.start()

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
