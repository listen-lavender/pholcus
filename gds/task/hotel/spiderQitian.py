#!/usr/bin/python
# coding=utf-8

"""
   从 7天官网 渠道抓取酒店数据
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

class Spider7day(SpiderHotelOrigin):
    """
       7天官网 数据爬虫
    """
    def __init__(self, worknum=30, queuetype='P', worktype='COROUTINE', timeout=-1):
        super(Spider7day, self).__init__(worknum=worknum, queuetype=queuetype, worktype=worktype, timeout=timeout)

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
        main_resp = respGet(url, timeout=timeout, format='HTML')
        hotel_type = self.clscon['srctype']
        hotel_name = getHtmlNodeContent(main_resp.find('.//span[@class="title"]'), 'TEXT')
        admin_area = ''
        business_area = ''
        star_rate = 2
        landmark = ''
        aboutinfo = main_resp.findall('.//div[@class="left-bottom-wrapper"]//p')
        aboutinfo.extend([None, None])
        address = getHtmlNodeContent(aboutinfo[0], 'TEXT').replace('地址：', '')
        brand = additions.get('brand', None)
        lat, lnt = convertBtoG(additions.get('blat', 0), additions.get('blng', 0))
        tel = getHtmlNodeContent(aboutinfo[1], 'TEXT').replace('电话：', '')
        manager_tel = ''
        fax = ''
        logo = additions.get('logo', None)
        traffic = '；'.join(getHtmlNodeContent(one, 'TEXT') for one in main_resp.findall('.//div[@class="rigth-bottom-wrapper border-lrb bg"]//span[@class="s2"]//td'))
        introduce = getHtmlNodeContent(main_resp.find('.//div[@class="left-bottom-show"]//span'), 'TEXT')
        build_time = ''
        decorate_time = ''
        status = 2 if '（筹' in hotel_name or '(筹' in hotel_name else 1
        status_desc = SERVICES['status_desc'][str(status)]
        servcodes = {'public_wifi':'N', 'wifi':'N', 'parking':'N', 'dining_room':'N', 'meeting_room':'N', 'swimming_pool':'N', 'gym':'N', 'morning_call':'N', 'luggage':'N', 'laundry':'N'}
        serv_table = main_resp.findall('.//div[@id="ptss"]//li')
        for it in serv_table:
            txt = getHtmlNodeContent(it.find('.//em'), {'ATTR':'class'}) + ';' + getHtmlNodeContent(it.find('.//span'), 'TEXT').lower()
            if '大堂上网' in txt and 'true' in txt:
                servcodes['public_wifi'] = 'Y'
            if 'wifi' in txt and 'true' in txt:
                servcodes['wifi'] = 'F'
            if '停车' in txt and 'true' in txt:
                servcodes['parking'] = 'F'
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
        if brand == 2 or '7天优品' in hotel_name:
            hotel_name = '7天优品' + hotel_name
        elif brand == 3 or '7天阳光' in hotel_name:
            hotel_name = '7天阳光' + hotel_name
        elif brand == 93 or '铂涛菲诺' in hotel_name:
            hotel_name = '铂涛菲诺' + hotel_name
        elif brand == 92 or 'ZMAX潮漫' in hotel_name:
            hotel_name = 'ZMAX潮漫' + hotel_name
        elif brand == 91 or '喆·啡' in hotel_name:
            hotel_name = '喆·啡' + hotel_name
        elif brand == 90 or '麗枫' in hotel_name:
            hotel_name = '麗枫' + hotel_name
        elif brand and not brand == 1:
            pass
        else:
            hotel_name = '7天快捷酒店' + hotel_name
        createtime = SpiderHotelOrigin.uniquetime().strftime('%Y-%m-%d %H:%M:%S')
        hotel_one = (hotel_id, hotel_type, hotel_name, admin_area, business_area, star_rate, landmark, address, lat, lnt, tel, manager_tel, fax, logo, traffic, introduce, build_time, decorate_time, status, status_desc, wifi, public_wifi, parking, dining_room, meeting_room, swimming_pool, gym, morning_call, luggage, laundry, city, extra, hotel_prefix, createtime)
        hotel_one = unicode2utf8(hotel_one)
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
        main_resp = respGet(url, timeout=timeout, format='JSON')
        allhotels = main_resp['content']
        page = main_resp['number'] + 1
        try:
            next = page if page+1 < main_resp['totalPages'] else 0
        except:
            next = 0
        if next > 1:
            next_page = url[:url.rindex('=')+1] + str(next)
        else:
            next_page = None
        yield next_page
        for hotel in allhotels:
            hotel_id = hotel['innId']
            if 'hotelids' in additions and not hotel_id in additions['hotelids']:
                continue
            yield {'url':'http://www.plateno.com/hotel/pg/%s/detail.html' % str(hotel_id), 'hotel_id':hotel_id, 'additions':{'brand':hotel['brandId'], 'city':city, 'admin_area':hotel['districtName'], 'logo':'http://www.plateno.com/'+hotel['thumbnailPath'], 'blng':hotel['blng'], 'blat':hotel['blat']}}

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
        main_resp = respGet(url, timeout=timeout, format='JSON', dirtys=[('([{', '[{'), ('}])', '}]'),])
        for prov in main_resp:
            if 'citys' in additions and not prov['name'] in additions['citys']:
                continue
            yield {'url':'http://www.plateno.com/hotel/q/list?cityId=%s&pageSize=50&pageNumber=1' % str(prov['id']), 'city':prov['name']}

if __name__ == '__main__':

    print 'start'
    spider = Spider7day(worknum=6, queuetype='P', worktype='COROUTINE')
    spider.fetchDatas('www', 'http://www.plateno.com/geo/cities1.json?callback=')
    spider.statistic()
    # spider.extractFlow()
    # spider.fire('http://www.homeinns.com/')
    print 'end'
