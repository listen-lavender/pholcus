#!/usr/bin/python
# coding=utf-8

"""
   从 如家官网 渠道抓取酒店数据
"""

import datetime
import re

from task.config.web.hotel import TIMEOUT, SERVICES, INSERTSQLS
from webcrawl.handleRequest import respGet, respPost, getHtmlNodeContent, getXmlNodeContent
from webcrawl.atlas import convertBtoG
from webcrawl.character import unicode2utf8

from webcrawl.work import initflow, index, retry, next, timelimit
from multilog.aboutfile import modulename, modulepath
from multilog.prettyprint import logprint
from hotelspider import SpiderHotelOrigin

_print, logger = logprint(modulename(__file__), modulepath(__file__))

class SpiderPodinns(SpiderHotelOrigin):
    """
       如家官网 数据爬虫
    """
    def __init__(self, worknum=30, queuetype='P', worktype='COROUTINE', timeout=-1):
        super(SpiderPodinns, self).__init__(worknum=worknum, queuetype=queuetype, worktype=worktype, timeout=timeout)
        self.areas = {}

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
        hotel_name = getHtmlNodeContent(main_resp.find('.//ul[@class="dian_name"]//h1'), 'TEXT')
        if hotel_id in self.areas:
            admin_area = self.areas[hotel_id]['admin_area']
            business_area = self.areas[hotel_id]['business_area']
        else:
            admin_area = ''
            business_area = ''
        star_rate = 2
        landmark = ''
        info1 = main_resp.find('.//div[@class="dian_txt"]')
        info1 = info1.findall('.//li')
        info1.extend([None, None, None, None])
        address = getHtmlNodeContent(info1[0], 'TEXT').replace('地址：','').replace('查看地图','')
        url = 'http://www.podinns.com/Hotel/HotelMapDetail?no=%s' % hotel_id
        map_resp = respGet(url, timeout=timeout, format='HTML')
        script = ''.join(getHtmlNodeContent(one, 'TEXT') for one in map_resp.findall('.//script'))
        latlntRE = re.compile('address = ".*";')
        latlnt = latlntRE.search(script)
        latlnt = latlnt.group(0).replace('address = "', '').replace('";', '').split(',') if latlnt is not None else [0, 0]
        if len(latlnt) < 2:
            latlnt = [0, 0]
        lnt, lat = float(latlnt[0]), float(latlnt[1])
        lat, lnt = convertBtoG(lat, lnt)
        telstr = getHtmlNodeContent(info1[1], 'TEXT').replace('\r\n', '::').replace(' ','').replace(' ', '')
        telstr = telstr.split('::')
        tel = telstr[-1].split('：')[-1]
        if tel == '筹':
            tel = telstr[0].split('：')[-1]
        manager_tel = ''
        fax = ''
        logo = main_resp.find('.//div[@class="dian_img"]')
        logo = logo.findall('.//img') if logo is not None else []
        logo.append(None)
        logo = getHtmlNodeContent(logo[0], {'ATTR':'src'})
        car = getHtmlNodeContent(map_resp, {'ATTR':'value'}, 'input', {'id':'PH_GO_CAR'})
        bus = getHtmlNodeContent(map_resp, {'ATTR':'value'}, 'input', {'id':'PH_GO_BUS'})
        traffic = car + bus if car == '' else car + '\n' + bus
        info2 = info1[3].findall('.//span') if info1[3] is not None else []
        info2.extend([None, None, None])
        introduce = getHtmlNodeContent(info2[0], 'TEXT') + getHtmlNodeContent(info2[1], {'ATTR':'data'}) + getHtmlNodeContent(info2[2], 'TEXT')
        build_time = ''
        decorate_time = ''
        status = 2 if '（筹' in hotel_name or '(筹' in hotel_name else 1
        status_desc = SERVICES['status_desc'][str(status)]
        servcodes = {'public_wifi':'N', 'wifi':'N', 'parking':'N', 'dining_room':'N', 'meeting_room':'N', 'swimming_pool':'N', 'gym':'N', 'morning_call':'N', 'luggage':'N', 'laundry':'N'}
        for item in main_resp.findall('.//div[@class="publicitem"]//span'):
            item = getHtmlNodeContent(item, {'ATTR':'class'})
            if item == 'pibg icon_s1':
                servcodes['public_wifi'] = 'Y'
            elif item == 'pibg icon_s7':
                servcodes['luggage'] = 'Y'
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
        city = getHtmlNodeContent(main_resp.find('.//div[@class="listmap"]//h4'), 'TEXT').replace('布丁酒店预订', '')
        extra = ''
        hotel_prefix = self.clscon['prefix']
        for one in ['布丁', '智尚', 'Zhotels']:
            if one in hotel_name:
                hotel_prefix = one
        else:
            hotel_prefix = self.clscon['prefix']
        createtime = SpiderHotelOrigin.uniquetime().strftime('%Y-%m-%d %H:%M:%S')
        hotel_one = (hotel_id, hotel_type, hotel_name, admin_area, business_area, star_rate, landmark, address, lat, lnt, tel, manager_tel, fax, logo, traffic, introduce, build_time, decorate_time, status, status_desc, wifi, public_wifi, parking, dining_room, meeting_room, swimming_pool, gym, morning_call, luggage, laundry, city, extra, hotel_prefix, createtime)
        hotel_one = unicode2utf8(hotel_one)
        yield (hotel_one,)

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
        areascomms = main_resp.findall('.//div[@class="menuyuding_titlebg"]')
        try:
            for one in areascomms:
                if getHtmlNodeContent(one, 'TEXT') == '行政区域':
                    areas_datas = one.getnext().findall('.//a')
                    for are in areas_datas:
                        area_resp = respGet(self.url_base[:-1] + getHtmlNodeContent(are, {'ATTR':'href'}), timeout=timeout, format='HTML')
                        hos = area_resp.findall('.//div[@class="menuyuding_jiudianname"]')
                        for a in hos:
                            href = getHtmlNodeContent(a, {'ATTR':'href'}, 'a')
                            aid = href[href.rindex('/')+1:-5]
                            if aid in self.areas:
                                self.areas[aid]['admin_area'] = getHtmlNodeContent(are, 'TEXT').replace('.', '').split('(')[0]
                            else:
                                self.areas[aid] = {'admin_area':getHtmlNodeContent(are, 'TEXT').replace('.', '').split('(')[0],'business_area':''}
        except:
            pass
        try:
            for one in areascomms:
                if getHtmlNodeContent(one, 'TEXT') == '商圈地标':
                    commercial_datas = one.getnext().findall('.//a')
                    for comm in commercial_datas:
                        comm_resp = respGet(self.url_base[:-1] + getHtmlNodeContent(comm, {'ATTR':'href'}), timeout=timeout, format='HTML')
                        hos = comm_resp.findall('.//div[@class="menuyuding_jiudianname"]')
                        for a in hos:
                            href = getHtmlNodeContent(a, {'ATTR':'href'}, 'a')
                            aid = href[href.rindex('/')+1:-5]
                            if aid in self.areas:
                                self.areas[aid]['business_area'] = getHtmlNodeContent(comm, 'TEXT').replace('.', '').split('(')[0]
                            else:
                                self.areas[aid] = {'admin_area':'','business_area':getHtmlNodeContent(comm, 'TEXT').replace('.', '').split('(')[0]}
        except:
            pass
        allhotels = main_resp.findall('.//div[@class="menuyuding_jiudianname"]')
        for hotel in allhotels:
            hotel_id = getHtmlNodeContent(hotel, {'ATTR':'href'}, 'a')
            hotel_id = hotel_id[hotel_id.rindex('/')+1:hotel_id.rindex('.')]
            if 'hotelids' in additions and not hotel_id in additions['hotelids']:
                continue
            yield {'url':'http://www.podinns.com/Hotel/HotelDetail/%s.html' % hotel_id, 'hotel_id':hotel_id}

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
        main_resp = respGet(url, timeout=timeout, format='HTML')
        provinces = main_resp.findall('.//div[@id="left_content"]//a')
        for prov in provinces:
            cpinyin = getHtmlNodeContent(prov, {'ATTR':'href'})
            cpinyin = cpinyin[cpinyin.rindex('/')+1:cpinyin.rindex('.')]
            city = getHtmlNodeContent(prov, 'TEXT')
            if 'citys' in additions and not city in additions['citys']:
                continue
            yield {'url':'http://www.podinns.com/Hotel/CInfo/%s.html' % cpinyin, 'city':city}

if __name__ == '__main__':

    print 'start'
    spider = SpiderPodinns(worknum=6, queuetype='P', worktype='COROUTINE')
    spider.fetchDatas('www', 'http://www.podinns.com/Hotel/AreaSearch')
    spider.statistic()
    # spider.extractFlow()
    # spider.fire('http://www.homeinns.com/')
    print 'end'
