#!/usr/bin/python
# coding=utf-8

from webcrawl.spider import SpiderOrigin
# from task.model.mongo import initDB
# from task.model.mongo import Video as Data
# from task.config.db.mongo import RDB
# from task.config.db.mongo import WDB
# from task.config.db.mongo import _DBCONN as DBCONN
# from datakit.mongo.suit import withMongo as withDB

from task.model.mongo import initDB
from task.model.mongo import Video as Data
from task.config.db.mongo import RDB
from task.config.db.mongo import WDB
from task.config.db.mongo import _DBCONN as DBCONN
from datakit.mongo.suit import withMongo as withDB

TIMEOUT = 120

class SpiderVideoOrigin(SpiderOrigin):

    def __del__(self):
        pass

    def __init__(self, queuetype='P', timeout=-1, worknum=6, worktype='COROUTINE'):
        super(SpiderVideoOrigin, self).__init__(queuetype=queuetype, timeout=timeout, worknum=worknum, worktype=worktype)
        initDB()

if __name__ == "__main__":
    pass

