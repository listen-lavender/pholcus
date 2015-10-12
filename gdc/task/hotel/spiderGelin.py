#!/usr/bin/python
# coding=utf-8

from datetime import timedelta
from datetime import datetime
from task.config.web.hotel import TIMEOUT
from webcrawl.handleRequest import requGet
from webcrawl.handleRequest import requPost
from webcrawl.handleRequest import ensureurl
from webcrawl.handleRequest import parturl
from webcrawl.handleRequest import getHtmlNodeContent
from webcrawl.handleRequest import getXmlNodeContent
from task.config.db.mongo import _DBCONN as mongo
from task.config.db.mysql import _DBCONN as mysql
from datakit.mongo.suit import withMongo
from webcrawl.work import retry
from webcrawl.work import index
from webcrawl.work import initflow
from webcrawl.handleRequest import getJsonNodeContent
from datakit.mysql.suit import withMysql
from webcrawl.work import store
from webcrawl.work import timelimit
from webcrawl.work import next
from hotelspider import Data
from hotelspider import SpiderHotelOrigin

class Spider998(SpiderHotelOrigin):

    def __init__(self, queuetype="P", worktype="COROUTINE", worknum=6, timeout=-1, tid=0):
        super(Spider998, self).__init__(queuetype=queuetype, worktype=worktype, worknum=worknum, timeout=timeout)
        self.tid = tid
        self.clsname = self.__class__.__name__

if __name__ == "__main__":
    pass

