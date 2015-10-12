#!/usr/bin/python
# coding=utf-8

from webcrawl.spider import SpiderOrigin
from task.config.db.mysql import RDB
from task.model.mysql import initDB
from task.config.db.mysql import WDB
from datakit.mysql.suit import withMysql as withDB
from task.model.mysql import Tiger as Data

class SpiderTigerOrigin(SpiderOrigin):

    def __del__(self):
        pass

    def __init__(self, queuetype="P", worknum=6, timeout=-1, worktype="COROUTINE"):
        super(SpiderTigerOrigin, self).__init__(queuetype=queuetype, worknum=worknum, timeout=timeout, worktype=worktype)
        initDB()

if __name__ == "__main__":
    pass

