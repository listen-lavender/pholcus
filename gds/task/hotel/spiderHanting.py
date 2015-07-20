#!/usr/bin/python
# coding=utf-8

"""
   从 华住官网 渠道抓取酒店数据
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

class SpiderHtinns(SpiderHotelOrigin):
    """
       华住官网 数据爬虫
    """
    def __init__(self, worknum=30, queuetype='P', worktype='COROUTINE', timeout=-1):
        super(SpiderHtinns, self).__init__(worknum=worknum, queuetype=queuetype, worktype=worktype, timeout=timeout)
        self.bt = datetime.datetime.now().strftime('%Y-%m-%d')
        self.et = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    @next(SpiderHotelOrigin.store, 'www', 'mysql', template=INSERTSQLS['fetchhotel'])
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
        main_resp = respPost(url, data, cookies=cookies, timeout=timeout, format='JSON')
        hotel = main_resp['Data']['Hotel']['Info']
        hotel_type = self.clscon['srctype']
        hotel_name = hotel['HotelName']
        admin_area = ''
        business_area = ''

        star_rate = 2 # mark
        landmark = '' # mark
        address = hotel['Address'] + '（'
        address = address.split('（')[0]


        lat = float(hotel['Lat'] or 0)
        lnt = float(hotel['Lng'] or 0)

        tel = hotel['Telephone']
        manager_tel = '' #mark
        fax = hotel['Fax']
        logo = hotel['HotelImage'][0]['ImageUrl'] if len(hotel['HotelImage']) > 0 else ''
        traffic = ''
        introduce = hotel['Descript']
        build_time = ''
        decorate_time = ''
        status = 2 if '（筹' in hotel_name or '(筹' in hotel_name else 1
        status_desc = SERVICES['status_desc'][str(status)]
        servcodes = {'public_wifi':'N', 'wifi':'N', 'parking':'N', 'dining_room':'N', 'meeting_room':'N', 'swimming_pool':'N', 'gym':'N', 'morning_call':'N', 'luggage':'N', 'laundry':'N'}
        for it in hotel['HotelFacility']:
            it = it['Name'] + it['Descript']
            if '宽带' in it or 'wifi' in it.lower() or '上网' in it or '无线' in it:
                servcodes['public_wifi'] = 'N' if '无' in it or '未' in it else 'Y'
            if '洗衣' in it:
                servcodes['laundry'] = 'N' if '无' in it or '未' in it else 'Y'
            if '会议' in it:
                servcodes['meeting_room'] = 'N' if len(it)==0 or '无' in it else 'Y'
            if '停车' in it:
                if '收费' in it:
                    servcodes['parking'] = 'C'
                elif '无' in it or len(it) == 0:
                    servcodes['parking'] = 'N'
                else:
                    servcodes['parking'] = 'F'
            if '餐' in it:
                servcodes['dining_room'] =  'N' if '无' in it or '未' in it else 'D'
            if '叫醒' in it:
                servcodes['morning_call'] = 'N' if '无' in it else 'Y'
            if '健身' in it:
                servcodes['gym'] = 'N' if '无' in it else 'Y'
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
        city = hotel['CityName']
        extra = '' #mark
        hotel_prefix = self.clscon['prefix']
        createtime = SpiderHotelOrigin.uniquetime().strftime('%Y-%m-%d %H:%M:%S')
        hotel_one = (hotel_id, hotel_type, hotel_name, admin_area, business_area, star_rate, landmark, address, lat, lnt, tel, manager_tel, fax, logo, traffic, introduce, build_time, decorate_time, status, status_desc, wifi, public_wifi, parking, dining_room, meeting_room, swimming_pool, gym, morning_call, luggage, laundry, city, extra, hotel_prefix, createtime)
        hotel_one = unicode2utf8(hotel_one)
        print hotel_one
        yield (hotel_one,)

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
        main_resp = respPost(url, data, timeout=timeout, format='JSON')
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
        print 'dddd'
        data = {}
        main_resp = respPost(url, data, timeout=timeout, format='JSON')
        provinces = main_resp['Data']['CityList']
        for prov in provinces:
            city = prov['CityName']
            if 'citys' in additions and not city in additions['citys']:
                continue
            print city
            yield {'url':'http://i.huazhu.com/api/hotel/list###0', 'city':city, 'additions':{'NUM':0, 'cid':prov['CityID']}}
            break

if __name__ == '__main__':

    print 'start'
    spider = SpiderHtinns(worknum=6, queuetype='P', worktype='COROUTINE')
    spider.fetchDatas('www', 'http://i.huazhu.com/api/City/GetCityList')
    spider.statistic()
    # spider.extractFlow()
    # spider.fire('http://www.homeinns.com/')
    print 'end'
