#!/usr/bin/python
# coding=utf-8

from datetime import timedelta
from datetime import datetime
from task.config.web.hotel import TIMEOUT
from webcrawl.handleRequest import requGet
from webcrawl.handleRequest import requPost
from webcrawl.handleRequest import getHtmlNodeContent
from webcrawl.handleRequest import getXmlNodeContent
from task.config.db.mysql import _DBCONN as mysql
from datakit.mongo.suit import withMongo
from webcrawl.work import retry
from webcrawl.work import index
from webcrawl.work import initflow
from webcrawl.handleRequest import getJsonNodeContent
from webcrawl.work import store
from webcrawl.work import timelimit
from webcrawl.work import next
from webcrawl.handleRequest import ensureurl
from webcrawl.handleRequest import parturl
from task.config.db.mongo import _DBCONN as mongo
from datakit.mysql.suit import withMysql
from hotelspider import Data
from hotelspider import SpiderHotelOrigin

class SpiderHomeinns(SpiderHotelOrigin):

    def __init__(self, queuetype="P", worktype="COROUTINE", timeout=-1, worknum=6, tid=0):
        super(SpiderHomeinns, self).__init__(queuetype=queuetype, worktype=worktype, timeout=timeout, worknum=worknum)
        self.tid = tid
        self.clsname = self.__class__.__name__

    @timelimit(30)
    @store(update=True, method="MANY", way=Data.insert, db=withMysql(mysql['use']['wdb']))
    def fetchWWWHotelone(self, url):
        rqp = parturl(url=url)
        hotel = requGet(url=url, format="HTML", timeout=TIMEOUT)
        hotel_id = rqp[0][-1]
        hotel_name = getHtmlNodeContent(hotel.find(".//div[@class='hotelname']"), "TEXT")
        hotel_type = "001"
        lat = getHtmlNodeContent(hotel.find(".//input[@id='zuobiao_y']"), {'ATTR':'value'})
        address = getHtmlNodeContent(hotel.find(".//a[@pop='addressTip']"), "TEXT")
        create_time = datetime.now()
        tid = self.tid
        update_time = datetime.now()
        logo = getHtmlNodeContent(hotel.find(".//div[@class='pic1 ']//div"), {'ATTR':'_src'})
        status = 1
        lnt = getHtmlNodeContent(hotel.find(".//input[@id='zuobiao_x']"), {'ATTR':'value'})
        tel = getHtmlNodeContent(hotel.find(".//div[@class='tel']"), "TEXT")
        yield Data(hotel_id=hotel_id, hotel_name=hotel_name, hotel_type=hotel_type, lat=lat, address=address, create_time=create_time, tid=tid, update_time=update_time, logo=logo, status=status, lnt=lnt, tel=tel)

    @next(fetchWWWHotelone)
    @timelimit(30)
    def fetchWWWHotelids(self, url):
        result = requGet(url=url, format="HTML", timeout=TIMEOUT)
        hotels = result.findall(".//div[@class='list_intro_name_tj']//a")
        for one in hotels:
            hotel = getHtmlNodeContent(one, {'ATTR':'href'})
            hotel = ensureurl(objurl=hotel, refurl=url)
            yield hotel

    @next(fetchWWWHotelids)
    @initflow("www")
    @timelimit(30)
    def fetchWWWCitys(self, url):
        result = requGet(url=url, timeout=TIMEOUT, format="HTML")
        citys = result.findall(".//ul[@class='ml_order_link']//a")
        for one in citys:
            city = getHtmlNodeContent(one, {'ATTR':'href'})
            city = ensureurl(refurl=url, objurl=city)
            yield city

if __name__ == "__main__":
    pass

