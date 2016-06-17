#!/usr/bin/env python
# coding=utf-8

import os, sys, redis, time, datetime
import cPickle as pickle
from model.log import Log, Logsummary
from webcrawl.daemon import Daemon
from webcrawl import Logger
from model.setting import baseorm
from model.setting import withData, datacfg, LOGNUM, LOGSPAN, LOGQUEUE
from threading import Thread

path = os.path.abspath('.')
log_queue = redis.StrictRedis(host=LOGQUEUE['host'], port=LOGQUEUE['port'], db=LOGQUEUE['db'])

@withData(datacfg.W, autocommit=True)
def record(data):
    Log.insert(Log(**data))

@withData(datacfg.W, autocommit=True)
def statistic(start, end):
    result = {}
    for log in Log.queryAll({'create_time':{'$gte':start}, 'create_time':{'$lt':end}}):
        if not log['_id'] in result:
            result[log['_id']] = {
                'total':0,
                'succ':0,
                'fail':0,
                'timeout':0,
                'elapse':0
            }
        result[log['_id']]['total'] += 1
        result[log['_id']][log['status'].lower()] += 1
        result[log['_id']]['elapse'] += log['elapse']
    for tid in result:
        Logsummary.insert(Logsummary(**{'tid':tid, 
            'succ':result[tid]['succ'],
            'fail':result[tid]['fail'],
            'timeout':result[tid]['timeout'],
            'elapse':(result[tid]['elapse']/float(result[tid]['total']), 2)
            'create_time':start
        }))


def produce(cls, **kwargs):
    data = {'_id':kwargs['ssid'],
        'tid':baseorm.IdField.verify(kwargs['tid']),
        'status':kwargs['status'],
        'elapse':kwargs['elapse'],
        'desc':kwargs['txt'],
        'create_time':kwargs['create_time'],
    }
    log_queue.rpush(LOGQUEUE['tube'], pickle.dumps(data))

Logger._print = MethodType(produce, Logger, Logger)


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
            statistic(start, end)
            time.sleep(LOGSPAN)


class LogMonitor(Daemon):

    def _run(self):
        for k in range(LOGNUM):
            c = Consumer(**LOGQUEUE)
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
