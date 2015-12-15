#!/usr/bin/python
# coding=utf-8

from webcrawl.spider import SpiderOrigin

from task.model.mysql import initDB
from task.model.mysql import Hotel as Data
from task.config.db.mysql import RDB
from task.config.db.mysql import WDB
from task.config.db.mysql import _DBCONN as DBCONN
from datakit.mysql.suit import withMysql as withDB

# from task.model.mongo import initDB
# from task.model.mongo import Hotel as Data
# from task.config.db.mongo import RDB
# from task.config.db.mongo import WDB
# from task.config.db.mongo import _DBCONN as DBCONN
# from datakit.mongo.suit import withMongo as withDB

class SpiderHotelOrigin(SpiderOrigin):

    def __del__(self):
        pass

    def __init__(self, queuetype="P", worknum=6, timeout=-1, worktype="COROUTINE"):
        super(SpiderHotelOrigin, self).__init__(queuetype=queuetype, worknum=worknum, timeout=timeout, worktype=worktype)
        initDB()

if __name__ == "__main__":
    pass

