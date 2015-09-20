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
from datakit.mysql.suit import withMysql
from webcrawl.work import store
from webcrawl.work import timelimit
from webcrawl.work import next
from task.config.db.mongo import _DBCONN as mongo
from hotelspider import SpiderHotelOrigin
from hotelspider import Data

class SpiderHomeinns(SpiderHotelOrigin):

    def __init__(self, queuetype="P", worktype="COROUTINE", timeout=-1, worknum=6):
        super(SpiderHomeinns, self).__init__(queuetype=queuetype, worktype=worktype, timeout=timeout, worknum=worknum)
        self.clsname = self.__class__.__name__
        self.bt = datetime.now().strftime('%Y-%m-%d')
        self.et = (datetime.now()+timedelta(days=1)).strftime('%Y-%m-%d')

    @timelimit(30)
    @store(update=True, method="MANY", way=Data.insert, db=withMysql(mysql['use']['wdb']))
    def fetchWWWHotelone(self, url, hotel_id, additions={}, timeout=30, implementor=None):
        hotel = requGet(url=url, timeout=timeout, format="HTML")
        cookies = {}
        cookies["Origin"] = "http://i.huazhu.com"
        cookies["Referer"] = "http://i.huazhu.com/hotel/detail/%s" % hotel_id
        data = {}
        data["hotelID"] = hotel_id
        data["CheckInDate"] = self.bt
        data["CheckOutDate"] = self.et
        data["QueryRoomType"] = ""
        data["activityID"] = ""
        hotel_id = hotel_id
        hotel_name = getHtmlNodeContent(hotel.find(".//div[@class='hotelname']"), {"ATTR":"alt"})
        hotel_type = "001"
        lat = getHtmlNodeContent(hotel.find(".//input[@id='zuobiao_y']"), "TEXT")
        address = ""
        create_time = datetime.now()
        tid = 1
        update_time = datetime.now()
        logo = getHtmlNodeContent(hotel.find(".//div[@class='m_img']//img"), "TEXT")
        status = 1
        lnt = getHtmlNodeContent(hotel.find(".//input[@id='zuobiao_x']"), "TEXT")
        tel = getHtmlNodeContent(hotel.find(".//div[@class='tel']"), "TEXT")
        yield Data(hotel_id=hotel_id, hotel_name=hotel_name, hotel_type=hotel_type, lat=lat, address=address, create_time=create_time, tid=tid, update_time=update_time, logo=logo, status=status, lnt=lnt, tel=tel)

    @next(fetchWWWHotelone)
    @timelimit(30)
    def fetchWWWHotelids(self, city, url, implementor=None, timeout=30, additions={}):
        result = requGet(url=url, timeout=timeout, format="HTML")
        data = {}
        data["CityID"] = city
        data["CheckOutDate"] = self.et
        data["CheckInDate"] = self.bt
        data["PageSize"] = 15
        data["PageIndex"] = 1
        hotels = result.findall(".//div[@class='list_tj']")
        for one in hotels:
            hotel = {}
            hotel["hotel_id"] = getHtmlNodeContent(one.find(".//div[@class='list_intro_img']//a"), {'ATTR':'hotelcd'})
            hotel["url"] = "http://www.homeinns.com/hotel/%s" % hotel["hotel_id"]
            yield hotel

    @next(fetchWWWHotelids)
    @initflow("www")
    @timelimit(30)
    def fetchWWWCitys(self, url, implementor=None, additions={}, timeout=30):
        result = requPost(url=url, timeout=timeout, data={}, format="HTML")
        citys = result.findall(".//ul[@id='a_f'][@class='zb_pop_se ABCDEF']//li")
        for one in citys[:1]:
            cpp = getHtmlNodeContent(one.find(".//span[@class='pop_pinyin']"), "TEXT")
            city = {}
            city["url"] = "http://www.homeinns.com/%s/p1" % cpp
            city["city"] = getHtmlNodeContent(one.find(".//CityName"), "TEXT")
            city["additions"] = {}
            city["additions"]["NUM"] = 30
            city["additions"]["cid"] = getHtmlNodeContent(one.find(".//CityName"), "TEXT")
            yield city

if __name__ == "__main__":
    pass

