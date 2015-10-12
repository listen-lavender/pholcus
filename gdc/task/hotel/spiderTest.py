#!/usr/bin/python
# coding=utf-8

from datetime import timedelta
from datetime import datetime
from task.config.web.hotel import TIMEOUT
from webcrawl.handleRequest import requGet
from webcrawl.handleRequest import requPost
from webcrawl.handleRequest import getHtmlNodeContent
from webcrawl.handleRequest import getXmlNodeContent
from webcrawl.handleRequest import getJsonNodeContent
from webcrawl.handleRequest import parturl
from task.config.db.mysql import _DBCONN as mysql
from datakit.mongo.suit import withMongo
from webcrawl.work import retry
from webcrawl.work import index
from webcrawl.work import initflow
from datakit.mysql.suit import withMysql
from webcrawl.work import store
from webcrawl.work import timelimit
from webcrawl.work import next
from task.config.db.mongo import _DBCONN as mongo
from hotelspider import SpiderHotelOrigin
from hotelspider import Data


class SpiderHomeinns(SpiderHotelOrigin):

    def __init__(self, tid=0, queuetype="P", worktype="COROUTINE", timeout=-1, worknum=6):
        super(SpiderHomeinns, self).__init__(queuetype=queuetype, worktype=worktype, timeout=timeout, worknum=worknum)
        self.tid = tid
        self.clsname = self.__class__.__name__
        self.bt = datetime.now().strftime('%Y-%m-%d')
        self.et = (datetime.now()+timedelta(days=1)).strftime('%Y-%m-%d')

    @timelimit(30)
    @store(update=True, method="MANY", way=Data.insert, db=withMysql(mysql['use']['wdb']))
    def fetchWWWHotelone(self, url):
        rp, pq = parturl(url)
        hotel = requGet(url=url, timeout=timeout, format="HTML")
        hotel_id = rp[-1]
        hotel_name = getHtmlNodeContent(hotel.find(".//div[@class='hotelname']"), {"ATTR":"alt"})
        hotel_type = "001"
        lat = getHtmlNodeContent(hotel.find(".//input[@id='zuobiao_y']"), "TEXT")
        address = ""
        create_time = datetime.now()
        tid = self.tid
        update_time = datetime.now()
        logo = getHtmlNodeContent(hotel.find(".//div[@class='m_img']//img"), "TEXT")
        status = 1
        lnt = getHtmlNodeContent(hotel.find(".//input[@id='zuobiao_x']"), "TEXT")
        tel = getHtmlNodeContent(hotel.find(".//div[@class='tel']"), "TEXT")
        yield Data(hotel_id=hotel_id, hotel_name=hotel_name, hotel_type=hotel_type, lat=lat, address=address, create_time=create_time, tid=tid, update_time=update_time, logo=logo, status=status, lnt=lnt, tel=tel)

    @next(fetchWWWHotelone)
    @timelimit(30)
    def fetchWWWHotelids(self, url):
        result = requGet(url=url, timeout=timeout, format="HTML")
        hotels = result.findall(".//div[@class='list_tj']")
        for one in hotels:
            hotel = {}
            hotel["url"] = "http://www.homeinns.com/hotel/%s" % getHtmlNodeContent(one.find(".//div[@class='list_intro_img']//a"), {'ATTR':'hotelcd'})
            yield hotel

    @next(fetchWWWHotelids)
    @initflow("www")
    @timelimit(30)
    def fetchWWWCitys(self, url):
        data = {}
        result = requPost(url=url, timeout=timeout, data={}, format="HTML")
        citys = result.findall(".//ul[@id='a_f'][@class='zb_pop_se ABCDEF']//li")
        for one in citys:
            city = {}
            city['url'] = "http://www.homeinns.com/%s/p1" % getHtmlNodeContent(one.find(".//span[@class='pop_pinyin']"), "TEXT")
            yield city

if __name__ == "__main__":
    pass

