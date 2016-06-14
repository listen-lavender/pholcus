#!/usr/bin/env python
# coding=utf-8

from datetime import *
from webcrawl.character import *
from webcrawl.task import *
from shopspider import *
from webcrawl import request

import pymongo
mc = pymongo.MongoClient('localhost')
food = mc['food']['food']

class SpiderDianping(SpiderShopOrigin):

    """
       大众点评 数据爬虫
    """

    def __init__(self, worknum=6, queuetype='P', worktype='COROUTINE', timeout=-1, tid=0, settings={}, callback=None):
        super(SpiderDianping, self).__init__(worknum=worknum, queuetype=queuetype, worktype=worktype, timeout=timeout, tid=tid, settings=settings, callback=callback)
        self.clsname = self.__class__.__name__
        self.tid = tid

    @store(withData(datacfg.W), Data.insert, update=True, method='MANY')
    @timelimit(20)
    def fetchShopDetail(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        headers = {
            "User-Agent":"iPhone; CPU iPhone OS 9_1 like Mac OS X AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
        }
        result = request.get(url, headers=headers, timeout=timeout, format='HTML')
        food_id = [additions['food_id'], ]
        name = additions['name']
        desc = additions['desc']
        tel = additions['tel']
        pic = additions['pic']
        province_id = additions['province_id']
        city_id = additions['city_id']
        tag = []
        try:
            for one in result.findall('.//p[@class="info info-indent"]'):
                prompt = request.getHtmlNodeContent(one.find('.//span'), 'TEXT')
                if '标签' in prompt:
                    tag.extend([request.getHtmlNodeContent(a, 'TEXT') for a in one.findall('.//a')])
        except:
            pass

        area_id = additions['area_id']
        town_id = additions['town_id']
        country_id = additions['country_id']
        address = additions['address']
        longitude = additions['longitude']
        latitude = additions['latitude']

        dianping = {
            'url': url,
            'star': 0,
            'average': additions['average'],
            'taste': 0,
            'env': 0,
            'service': 0,
        }
        dianping_info = result.findall('.//div[@class="brief-info"]//span')
        try:
            dianping['star'] = request.getHtmlNodeContent(dianping_info[0], {'ATTR':'class'})
            dianping['star'] = dianping['star'].replace('mid-rank-stars mid-str', '')
            dianping['star'] = float('%s.%s' % (dianping['star'][0], dianping['star'][1:]))
            dianping['taste'] = float(request.getHtmlNodeContent(dianping_info[3], 'TEXT').replace('口味：', ''))
            dianping['env'] = float(request.getHtmlNodeContent(dianping_info[4], 'TEXT').replace('环境：', ''))
            dianping['service'] = float(request.getHtmlNodeContent(dianping_info[5], 'TEXT').replace('服务：', ''))
        except:
            pass

        src = '大众点评'
        link_url = url
        atime = datetime.now()
        uptime = atime
        time = atime

        print link_url, name

        time_result = request.get(url+'/editmember', headers=headers, timeout=timeout, format='HTML')
        time_info = time_result.findall('.//ul[@class="block-inner desc-list contribute-list Fix"]//li')
        try:
            for one in time_info:
                prompt = request.getHtmlNodeContent(one.find('.//strong'), 'TEXT')
                if '商户' in prompt:
                    atime = datetime.strptime('20%s' % request.getHtmlNodeContent(one.find('.//span'), 'TEXT').split('\xc2\xa0')[-1], '%Y-%m-%d')
                elif '更新' in prompt:
                    uptime = datetime.strptime('20%s' % request.getHtmlNodeContent(one.find('.//span'), 'TEXT').split('\xc2\xa0')[-1], '%Y-%m-%d')
        except:
            pass

        data = Data(food_id=food_id, name=name, desc=desc, tel=tel, pic=pic, province_id=province_id,
            city_id=city_id, tag=tag, area_id=area_id, town_id=town_id, country_id=country_id, address=address,
            longitude=longitude, latitude=latitude, dianping=dianping, src=src, link_url=link_url,
            atime=atime, time=time, uptime=uptime, tid=self.tid)
        yield data

    @next(fetchShopDetail)
    @timelimit(20)
    def fetchShopList(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        headers = {
            "User-Agent":"iPhone; CPU iPhone OS 9_1 like Mac OS X AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
        }
        result = request.get(url, headers=headers, timeout=timeout, format='JSON')
        shops = result['msg']['shops']
        for one in shops:
            additions = {}
            additions['name'] = one['shopName'] + one['branchName']
            additions['address'] = one['address']
            additions['tel'] = one['contactPhone']
            additions['longitude'] = one['glng']
            additions['latitude'] = one['glat']
            additions['desc'] = one['businessHours'] + ',' + one['crossRoad']
            additions['average'] = one['avgPrice']
            yield {'url':'http://www.dianping.com/shop/%s' % str(one['shopId']), 'additions':additions}


    @next(fetchShopList)
    @index('url')
    @timelimit(20)
    def fetchTuanFoodList(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        headers = {
            "User-Agent":"iPhone; CPU iPhone OS 9_1 like Mac OS X AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
        }
        result = request.get(url, headers=headers, timeout=timeout, format='HTML')
        foods = result.findall('.//ul[@class="tg-floor-list Fix tg-floor-list-freak"]//a[@class="tg-floor-img"]')
        if len(foods) < 40:
            nextpage = None
        else:
            index = url.split('=')
            index[-1] = str(int(index[-1]) + 1)
            nextpage = '-'.join(index)
        yield nextpage
        for one in foods:
            detail = request.get('http://t.dianping.com%s' % request.getHtmlNodeContent(one, {'ATTR':'href'}), headers=headers, timeout=timeout, format='HTML')
            pic = []
            try:
                for pic_one in detail.findall('.//div[@class="detail"]'):
                    if request.getHtmlNodeContent(pic_one.find('.//span[@class="name"]'), 'TEXT') == '商户介绍':
                        pic.extend([request.getHtmlNodeContent(img, {'ATTR':'lazy-src-load'}) for img in pic_one.findall('.//img')])
                        break
            except:
                pass
            additions['pic'] = pic
            gid = request.getHtmlNodeContent(one, {'ATTR':'href'}).split('/')[-1]
            url = 'http://t.dianping.com/ajax/dealGroupShopDetail?dealGroupId=%s&action=shops' % gid
            yield {'url': url, 'additions':additions}


    @next(fetchTuanFoodList)
    @timelimit(20)
    @initflow('tuan')
    def fetchTuanFood(self, additions={}, timeout=TIMEOUT, implementor=None):
        for one in food.find({"province_id" : "110000"}, {"name":1, "area_id":1, "city_id":1, "country_id":1, "province_id":1, "town_id":1}):
            yield {'url': 'http://t.dianping.com/list/beijing?q=%s&pageIndex=0' % one['name'], 
            'additions':{'food_id':str(one['_id']),
                'country_id':one['country_id'],
                'province_id':one['province_id'],
                'city_id':one['city_id'],
                'town_id':one['town_id'],
                'area_id':one['area_id'],
            }}


    @next(fetchShopList)
    @index('url')
    @timelimit(20)
    def fetchWWWFoodList(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        }
        result = request.get(url, headers=headers, timeout=timeout, format='HTML')
        foods = result.findall('.//div[@id="shop-all-list"]//ul//li')
        print len(foods)
        if len(foods) < 15:
            nextpage = None
        else:
            index = url.split('/')
            index[-1] = str(int(index[-1]) + 1)
            nextpage = '/'.join(index)
        yield nextpage
        for one in foods:
            groupbuy = request.getHtmlNodeContent(one.find('.//div[@class="svr-info"]//a'), {'ATTR':'href'})
            detail = request.get(groupbuy, headers=headers, timeout=timeout, format='HTML')
            pic = []
            try:
                for pic_one in detail.findall('.//div[@class="detail"]'):
                    if request.getHtmlNodeContent(pic_one.find('.//span[@class="name"]'), 'TEXT') == '商户介绍':
                        pic.extend([request.getHtmlNodeContent(img, {'ATTR':'lazy-src-load'}) for img in pic_one.findall('.//img')])
                        break
            except:
                pass
            additions['pic'] = pic
            gid = groupbuy.split('/')[-1]
            url = 'http://t.dianping.com/ajax/dealGroupShopDetail?dealGroupId=%s&action=shops' % gid
            yield {'url': url, 'additions':additions}


    @next(fetchWWWFoodList)
    @timelimit(20)
    @initflow('www')
    def fetchWWWFood(self, additions={}, timeout=TIMEOUT, implementor=None):
        for one in food.find({"province_id" : "110000"}, {"name":1, "area_id":1, "city_id":1, "country_id":1, "province_id":1, "town_id":1}):
            yield {'url': 'http://www.dianping.com/search/keyword/2/0_%s/p1' % one['name'], 
            'additions':{'food_id':str(one['_id']),
                'country_id':one['country_id'],
                'province_id':one['province_id'],
                'city_id':one['city_id'],
                'town_id':one['town_id'],
                'area_id':one['area_id'],
            }}

if __name__ == '__main__':

    print 'start'
    spider = SpiderDianping(worknum=6, queuetype='P', worktype='COROUTINE')
    spider.fetchDatas('www')
    print 'end'
