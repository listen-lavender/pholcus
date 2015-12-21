#!/usr/bin/python
# coding=utf-8
import logging
import os
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
