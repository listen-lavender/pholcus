#!/usr/bin/python
# coding=utf-8

from webcrawl.spider import SpiderOrigin
from task.model.mysql import initDB
from task.model.mysql import Proxy as Data
from task.config.db.mysql import RDB
from task.config.db.mysql import WDB
from task.config.db.mysql import _DBCONN as DBCONN
from datakit.mysql.suit import withMysql as withDB

TIMEOUT = 10

class SpiderProxyOrigin(SpiderOrigin):

    def __del__(self):
        pass

    def __init__(self, queuetype='P', timeout=-1, worknum=6, worktype='COROUTINE'):
        super(SpiderProxyOrigin, self).__init__(queuetype=queuetype, timeout=timeout, worknum=worknum, worktype=worktype)
        initDB()

if __name__ == "__main__":
    pass

