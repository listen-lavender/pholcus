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

    @retry(1)
    @timelimit(30)
    @index("url")
    @initflow("WWW")
    def fetchWWWHotelone(self, implementor, url, hotel_id, additions={}, timeout=30):
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
        hotel_name = getJsonNodeContent(hotel.find(".//HotelName"), {"ATTR":"alt"})
        hotel_type = "002"
        lat = getJsonNodeContent(hotel.find(".//Lat"), "TEXT")
        address = ""
        logo = getJsonNodeContent(hotel.find(".//Telephone"), "TEXT")
        status = 1
        lnt = getJsonNodeContent(hotel.find(".//Lnt"), "TEXT")
        tel = getJsonNodeContent(hotel.find(".//Tel"), "TEXT")
        

    @initflow("WWW")
    @index("url")
    @next(fetchWWWHotelone)
    @retry(1)
    @timelimit(30)
    def fetchWWWHotelids(self, city, url, implementor, timeout=30, additions={}):
        data = {}
        data["CityID"] = city
        data["CheckOutDate"] = self.et
        data["CheckInDate"] = self.bt
        data["PageSize"] = 15
        data["PageIndex"] = 1
        allhotels = requPost(url=url, timeout=timeout, data=data, format=format)
