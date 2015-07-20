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

class SpiderHomeinns(SpiderHotelOrigin):
    """
       如家官网 数据爬虫
    """
    def __init__(self, worknum=30, queuetype='P', worktype='COROUTINE', timeout=-1):
        super(SpiderHomeinns, self).__init__(worknum=worknum, queuetype=queuetype, worktype=worktype, timeout=timeout)

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
        hotel_name = getHtmlNodeContent(main_resp.find('.//div[@class="hotelname"]'), 'TEXT')
        if hotel_name.startswith('M'):
            hotel_name = hotel_name.replace('M', '莫泰-')
        elif hotel_id.startswith('M') and not '莫泰' in hotel_name:
            hotel_name = '莫泰-' + hotel_name.replace('如家', '')
        hotel_name = hotel_name.replace('-', '').replace('168', '')

        admin_area = ''
        business_area = getHtmlNodeContent(main_resp.find('.//div[@class="describe"]//div[@class="bd"]'), 'TEXT').strip(',')

        star_rate = 2 # mark
        landmark = '' # mark
        address = getHtmlNodeContent(main_resp.find('.//div[@class="address"]//div[@class="bd"]'), 'TEXT')
        try:
            lat = float(getHtmlNodeContent(main_resp.find('.//input[@id="zuobiao_y"]'), {'ATTR':'value'}))
            lnt = float(getHtmlNodeContent(main_resp.find('.//input[@id="zuobiao_x"]'), {'ATTR':'value'}))
            lat, lnt = convertBtoG(lat, lnt)
        except:
            lat, lnt = 0.0, 0.0

        tel = getHtmlNodeContent(main_resp.find('.//div[@class="tel"]'), 'TEXT').replace('电话：', '').strip('"').replace('gethotelfail', '')
        manager_tel = '' #mark
        fax = '' #mark
        logo = getHtmlNodeContent(main_resp.find('.//div[@class="m_img"]//img'), {'ATTR':'src'})
        traffic = '\n'.join(getHtmlNodeContent(sec, 'TEXT').replace(' ', '') for sec in main_resp.findall('.//div[@class="search_yule"]//p'))
        introduce = getHtmlNodeContent(main_resp.find('.//div[@class="m_content"]'), 'TEXT').strip('"')
        build_time = ''
        decorate_time = '' #mark
        status = 2 if '停' in getHtmlNodeContent(main_resp.find('.//div[@id="duiduipeng"][@class="home_tishi"]'), 'TEXT') or '（筹' in hotel_name or '(筹' in hotel_name else 1
        status_desc = SERVICES['status_desc'][str(status)]
        servcodes = {'public_wifi':'N', 'wifi':'N', 'parking':'N', 'dining_room':'N', 'meeting_room':'N', 'swimming_pool':'N', 'gym':'N', 'morning_call':'N', 'luggage':'N', 'laundry':'N'}
        for it in main_resp.findall('.//div[@class="list_intro_icon"]//span'):
            title = getHtmlNodeContent(it, {'ATTR':'title'})
            if '停车位' in title:
                servcodes['parking'] = 'F'
            if '覆盖' in title:
                servcodes['public_wifi'] = 'Y'
                servcodes['wifi'] = 'F'
            if '洗衣' in title:
                servcodes['laundry'] = 'Y'
            if '行李' in title:
                servcodes['luggage'] = 'Y'
            if '游泳池' in title:
                servcodes['swimming_pool'] = 'O'
            if '会议' in title or '厅' in title:
                servcodes['meeting_room'] = 'Y'
            if '餐厅' in title:
                servcodes['dining_room'] =  'D'
            if '叫醒' in title:
                servcodes['morning_call'] = 'Y'
            if '健身' in title:
                servcodes['gym'] = 'Y'
        if '无线网络全覆盖' in getHtmlNodeContent(main_resp.find('.//div[@class="goodness"]'), 'TEXT'):
            servcodes['public_wifi'] = 'Y'
            servcodes['wifi'] = 'F'
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
        city = getHtmlNodeContent(main_resp.find('.//div[@class="city_ruzhu floatleft"]'), 'TEXT').replace('入住城市：', '')
        extra = '' #mark
        hotel_prefix = self.clscon['prefix']
        createtime = SpiderHotelOrigin.uniquetime().strftime('%Y-%m-%d %H:%M:%S')
        introduce = introduce[:-1] if introduce.endswith('\\') else introduce
        if hotel_name.startswith('莫泰'):
            hotel_type = '015'
            hotel_prefix = '莫泰'
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
        main_resp = respGet(url, timeout=timeout, format='HTML')
        allhotels = main_resp.findall('.//div[@class="list_tj"]')
        pages = main_resp.find('.//div[@class="page"]//a[@mk="True"]')
        try:
            next = int(getHtmlNodeContent(pages.getnext(), 'TEXT') or 0)
        except:
            next = 0
        if next > 1:
            next_page = url[:url.rindex('/')] + '/p' + str(next)
        else:
            next_page = None
        yield next_page
        for hotel in allhotels:
            hotel_id = getHtmlNodeContent(hotel.find('.//div[@class="list_intro_img"]//a'), {'ATTR':'hotelcd'})
            if 'hotelids' in additions and not hotel_id in additions['hotelids']:
                continue
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
        main_resp = respPost(url, {}, timeout=timeout, format='HTML')
        provinces = []
        provinces.extend(main_resp.findall('.//ul[@id="a_f"][@class="zb_pop_se ABCDEF"]//li'))
        provinces.extend(main_resp.findall('.//ul[@id="g_j"][@class="zb_pop_se GHIJ"]//li'))
        provinces.extend(main_resp.findall('.//ul[@id="k_n"][@class="zb_pop_se KLMN"]//li'))
        provinces.extend(main_resp.findall('.//ul[@id="p_w"][@class="zb_pop_se PQRSTUVW"]//li'))
        provinces.extend(main_resp.findall('.//ul[@id="x_z"][@class="zb_pop_se XYZ"]//li'))
        for province in provinces:
            city = getHtmlNodeContent(province.find('.//a'), 'TEXT')
            if 'citys' in additions and not city in additions['citys']:
                continue
            yield {'url':'http://www.homeinns.com/%s/p1' % getHtmlNodeContent(province.find('.//span[@class="pop_pinyin"]'), 'TEXT'), 'city':city}

if __name__ == '__main__':

    print 'start'
    spider = SpiderHomeinns(worknum=6, queuetype='P', worktype='COROUTINE')
    spider.fetchDatas('www', 'http://www.homeinns.com/')
    spider.statistic()
    # spider.extractFlow()
    # spider.fire('http://www.homeinns.com/')
    print 'end'
