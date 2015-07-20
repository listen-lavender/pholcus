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

class Spider998(SpiderHotelOrigin):
    """
       如家官网 数据爬虫
    """
    def __init__(self, worknum=30, queuetype='P', worktype='COROUTINE', timeout=-1):
        super(Spider998, self).__init__(worknum=worknum, queuetype=queuetype, worktype=worktype, timeout=timeout)
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
        data={'hotelcode':hotel_id}
        main_resp = respPost(url, data, timeout=30, format='HTML')
        hotel_type = self.clscon['srctype']
        hotel_name = getHtmlNodeContent(main_resp.find('.//h2[@itemprop="name"]//span'), 'TEXT')
        if '市' in hotel_name:
            hotel_name = hotel_name[:12] + hotel_name[hotel_name.index('市')+len('市'):]
        elif '省' in hotel_name:
            hotel_name = hotel_name[:12] + hotel_name[hotel_name.index('省')+len('省'):]

        admin_area = ''
        business_area = ''
        star_rate = 2
        landmark = ''
        address = getHtmlNodeContent(main_resp.findall('.//div[@class="adress"]//span')[1], 'TEXT')
        latlnt = ';;;;'.join(getHtmlNodeContent(one, 'TEXT') for one in main_resp.findall('.//script'))
        if "var pointXY = '" in latlnt:
            latlnt = latlnt[latlnt.index("var pointXY = '")+len("var pointXY = '"):]
            latlnt = latlnt[:latlnt.index("';")].split(',')
        else:
            latlnt = ['0.0', '0.0']
        if len(latlnt) == 2:
            lat = float(latlnt[0] or 0)
            lnt = float(latlnt[1] or 0)
            lat, lnt = convertBtoG(lat, lnt)
        else:
            lat, lnt = 0.0, 0.0
        tel = getHtmlNodeContent(main_resp.findall('.//div[@class="yd_text_main clearfix"]//div[@class="yd_tbts clearfix"]')[2].findall('.//p//span')[0], 'TEXT').replace('酒店总机: ', '').replace('酒店总机:', '').replace('暂无', '')
        manager_tel = ''
        fax = getHtmlNodeContent(main_resp.findall('.//div[@class="yd_text_main clearfix"]//div[@class="yd_tbts clearfix"]')[2].findall('.//p//span')[1], 'TEXT').replace('酒店传真: ', '').replace('酒店传真:', '').replace('暂无', '')
        logo = additions.get('logo', '')
        traffic = ''
        introduce = getHtmlNodeContent(main_resp.findall('.//div[@class="yd_text_main clearfix"]//div[@class="yd_tbts clearfix"]')[3].findall('.//p')[1], 'TEXT')
        build_time = getHtmlNodeContent(main_resp.findall('.//div[@class="yd_text_main clearfix"]//div[@class="yd_tbts clearfix"]')[3].findall('.//p')[0], 'TEXT').replace('酒店开业时间:', '')
        decorate_time = ''
        status = 2 if '筹备' in hotel_name else 1
        status_desc = SERVICES['status_desc'][str(status)]
        servcodes = {'public_wifi':'N', 'wifi':'N', 'parking':'N', 'dining_room':'N', 'meeting_room':'N', 'swimming_pool':'N', 'gym':'N', 'morning_call':'N', 'luggage':'N', 'laundry':'N'}
        serv_table = []
        for one in main_resp.findall('.//div[@class="htl_info_table"]//td'):
            one = getHtmlNodeContent(one, 'TEXT').strip(';')
            if ';' in one:
                serv_table.extend(one.split(';'))
            else:
                serv_table.append(one)
        for one in serv_table:
            if '大堂无线网络' in one and '有' in one:
                servcodes['public_wifi'] = 'Y'
            elif 'wifi' in one.lower() and '有' in one:
                servcodes['wifi'] = 'F'
            elif '餐厅' in one and '有' in one:
                servcodes['dining_room'] = 'D'
            elif '停车场' in one and '有' in one:
                if '是免费' in one:
                    servcodes['parking'] = 'F'
                else:
                    servcodes['parking'] = 'C'
            elif '洗衣' in one and '有' in one:
                servcodes['laundry'] = 'Y'
            elif '健身' in one and '有' in one:
                servcodes['gym'] = 'Y'
            elif '行李寄存' in one and '有' in one:
                servcodes['luggage'] = 'Y'
            elif '会议室' in one and '有' in one:
                servcodes['meeting_room'] = 'Y'
            elif '游泳' in one and '有' in one:
                servcodes['swimming_pool'] = 'Y'
            elif '叫醒' in one and '有' in one:
                servcodes['morning_call'] = 'Y'
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
        city = getHtmlNodeContent(main_resp.find('.//a[@id="HotelDetailCityText"]'), {'ATTR':'title'}).replace('酒店', '').replace('市', '')
        extra = getHtmlNodeContent(main_resp.findall('.//div[@class="yd_text_main clearfix"]//div[@class="yd_tbts clearfix"]')[0].find('.//p'), 'TEXT').replace('"', '')
        extra = extra if '提供' in extra or '免费' in extra or '配备' in extra else ''
        hotel_prefix = self.clscon['prefix']
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
        page = int(url.split('###')[-1])
        url = url.split('###')[0]
        pagesize = 20
        data={'cityId':additions['cid'], 'PageIndex':str(page), 'PageSize':pagesize, 'startDate':self.bt, 'endDate':self.et}
        main_resp = respPost(url, data, timeout=timeout, format='JSON')
        allhotels = main_resp['HotelInfoViewList']
        if len(allhotels) == pagesize:
            next = page + 1
        else:
            next = 0
        if next > 1:
            next_page = url + '###' + str(next)
        else:
            next_page = None
        yield next_page
        for hotel in allhotels:
            hotel_id = hotel['HotelCode']
            logo = hotel['HotelImg']
            if 'hotelids' in additions and not hotel_id in additions['hotelids']:
                continue
            yield {'url':'http://www.998.com/HotelDetail/Index', 'hotel_id':hotel_id, 'additions':{'logo':logo}}

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
        main_resp = respPost(url, data={}, timeout=timeout, format='JSON')
        for prov in main_resp:
            city = prov['Name']
            if 'citys' in additions and not city in additions['citys']:
                continue
            yield {'url':'http://www.998.com/HotelList/SearchHotelList###1', 'city':city, 'additions':{'cid':prov['Cityid']}}

if __name__ == '__main__':

    print 'start'
    spider = Spider998(worknum=6, queuetype='P', worktype='THREAD')
    spider.fetchDatas('www', 'http://www.998.com/HotelList/GetCityList')
    spider.statistic()
    # spider.extractFlow()
    # spider.fire('http://www.homeinns.com/')
    print 'end'
