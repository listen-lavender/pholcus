#!/usr/bin/env python
# coding=utf-8

from webcrawl.spider import SpiderOrigin
# from task.model.mysql import initDB
# from task.model.mysql import Audio as Data
# from task.config.db.mysql import RDB
# from task.config.db.mysql import WDB
# from task.config.db.mysql import _DBCONN as DBCONN
# from dbskit.mysql.suit import withMysql as withData

from task.model.mongo import initDB
from task.model.mongo import Audio as Data
from task.config.db.mongo import RDB
from task.config.db.mongo import WDB
from task.config.db.mongo import _DBCONN as DBCONN
from model.setting import withData

TIMEOUT = 120

class SpiderAudioOrigin(SpiderOrigin):

    def __del__(self):
        pass

    def __init__(self, queuetype='P', timeout=-1, worknum=6, worktype='COROUTINE'):
        super(SpiderAudioOrigin, self).__init__(queuetype=queuetype, timeout=timeout, worknum=worknum, worktype=worktype)
        initDB()

if __name__ == "__main__":
    pass

