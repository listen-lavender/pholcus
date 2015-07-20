#!/usr/bin/python
# coding=utf-8

"""
   从 锦江之星官网 渠道抓取酒店数据
"""

import datetime
import json

from task.config.web.hotel import TIMEOUT, SERVICES, INSERTSQLS
from webcrawl.handleRequest import respGet, respPost, getHtmlNodeContent, getXmlNodeContent, treeHtml
from webcrawl.atlas import convertBtoG
from webcrawl.character import unicode2utf8

from webcrawl.work import initflow, index, retry, next, timelimit
from multilog.aboutfile import modulename, modulepath
from multilog.prettyprint import logprint
from hotelspider import SpiderHotelOrigin

_print, logger = logprint(modulename(__file__), modulepath(__file__))

class SpiderJjinns(SpiderHotelOrigin):
    """
       锦江之星官网 数据爬虫
    """
    def __init__(self, worknum=30, queuetype='P', worktype='COROUTINE', timeout=-1):
        super(SpiderJjinns, self).__init__(worknum=worknum, queuetype=queuetype, worktype=worktype, timeout=timeout)
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
        url = 'http://www.jinjianginns.com/hotel/hotelSingleLoad.ashx'
        data = {"unitid":hotel_id,"bt":self.bt,"et":self.et}
        info_resp = respPost(url, data, timeout=timeout, format='JSON')
        hotel_type = self.clscon['srctype']
        hotel_name = info_resp['unitTtitle'][info_resp['unitTtitle'].rindex(';')+1:]
        bs_detail1 = treeHtml(info_resp['unitSingle'], coding='utf-8')

        areas = bs_detail1.findall('.//span')
        areas.extend([None, None, None, None])
        areas = getHtmlNodeContent(areas[3], 'TEXT').split('|')
        areas.append('')
        admin_area = areas[0].replace('&nbsp', '').replace(';', '').strip()
        admin_area = admin_area if '区' in admin_area or '镇' in admin_area or '市' in admin_area else ''
        business_area = ','.join(are.replace('&nbsp', '').replace(';', '').strip() for are in areas[1:]).strip(',')
        if len(business_area) > 126:
            business_area = business_area[:min(len(business_area), 126)]
            business_area = business_area[:business_area.rindex(',')]

        star_rate = 2 # mark
        url = 'http://map.jinjianginns.com/Home/HotelPeriphery?hotelCode=%s' % hotel_id
        map_resp = respGet(url, timeout=timeout, format='HTML')
        latlnt = getHtmlNodeContent(map_resp.find('.//input[@id="fromsuggest"]'), {'ATTR':'lnglat'}).split(',')
        if len(latlnt) == 2:
            lat, lnt = float(latlnt[1].strip() or 0), float(latlnt[0].strip() or 0)
            lat, lnt = convertBtoG(lat, lnt)
        else:
            lat, lnt = 0.0, 0.0

        telitems = bs_detail1.findall('.//span[@class="itemHead"]')
        for one in telitems:
            one = getHtmlNodeContent(one.getparent(), 'TEXT')
            if '电话' in one and not '<' in one:
                tel = one.replace('电话', '')
                break
        else:
            tel = ''
        manager_tel = '' #mark
        fax = '' #mark
        bs_detail2 = treeHtml(info_resp['unitImg'], coding='utf-8')
        logo = bs_detail2.findall('.//img')
        logo = getHtmlNodeContent(logo[0], {'ATTR':'src'}) if logo else ''
        traffic = ''
        introduce = getHtmlNodeContent(bs_detail1.find('.//div'), 'TEXT')
        build_time = ''
        decorate_time = '' #mark
        status = 2 if '（筹' in hotel_name or '(筹' in hotel_name else 1
        status_desc = SERVICES['status_desc'][str(status)]
        bs_detail3 = treeHtml(info_resp['unitScore'], coding='utf-8')
        bs_detail4 = treeHtml(info_resp['unitDetail'], coding='utf-8')
        servcodes = {'public_wifi':'N', 'wifi':'N', 'parking':'N', 'dining_room':'N', 'meeting_room':'N', 'swimming_pool':'N', 'gym':'N', 'morning_call':'N', 'luggage':'N', 'laundry':'N'}
        for it in bs_detail2.findall('.//a'):
            ti = getHtmlNodeContent(it, {'ATTR':'title'})
            if ti:
                servcodes['meeting_room'] = 'Y' if '会议' in ti else 'N'
                servcodes['dining_room'] =  'D' if '餐' in ti else 'N'
        for it in bs_detail3.findall('.//td')[2:][::2]:
            ti = getHtmlNodeContent(it, 'TEXT')
            if ti:
                servcodes['public_wifi'] = 'Y' if '宽带' in ti or 'wifi' in ti.lower() or '网络' in ti or '无线' in ti else 'N'
                servcodes['laundry'] = 'Y' if '洗衣' in ti else 'N'
                servcodes['meeting_room'] = 'Y' if '会议' in ti else 'N'
                if '停车' in ti:
                    if '收费' in ti:
                        servcodes['parking'] = 'C'
                    else:
                        servcodes['parking'] = 'F'
                servcodes['dining_room'] =  'D' if '餐' in ti else 'N'
                servcodes['morning_call'] = 'Y' if '叫醒' in ti else 'N'
                servcodes['gym'] = 'Y' if '健身' in ti else 'N'
        for it in bs_detail4.findall('.//li[@class="greenBlt"]'):
            ti = getHtmlNodeContent(it, 'TEXT')
            if ti:
                servcodes['public_wifi'] = 'Y' if '宽带' in ti or 'wifi' in ti.lower() or '网络' in ti or '无线' in ti else 'N'
                servcodes['laundry'] = 'Y' if '洗衣' in ti else 'N'
                servcodes['meeting_room'] = 'Y' if '会议' in ti else 'N'
                if '停车' in ti:
                    if '收费' in ti:
                        servcodes['parking'] = 'C'
                    else:
                        servcodes['parking'] = 'F'
                servcodes['dining_room'] =  'D' if '餐' in ti else 'N'
                servcodes['morning_call'] = 'Y' if '叫醒' in ti else 'N'
                servcodes['gym'] = 'Y' if '健身' in ti else 'N'
        # url = 'http://map.jinjianginns.com/hotel/hotelSingleAbout.ashx'
        # data = {'unitid':hotel_id,'pageIndex':'1'}
        # lm_resp = respPost(url, data, timeout=timeout, format='HTML')
        # landmark = ','.join(getHtmlNodeContent(k, 'TEXT') for k in lm_resp.findall('.//font[@color="#000000"]'))
        landmark = ''
        address = getHtmlNodeContent(bs_detail1.findall('.//p')[0], 'TEXT').replace('地址', '')
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
        city = getHtmlNodeContent(bs_detail1.findall('.//p')[1].find('.//a'), 'TEXT')
        extra = '' #mark
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
        # main_resp = respGet(url, timeout=timeout, format='JSON')
        about = url.split('?')
        data = {'cityId':about[-1].split('=')[-1]}
        url = about[0]
        headers = {'Host':'www.jinjianginns.com', 'Origin':'http://www.jinjianginns.com', 'Referer':'http://www.jinjianginns.com/'}
        main_resp = respPost(url, data, headers=headers, timeout=timeout, format='JSON')
        for hotel in main_resp:
            hotel_id = hotel['Id']
            if 'hotelids' in additions and not hotel_id in additions['hotelids']:
                continue
            yield {'url':'http://www.jinjianginns.com/hotel/HotelSingle--%s.html' % hotel_id, 'hotel_id':hotel_id}

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
        main_resp = respGet(url, timeout=timeout, format='TEXT')
        main_resp = main_resp.split('var CITY_DATA_CHA')[0].replace('\n', '').replace(' ', '')
        main_resp = unicode2utf8(json.loads(main_resp[main_resp.index('=')+1:].decode('utf-8')))
        provinces = [(city['Id'], city['Name']) for city in main_resp if not ',' in city['Id'] and not '法国' in city['Name'] and not '朝鲜' in city['Name']]
        for prov in provinces:
            if 'citys' in additions and not prov[1] in additions['citys']:
                continue
            yield {'url':'http://www.jinjianginns.com/hotel/hotelSel_Name.ashx?cityid=%s' % prov[0], 'city':prov[1]}

if __name__ == '__main__':

    print 'start'
    spider = SpiderJjinns(worknum=6, queuetype='B', worktype='COROUTINE')
    spider.fetchDatas('www', 'http://www.jinjianginns.com/Js/CityData.js')
    spider.statistic()
    # spider.extractFlow()
    # spider.fire('http://www.homeinns.com/')
    print 'end'
