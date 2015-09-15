#!/usr/bin/python
# coding=utf-8

"""
   从 如家官网 渠道抓取酒店数据
"""

import datetime

from task.config.web.hotel import TIMEOUT, SERVICES, INSERTSQLS
from webcrawl.handleRequest import requGet, requPost, getHtmlNodeContent, getXmlNodeContent
from webcrawl.atlas import convertBtoG
from webcrawl.character import unicode2utf8

from webcrawl.work import initflow, index, retry, next, timelimit, store
from multilog.aboutfile import modulename, modulepath
from multilog.prettyprint import logprint
from hotelspider import SpiderHotelOrigin, withDB, Data, WDB

print '====>>>>', WDB

_print, logger = logprint(modulename(__file__), modulepath(__file__))

class SpiderHtinns(SpiderHotelOrigin):
    """
       华住官网 数据爬虫
    """
    def __init__(self, worknum=30, queuetype='P', worktype='GEVENT', timeout=-1):
        self.clsname = str(self.__class__).split(".")[-1].replace("'>", "")
        super(SpiderHtinns, self).__init__(worknum=worknum, queuetype=queuetype, worktype=worktype, timeout=timeout)
        self.bt = datetime.datetime.now().strftime('%Y-%m-%d')
        self.et = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    @store(withDB(WDB), Data.insert, update=True, method='MANY')
    @timelimit(3)
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
        data = {"hotelID":"","CheckInDate":"","CheckOutDate":"","QueryRoomType":"","activityID":""}
        data['CheckInDate'] = self.bt
        data['CheckOutDate'] = self.et
        data['hotelID'] = hotel_id
        cookies = {"Origin":"http://i.huazhu.com","Referer":"http://i.huazhu.com/hotel/detail/%s" % hotel_id}
        main_resp = requPost(url, data, cookies=cookies, timeout=timeout, format='JSON')
        hotel = main_resp['Data']['Hotel']['Info']
        hotel_type = self.clscon['srctype']
        hotel_name = hotel['HotelName']
        address = ''
        lat = float(hotel['Lat'] or 0)
        lnt = float(hotel['Lng'] or 0)
        tel = hotel['Telephone']
        logo = hotel['HotelImage'][0]['ImageUrl'] if len(hotel['HotelImage']) > 0 else ''
        status = 2
        hotel_one = Hotel(hotel_id=hotel_id,
                        hotel_type=hotel_type,
                        hotel_name=hotel_name,
                        address=address,
                        lat=lat,
                        lnt=lnt,
                        tel=tel,
                        logo=logo,
                        status=status,
                        city=city,
                        hotel_prefix=hotel_prefix,
                        create_time=createtime
            )
        yield hotel_one

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
        page = url.split('###')[-1]
        url = url.split('###')[0]
        data = {"CheckInDate":"","CheckOutDate":"","PageIndex":"","PageSize":"","SortBy":"0","CityID":"","ActivityID":"","QueryRoomType":"","KeyWord":"","Latlng":"","IsPointExchangRoom":""}
        data['CheckInDate'] = self.bt
        data['CheckOutDate'] = self.et
        data['PageIndex'] = page
        data['PageSize'] = 15
        data['CityID'] = additions['cid']
        main_resp = requPost(url, data, timeout=timeout, format='JSON')
        allhotels = main_resp['Data']['HotelList']
        if len(allhotels) == data['PageSize']:
            next = int(page) + 1
        else:
            next = 0
        if next > 0:
            next_page = url + '###' + str(next)
        else:
            next_page = None
        yield next_page
        for hotel in allhotels:
            hotel_id =hotel['Info']['ID']
            if 'hotelids' in additions and not hotel_id in additions['hotelids']:
                continue
            yield {'url':'http://i.huazhu.com/api/hotel/detail', 'hotel_id':hotel_id}

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
        main_resp = requPost(url, data, timeout=timeout, format='JSON')
        provinces = main_resp['Data']['CityList']
        for prov in provinces[:3]:
            city = prov['CityName']
            if 'citys' in additions and not city in additions['citys']:
                continue
            print city
            yield {'url':'http://i.huazhu.com/api/hotel/list###0', 'city':city, 'additions':{'NUM':0, 'cid':prov['CityID']}}

if __name__ == '__main__':

    print 'start'
    spider = SpiderHtinns(worknum=6, queuetype='P', worktype='THREAD')
    spider.fetchDatas('www', 'http://i.huazhu.com/api/City/GetCityList')
    spider.statistic()
    # spider.extractFlow()
    # spider.fire('http://www.homeinns.com/')
    print 'end'