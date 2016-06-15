#!/usr/bin/env python
# coding=utf-8

import os, sys, redis, time, datetime
import cPickle as pickle

from kokolog import KokologHandler, logging
from kokolog.prettyprint import CFG
from model.log import Log, Logsummary
from webcrawl.daemon import Daemon
from model.setting import baseorm
from model.setting import withData, datacfg, LOGNUM, LOGSTATUS, LOGQUEUE
from threading import Thread

path = os.path.abspath('.')


class Producer(KokologHandler):

    def __init__(self, **config):
        super(Producer, self).__init__()
        self._name = 'koko'
        self.tube = config['tube']
        self.q = redis.StrictRedis(host=config['host'], port=config['port'], db=config['db'])

    def emit(self, record):
        data = {'_id':record.kwargs['ssid'],
            'tid':baseorm.IdField.verify(record.kwargs['tid']),
            'status':record.kwargs['status'],
            'elapse':record.kwargs['elapse'],
            'desc':record.kwargs['txt'],
            'create_time':record.kwargs['create_time'],
        }
        self.q.rpush(self.tube, pickle.dumps(data))


hdr = Producer(**LOGQUEUE)
frt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
hdr.setFormatter(frt)
CFG.handlers.append(hdr)


@withData(datacfg.W, autocommit=True)
def record(data):
    Log.insert(Log(**data))


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
                if data is None:
                    continue
                data = pickle.loads(data)
                data['atime'] = datetime.datetime.now()
                record(data)


class Summary(Thread):
    def __init__(self):
        pass

    def run(self):
        while True:
            time.sleep(1)


class LogMonitor(Daemon):

    def _run(self):
        for k in range(LOGNUM):
            c = Consumer(**LOGQUEUE)
            c.setDaemon(False)
            c.start()
        # s = Summary()
        # s.start()


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
