#!/usr/bin/python
# coding=utf-8

"""
   从 如家官网 渠道抓取酒店数据
"""

import datetime

from task.config.web.hotel import TIMEOUT
from webcrawl.handleRequest import requGet
from webcrawl.handleRequest import requPost
from webcrawl.handleRequest import getHtmlNodeContent
from webcrawl.handleRequest import getXmlNodeContent
from task.config.db.mysql import _DBCONN
from datakit.mongo.suit import withMongo
from webcrawl.work import retry
from webcrawl.work import index
from webcrawl.work import initflow
from webcrawl.handleRequest import getJsonNodeContent
from datakit.mysql.suit import withMysql
from webcrawl.work import store
from webcrawl.work import timelimit
from webcrawl.work import next
from task.config.db import mongo
from hotelspider import SpiderHotelOrigin
from hotelspider import Data

class SpiderHomeinns(SpiderHotelOrigin):
    """
       如家官网 数据爬虫
    """
    def __init__(self, worknum=30, queuetype='P', worktype='GEVENT', timeout=-1):
        self.clsname = self.__class__.__name__
        super(SpiderHomeinns, self).__init__(worknum=worknum, queuetype=queuetype, worktype=worktype, timeout=timeout)

    @timelimit(30)
    @store(update=True, method="MANY", way=Data.insert, db=withMysql(_DBCONN['use']['wdb']))
    def fetchMainWWWHotelone(self, url, hotel_id, additions={}, timeout=TIMEOUT, implementor=None):
        """
            根据url, hotel_id抓取一家官网酒店的信息
            @param url: 抓取地址
            @param hotel_id: 酒店ID
            @param additions: 附加内容
            @param timeout: 抓取超时
            @param implementor: 补充抓取器
            @return hotel_one: 一家酒店的信息
        """
        main_resp = requGet(url, timeout=timeout, format='HTML')
        hotel_id = hotel_id
        hotel_type = "001"
        hotel_name = getHtmlNodeContent(main_resp.find('.//div[@class="hotelname"]'), 'TEXT')
        address = getHtmlNodeContent(main_resp.find('.//div[@class="address"]//div[@class="bd"]'), 'TEXT')
        lat = getHtmlNodeContent(main_resp.find('.//input[@id="zuobiao_y"]'), {'ATTR':'value'})
        lnt = getHtmlNodeContent(main_resp.find('.//input[@id="zuobiao_x"]'), {'ATTR':'value'})
        logo = getHtmlNodeContent(main_resp.find('.//div[@class="m_img"]//img'), {'ATTR':'src'})
        status = 1
        tel = getHtmlNodeContent(main_resp.find('.//div[@class="tel"]'), 'TEXT').replace('电话：', '').strip('"').replace('gethotelfail', '')
        create_time = datetime.datetime.now()
        update_time = datetime.datetime.now()
        tid = 1
        yield Data(hotel_id=hotel_id, hotel_name=hotel_name, hotel_type=hotel_type, lat=lat, address=address, logo=logo, status=status, lnt=lnt, tel=tel, create_time=create_time, update_time=update_time, tid=tid)

    @index('url')
    @timelimit(6)
    @next(fetchMainWWWHotelone)
    def fetchMainWWWHotelids(self, url, city, additions={}, timeout=TIMEOUT, implementor=None):
        """
            抓取官网酒店列表
            @param url: 抓取地址
            @param city: 抓取城市
            @param additions: 附加内容
            @param timeout: 抓取超时
            @param implementor: 补充抓取器
            @return hotelid: 酒店ID
        """
        main_resp = requGet(url, timeout=timeout, format='HTML')
        allhotels = main_resp.findall('.//div[@class="list_tj"]')
        for hotel in allhotels:
            hotel_id = getHtmlNodeContent(hotel.find('.//div[@class="list_intro_img"]//a'), {'ATTR':'hotelcd'})
            yield {'url':'http://www.homeinns.com/hotel/%s' % hotel_id, 'hotel_id':hotel_id}

    @next(fetchMainWWWHotelids)
    @timelimit(20)
    @initflow('www')
    def fetchMainWWWCitys(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        """
            抓取官网城市列表
            @param url: 抓取地址
            @param additions: 附加内容
            @param timeout: 抓取超时
            @param implementor: 补充抓取器
            @return city: 城市
        """
        data = {}
        main_resp = requPost(url, data=data, timeout=timeout, format='HTML')
        provinces = main_resp.findall('.//ul[@id="a_f"][@class="zb_pop_se ABCDEF"]//li')
        for province in provinces[:1]:
            city = getHtmlNodeContent(province.find('.//a'), 'TEXT')
            yield {'url':'http://www.homeinns.com/%s/p1' % getHtmlNodeContent(province.find('.//span[@class="pop_pinyin"]'), 'TEXT'), 'city':city}

if __name__ == '__main__':

    print 'start'
    spider = SpiderHomeinns(worknum=6, queuetype='P', worktype='THREAD')
    spider.fetchDatas('www', 'http://www.homeinns.com/')
    spider.statistic()
    # spider.extractFlow()
    # spider.fire('http://www.homeinns.com/')
    print 'end'