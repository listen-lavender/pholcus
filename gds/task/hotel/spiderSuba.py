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

class SpiderSuper8(SpiderHotelOrigin):
    """
       如家官网 数据爬虫
    """
    def __init__(self, worknum=30, queuetype='P', worktype='COROUTINE', timeout=-1):
        super(SpiderSuper8, self).__init__(worknum=worknum, queuetype=queuetype, worktype=worktype, timeout=timeout)

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
        hotel_name = getHtmlNodeContent(main_resp.find('.//font[@class="hotelh3title"]'), 'TEXT')

        areasinfo = []
        for tr in main_resp.findall('.//div[@id="Description"]//tr'):
            if getHtmlNodeContent(tr, {'ATTR':'class'}) == 'aroundInfo':
                continue
            tds = tr.findall('.//td')
            tds.extend([None, None, None, None, None])
            areasinfo.append({'areaname':getHtmlNodeContent(tds[0], 'TEXT'),
                              'distance':float(getHtmlNodeContent(tds[1], 'TEXT').replace('公里', '').strip() or 0),
                              'traffictools':getHtmlNodeContent(tds[2], 'TEXT'),
                              'predictime':getHtmlNodeContent(tds[3], 'TEXT'),
                              'direction':getHtmlNodeContent(tds[4], 'TEXT')})
        admin_area = ''
        business_area = ','.join(k['areaname'] for k in areasinfo if k['distance'] < 2.1)

        star_rate = 2 # mark
        landmark = '' # mark
        addintro = main_resp.findall('.//div[@id="Description"]//p')
        addintro.extend([None, None])
        address = getHtmlNodeContent(addintro[1], 'TEXT').replace('地址：', '')

        url = 'http://www.super8.com.cn/Map/hotelMap.aspx?oid=%s' % hotel_id
        map_resp = respGet(url, timeout=timeout, format='TEXT')
        lat = re.search('var y = .*;', map_resp)
        lat = lat.group(0).split('\'') if lat is not None else []
        lat = float(lat[1] or 0) if len(lat)>1 else 0.0
        lnt = re.search('var x = .*;', map_resp)
        lnt = lnt.group(0).split('\'') if lnt is not None else []
        lnt = float(lnt[1] or 0) if len(lnt)>1 else 0.0
        lat, lnt = convertBtoG(lat, lnt)

        tel = ''
        manager_tel = '' #mark
        fax = '' #mark
        logo = main_resp.findall('.//div[@id="Description"]//img')
        logo.append(None)
        logo = getHtmlNodeContent(logo[0], {'ATTR':'src'})
        traffic = '；'.join('往' + k['direction'] + '距离' + k['areaname'] + str(k['distance']) + 'km.' + k['traffictools'] + '需' + k['predictime'] for k in areasinfo)
        introduce = getHtmlNodeContent(addintro[0], 'TEXT')
        build_time = ''
        decorate_time = '' #mark
        status = 2 if '（筹' in hotel_name or '(筹' in hotel_name else 1
        status_desc = SERVICES['status_desc'][str(status)]
        serv_resp = '\n'.join(getHtmlNodeContent(k, 'TEXT') for k in main_resp.findall('.//script') if getHtmlNodeContent(k, {'ATTR':'src'}) == '')
        fs = re.search('var serviceCns = .*split', serv_resp)
        fs = fs.group(0).split('\'') if fs is not None else []
        serv_table = fs[1] if len(fs) > 1 else ''
        fs = re.search('var FacilityCns = .*split', serv_resp)
        fs = fs.group(0).split('\'') if fs is not None else []
        serv_table = serv_table + ',' + fs[1] if len(fs) > 1 else serv_table
        serv_table = serv_table.split(',')
        servcodes = {'public_wifi':'N', 'wifi':'N', 'parking':'N', 'dining_room':'N', 'meeting_room':'N', 'swimming_pool':'N', 'gym':'N', 'morning_call':'N', 'luggage':'N', 'laundry':'N'}
        for one in serv_table:
            one = one.lower()
            servcodes['public_wifi'] = 'Y' if 'wifi' in one or '公共区域上网' in serv_table else 'N'
            servcodes['laundry'] = 'Y' if '洗衣' in one else 'N'
            servcodes['meeting_room'] = 'Y' if '会议' in one else 'N'
            if '停车' in one:
                if '收费' in one:
                    servcodes['parking'] = 'C'
                else:
                    servcodes['parking'] = 'F'
            servcodes['dining_room'] =  'D' if '餐厅' in one else 'N'
            servcodes['morning_call'] = 'Y' if '叫醒' in one else 'N'
            servcodes['gym'] = 'Y' if '健身' in one else 'N'
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
        introduce = introduce[:-1] if introduce.endswith('\\') else introduce
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
        main_resp = respGet(url, timeout=timeout, format='HTML')
        allhotels = main_resp.findall('.//font[@class="hotelh3title"]')
        pages = main_resp.find('.//td[@class=""][@valign="bottom"]')
        try:
            next = int(getHtmlNodeContent(pages.find('font').getnext().getnext(), 'TEXT') or 0)
        except:
            next = 0
        if next > 1:
            next_page = url[0:url.rindex('=')+1] + str(next)
        else:
            next_page = None
        yield next_page
        for hotel in allhotels:
            hotel_id = getHtmlNodeContent(hotel.getparent(), {'ATTR':'href'}).split("&")[0].split('=')[-1]
            if 'hotelids' in additions and not hotel_id in additions['hotelids']:
                continue
            yield {'url':'http://www.super8.com.cn/Hotel/HotelDetail.aspx?oid=%s' % hotel_id, 'hotel_id':hotel_id}

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
        nameRE = re.compile('酒店.*')
        main_resp = respGet(url, timeout=timeout, format='HTML')
        provinces = main_resp.findall('.//div[@class="hotellist"]//a[@style="color:red;"][@target="_blank"]')
        for prov in provinces:
            city = nameRE.sub('', getHtmlNodeContent(prov, 'TEXT'))
            if 'citys' in additions and not city in additions['citys']:
                continue
            yield {'url':'http://www.super8.com.cn/Hotel/HotelList.aspx?CityId=%s&__EVENTTARGET=AspNetPager&__EVENTARGUMENT=' % city, 'city':city}

if __name__ == '__main__':

    print 'start'
    spider = SpiderSuper8(worknum=6, queuetype='P', worktype='THREAD')
    spider.fetchDatas('www', 'http://www.super8.com.cn/Hotel/HotelCityList.aspx')
    spider.statistic()
    # spider.extractFlow()
    # spider.fire('http://www.homeinns.com/')
    print 'end'
