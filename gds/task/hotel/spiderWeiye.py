#!/usr/bin/python
# coding=utf-8

"""
   从 如家官网 渠道抓取酒店数据
"""

import datetime

from task.config.web.hotel import TIMEOUT, SERVICES, INSERTSQLS
from webcrawl.handleRequest import respGet, respPost, getHtmlNodeContent, getXmlNodeContent
from webcrawl.atlas import convertBtoG
from webcrawl.character import unicode2utf8

from webcrawl.work import initflow, index, retry, next, timelimit
from multilog.aboutfile import modulename, modulepath
from multilog.prettyprint import logprint
from hotelspider import SpiderHotelOrigin

_print, logger = logprint(modulename(__file__), modulepath(__file__))

class SpiderWyn88(SpiderHotelOrigin):
    """
       如家官网 数据爬虫
    """
    def __init__(self, worknum=30, queuetype='P', worktype='COROUTINE', timeout=-1):
        super(SpiderWyn88, self).__init__(worknum=worknum, queuetype=queuetype, worktype=worktype, timeout=timeout)

    @next(SpiderHotelOrigin.store, 'www', 'mysql', template=INSERTSQLS['fetchhotel'])
    # @next(SpiderHotelOrigin.store, 'www', 'mongo', template='official_hotel_info')
    @timelimit(3)
    def fetchMainWAPHotelone(self, url, hotel_id, additions={}, timeout=TIMEOUT, implementor=None):
        """
            根据url, hotel_id抓取一家官网酒店的信息
            @param url: 抓取地址
            @param hotel_id: 酒店ID
            @param additions: 附加内容
            @param timeout: 抓取超时
            @param implementor: 补充抓取器
            @return hotel_one: 一家酒店的信息
        """
        hotel_type = self.clscon['srctype']
        hotel_name = additions.get('hotel_name', '')
        admin_area = ''
        business_area = ''
        star_rate = int(additions.get('star_rate', 0))
        landmark = ''
        address = additions.get('address', '')
        try:
            lat = float(additions.get('lat', 0))
            lnt = float(additions.get('lnt', 0))
        except:
            lat = float(additions.get('lnt', 0).split('至')[0].replace('北纬', '').replace('°', '.').replace('′', ''))
            lnt = float(additions.get('lat', 0).split('至')[0].replace('东经', '').replace('°', '.').replace('′', ''))
        tel = additions.get('tel', '')
        manager_tel = ''
        fax = additions.get('fax', '')
        logo = additions.get('logo', '')
        traffic = ''
        introduce = additions.get('introduce', '')
        build_time = ''
        decorate_time = ''
        status = 2 if '筹备' in hotel_name else 1
        status_desc = SERVICES['status_desc'][str(status)]
        servcodes = {'public_wifi':'Y', 'wifi':'F', 'parking':'F', 'dining_room':'D', 'meeting_room':'Y', 'swimming_pool':'N', 'gym':'N', 'morning_call':'N', 'luggage':'Y', 'laundry':'N'}
        wifi = SERVICES['wifi'][servcodes['wifi']]
        public_wifi = SERVICES['public_wifi'][servcodes['public_wifi']]
        parking = SERVICES['parking'][servcodes['parking']]
        dining_room = SERVICES['dining_room'][servcodes['dining_room']]
        meeting_room = SERVICES['meeting_room'][servcodes['meeting_room']]
        swimming_pool = SERVICES['swimming_pool'][servcodes['swimming_pool']]
        gym = SERVICES['gym'][servcodes['gym']]
        morning_call = SERVICES['morning_call'][servcodes['morning_call']]
        luggage = SERVICES['luggage'][servcodes['luggage']]
        laundry = SERVICES['laundry'][servcodes['laundry']]
        city = additions.get('city', '')
        extra = ''
        hotel_prefix = self.clscon['prefix']
        createtime = SpiderHotelOrigin.uniquetime().strftime('%Y-%m-%d %H:%M:%S')
        hotel_one = (hotel_id, hotel_type, hotel_name, admin_area, business_area, star_rate, landmark, address, lat, lnt, tel, manager_tel, fax, logo, traffic, introduce, build_time, decorate_time, status, status_desc, wifi, public_wifi, parking, dining_room, meeting_room, swimming_pool, gym, morning_call, luggage, laundry, city, extra, hotel_prefix, createtime)
        # hotel_one = {'hotel_id':hotel_id, 'hotel_type':hotel_type, 'hotel_name':hotel_name, 'admin_area':admin_area, 'business_area':business_area, 'star_rate':star_rate, 'landmark':landmark, 'address':address, 'lat':lat, 'lnt':lnt, 'tel':tel, 'manager_tel':manager_tel, 'fax':fax, 'logo':logo, 'traffic':traffic, 'introduce':introduce, 'build_time':build_time, 'decorate_time':decorate_time, 'status':status, 'status_desc':status_desc, 'wifi':wifi, 'public_wifi':public_wifi, 'parking':parking, 'dining_room':dining_room, 'meeting_room':meeting_room, 'swimming_pool':swimming_pool, 'gym':gym, 'morning_call':morning_call, 'luggage':luggage, 'laundry':laundry, 'city':city, 'extra':extra, 'hotel_prefix':hotel_prefix, 'createtime':createtime}
        hotel_one = unicode2utf8(hotel_one)
        print hotel_one
        yield (hotel_one,)

    @index('url')
    @timelimit(6)
    @next(fetchMainWAPHotelone)
    def fetchMainWAPHotelids(self, url, city, additions={}, timeout=TIMEOUT, implementor=None):
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
        data = {'city':city,'pageIndex':int(page)} # ,'indate':'2015-02-11','outdate':'2015-02-12'
        main_resp = respPost(url, data, format='JSON')
        allhotels = main_resp['pageInfo']['Rows']
        if len(allhotels) == 10:
            next = int(page) + 1
        else:
            next = 0
        if next > 0:
            next_page = url + '###' + str(next)
        else:
            next_page = None
        yield next_page
        for hotel in allhotels:
            hotel_id = hotel['HotelCode']
            hotel_name = hotel['HotelName']
            address = hotel['Address']
            star_rate = hotel['StarLevel']
            admin_area = hotel['DistrictName']
            lat = hotel['Latitude']
            lnt = hotel['Longitude']
            tel = hotel['Tel']
            fax = hotel['Fax']
            logo = hotel['ImageUrl']
            introduce = hotel['Summary'].replace('<div>', '').replace('&nbsp;', '').replace('</div>', '').replace('&ldquo;', '').replace('&rdquo;', '')
            # city = hotel['CityName'].strip('市')
            if 'hotelids' in additions and not hotel_id in additions['hotelids']:
                continue
            yield {'url':'', 'hotel_id':hotel_id, 'additions':{'hotel_name':hotel_name, 'address':address, 'star_rate':star_rate, 'admin_area':admin_area, 'lat':lat, 'lnt':lnt, 'tel':tel, 'fax':fax, 'logo':logo, 'introduce':introduce, 'city':city}}

    @next(fetchMainWAPHotelids)
    @timelimit(20)
    @initflow('wap')
    def fetchMainWAPCitys(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        """
            抓取官网城市列表
            @param url: 抓取地址
            @param additions: 附加内容
            @param timeout: 抓取超时
            @param implementor: 补充抓取器
            @return city: 城市
        """
        main_resp = respGet(url, timeout=timeout, format='HTML')
        citys = main_resp.findall('.//ul[@class="ullst"]//li')
        for prov in main_resp.findall('.//ul[@class="ullst"]//li'):
            city = getHtmlNodeContent(prov.find('.//h3'), 'TEXT')
            # cid = getHtmlNodeContent(city.find('.//h3'), {'ATTR':'data-no'})
            if 'citys' in additions and not city in additions['citys']:
                continue
            yield {'url':'http://wap.wyn88.com/Hotel/GetAjaxHotel###1', 'city':city}

if __name__ == '__main__':

    print 'start'
    spider = SpiderWyn88(worknum=6, queuetype='P', worktype='COROUTINE')
    spider.fetchDatas('wap', 'http://wap.wyn88.com/Hotel/Index')
    spider.statistic()
    # spider.extractFlow()
    # spider.fire('http://www.homeinns.com/')
    print 'end'
