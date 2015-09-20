#!/usr/bin/python
# coding=utf-8

from task.config.web.hotel import TIMEOUT
from webcrawl.handleRequest import requGet
from webcrawl.handleRequest import requPost
from webcrawl.handleRequest import getHtmlNodeContent
from webcrawl.handleRequest import getXmlNodeContent
from task.config.db import mysql
from webcrawl.work import withMongo
from webcrawl.work import retry
from webcrawl.work import index
from webcrawl.work import initflow
from webcrawl.handleRequest import getJsonNodeContent
from webcrawl.work import withMysql
from webcrawl.work import store
from webcrawl.work import timelimit
from webcrawl.work import next
from task.config.db import mongo
from hotelspider import SpiderHotelOrigin
from task.model.mysql import initDb
from task.model.mysql import Hotel

class SpiderHomeinns(SpiderHotelOrigin):

    def __init__(self, queuetype="P", worktype="COROUTINE", timeout=-1, worknum=6):
        super(SpiderHomeinns, self).__init__(queuetype=queuetype, worktype=worktype, timeout=timeout, worknum=worknum)
        self.bt = datetime.datetime.now().strftime('%Y-%m-%d')
        self.et = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    @timelimit(30)
    @store(update=True, method="MANY", way=Hotel.insert, db=withMysql(mysql['use']['wdb']))
    def fetchWWWHotelone(self, url, hotel_id, additions={}, timeout=30, implementor=None):
        cookies = {}
        cookies["Origin"] = "http://i.huazhu.com"
        cookies["Referer"] = "http://i.huazhu.com/hotel/detail/%s" % hotel_id
        data = {}
        data["hotelID"] = hotel_id
        data["CheckInDate"] = self.bt
        data["CheckOutDate"] = self.et
        data["QueryRoomType"] = ""
        data["activityID"] = ""
        hotel = requPost(url=url, timeout=timeout, cookies=cookies, data=data, format=format)
        hotel_id = hotel_id
        hotel_name = getJsonNodeContent(hotel.find(".//HotelName"), {"ATTR":"alt"})
        hotel_type = "002"
        lat = getJsonNodeContent(hotel.find(".//Lat"), "TEXT")
        address = ""
        logo = getJsonNodeContent(hotel.find(".//Telephone"), "TEXT")
        status = 1
        lnt = getJsonNodeContent(hotel.find(".//Lnt"), "TEXT")
        tel = getJsonNodeContent(hotel.find(".//Tel"), "TEXT")
        yield Hotel(hotel_id=hotel_id, hotel_name=hotel_name, hotel_type=hotel_type, lat=lat, address=address, logo=logo, status=status, lnt=lnt, tel=tel)

    @index("url")
    @next(fetchWWWHotelone)
    @timelimit(30)
    def fetchWWWHotelids(self, city, url, implementor=None, timeout=30, additions={}):
        yield next_page
        data = {}
        data["CityID"] = city
        data["CheckOutDate"] = self.et
        data["CheckInDate"] = self.bt
        data["PageSize"] = 15
        data["PageIndex"] = 1
        result = requPost(url=url, timeout=timeout, data=data, format=format)
        hotels = result.findall(".//Data//HotelList")
        for one in hotels:
            hotel = {}
            hotel["hotel_id"] = getJsonNodeContent(result.find(".//Info//ID"), "TEXT")
            hotel["url"] = "http://i.huazhu.com/api/hotel/detail"
            yield hotel

    @next(fetchWWWHotelids)
    @initflow("WWW")
    @timelimit(30)
    def fetchWWWCitys(self, url, implementor=None, additions={}, timeout=30):
        data = {}
        result = requPost(url=url, timeout=timeout, data=data, format=format)
        citys = result.findall(".//Data//CityList")
        for one in citys:
            city = {}
            city["url"] = "http://i.huazhu.com/api/hotel/list###0"
            city["city"] = getJsonNodeContent(result.find(".//CityName"), "TEXT")
            city["additions"] = {}
            city["additions"]["NUM"] = 30
            city["additions"]["cid"] = getJsonNodeContent(result.find(".//CityID"), "TEXT")
            yield city
