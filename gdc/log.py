#!/usr/bin/env python
# coding=utf-8

import os, sys, redis, time, datetime
import cPickle as pickle
sys.path.append('../')

from webcrawl.daemon import Daemon
from kokolog import KokologHandler, logging
from kokolog.prettyprint import CFG
from model.log import RunLog
from webcrawl.daemon import Daemon
from model.setting import withBase, withData, RDB, WDB
from threading import Thread
from setting import DQ, LOGWORKERNUM

path = os.path.abspath('.')


class Producer(KokologHandler):

    def __init__(self, **config):
        super(Producer, self).__init__()
        self._name = 'koko'
        self.tube = config['tube']
        self.q = redis.StrictRedis(host=config['host'], port=config['port'], db=config['db'])


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
        self.q.rpush(self.tube, pickle.dumps(data))


hdr = Producer(**DQ['redis']['log'])
frt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
hdr.setFormatter(frt)
CFG.handlers.append(hdr)


@withData(WDB, autocommit=True)
def record(data):
    RunLog.insert(RunLog(**data))


class Consumer(Thread):
    def __init__(self, **config):
        super(Consumer, self).__init__()
        self.tube = config['tube']
        self.q = redis.StrictRedis(host=config['host'], port=config['port'], db=config['db'])

    def run(self):
        while True:
            if self.q.llen(self.tube) == 0:
                time.sleep(10)
            else:
                data = self.q.lpop(self.tube)
                data = pickle.loads(data)
                data['atime'] = datetime.datetime.now()
                record(data)


class LogMonitor(Daemon):

    def _run(self):
        for k in range(LOGWORKERNUM):
            c = Consumer(**DQ['redis']['log'])
            c.setDaemon(False)
            c.start()


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
