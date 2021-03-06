#!/usr/bin/env python
# coding=utf-8

import os, sys, redis, time, datetime
import cPickle as pickle
from model.log import Log, Logsummary
from webcrawl.daemon import Daemon
from webcrawl.aboutfile import modulename, modulepath
from webcrawl.prettyprint import logprint
from webcrawl.queue.mongo import Queue
from model.setting import baseorm, withData, datacfg, LOGNUM, LOGSPAN, LOGRESERVE, LOGQUEUE, WORKQUEUE
from threading import Thread

_print, logger = logprint(modulename(__file__), modulepath(__file__))

path = os.path.abspath('.')
log_queue = redis.StrictRedis(host=LOGQUEUE['host'], port=LOGQUEUE['port'], db=LOGQUEUE['db'])
work_queue = Queue(host=WORKQUEUE['host'], port=WORKQUEUE['port'], db=WORKQUEUE['db'], tube=WORKQUEUE['tube'], init=False)
work_queue = work_queue.mc[work_queue.tube]

@withData(datacfg.W, autocommit=True)
def record(data):
    Log.insert(Log(**data))

@withData(datacfg.W, autocommit=True)
def statistic(start, end, reserve=None):
    result = {}
    for log in Log.queryAll({'$and':[{'create_time':{'$gte':start}}, {'create_time':{'$lt':end}}]}):
        if not log['tid'] in result:
            result[log['tid']] = {
                'total':0,
                'succ':0,
                'fail':0,
                'timeout':0,
                'elapse':0
            }
        result[log['tid']]['total'] += 1
        result[log['tid']][log['status'].lower()] += 1
        result[log['tid']]['elapse'] += log['elapse']
    for tid in result:
        Logsummary.insert(Logsummary(**{'tid':tid, 
            'succ':result[tid]['succ'],
            'fail':result[tid]['fail'],
            'timeout':result[tid]['timeout'],
            'elapse':round(result[tid]['elapse']/result[tid]['total'], 2),
            'create_time':start
        }))
    if reserve:
        for log in Log.queryAll({'create_time':{'$lt':reserve}}):
            Log.delete({'_id':log['_id']})
            work_queue.remove({'_id':log['_id']})


def produce(cls, **kwargs):
    data = {'_id':kwargs['ssid'],
        'tid':baseorm.IdField.verify(kwargs['tid']),
        'status':kwargs['status'],
        'elapse':kwargs['elapse'],
        'desc':kwargs['txt'],
        'create_time':kwargs['create_time'],
    }
    if kwargs['status'] in ('FAIL', 'TIMEOUT'):
        _print('_id-%s' % kwargs['ssid'])
        _print('tid: %s' % str(kwargs['tid']))
        _print('status: %s' % kwargs['status'])
        _print('elapse: %s' % str(kwargs['elapse']))
        _print('desc: %s' % kwargs['txt'])
        _print('create_time: %s' % str(kwargs['create_time']))
        _print('\n')
    log_queue.rpush(LOGQUEUE['tube'], pickle.dumps(data))


class Consumer(Thread):

    def run(self):
        while True:
            if log_queue.llen(LOGQUEUE['tube']) == 0:
                time.sleep(10)
            else:
                data = log_queue.lpop(LOGQUEUE['tube'])
                if data is None:
                    continue
                data = pickle.loads(data)
                record(data)


class Summary(Thread):

    def run(self):
        while True:
            end = datetime.datetime.now()
            start = end - datetime.timedelta(seconds=LOGSPAN)
            statistic(start.strftime('%Y-%m-%d %H:%M:%S'), \
                end.strftime('%Y-%m-%d %H:%M:%S'), \
                (end - datetime.timedelta(hours=LOGRESERVE)).strftime('%Y-%m-%d %H:%M:%S')
                )
            time.sleep(LOGSPAN)


class LogMonitor(Daemon):

    def _run(self):
        for k in range(LOGNUM):
            c = Consumer()
            c.setDaemon(False)
            c.start()
        s = Summary()
        s.start()


def main():

    lmoni = LogMonitor(os.path.join(path, 'log', 'lmoni.pid'), stdout=os.path.join(
        path, 'log', 'lmoni.out'), stderr=os.path.join(path, 'log', 'lmoni.err'))
    if os.path.exists(os.path.join(path, 'log', 'lmoni.pid')):
        print "LogMonitor stop successfully."
        lmoni.stop()
    else:
        print "LogMonitor start successfully."
        lmoni.start()


if __name__ == '__main__':
    main()
