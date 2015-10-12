#!/usr/bin/python
# coding=utf-8

from webcrawl.spider import SpiderOrigin
from task.config.db.mysql import RDB
from task.config.db.mysql import WDB
from task.model.mysql import initDB
from task.model.mysql import Lion as Data
from datakit.mysql.suit import withMysql as withDB

class SpiderLionOrigin(SpiderOrigin):

    def __del__(self):
        pass

    def __init__(self, queuetype="P", worknum=6, timeout=-1, worktype="COROUTINE"):
        super(SpiderLionOrigin, self).__init__(queuetype=queuetype, worknum=worknum, timeout=timeout, worktype=worktype)
        initDB()

if __name__ == "__main__":
    pass

