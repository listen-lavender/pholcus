#!/usr/bin/env python
# coding=utf-8
from pymongo import MongoClient
from datetime import timedelta
from datetime import datetime
from webcrawl.request import get
from webcrawl.request import post
from webcrawl.request import getHtmlNodeContent
from webcrawl.request import getXmlNodeContent
from webcrawl.task import retry
from webcrawl.task import index
from webcrawl.task import initflow
from webcrawl.request import getJsonNodeContent
from webcrawl.task import store
from webcrawl.task import timelimit
from webcrawl.task import next
from webcrawl.request import ensureurl
from webcrawl.request import parturl
from model.setting import withData, datacfg
from proxyspider import Data
from proxyspider import TIMEOUT
from proxyspider import SpiderProxyOrigin

class SpiderXicidaili(SpiderProxyOrigin):

    """
       西刺网 数据爬虫
    """

    def __init__(self, worknum=30, queuetype='P', worktype='COROUTINE', timeout=-1, tid=0):
        super(SpiderXicidaili, self).__init__(worknum=worknum, queuetype=queuetype, worktype=worktype, timeout=timeout, tid=tid)
        self.dt = datetime.now()
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36'
        }

    @store(withData(datacfg.W), Data.insert, update=True, method='MANY')
    @timelimit(3)
    def fetchDetail(self, proxy, additions={}, timeout=TIMEOUT, implementor=None):
        ip, port, location, safetype, usetype, refspeed, status, update_time = proxy
        data = Data(ip=ip, port=port, location=location, safetype=safetype, usetype=usetype, refspeed=refspeed, usespeed=0, usenum=0, status=status, update_time=update_time, tid=self.tid)
        yield data

    @next(fetchDetail)
    @timelimit(3)
    @index('url')
    @initflow('www')
    def fetchList(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        result = get(url, headers=self.headers, timeout=timeout, format='HTML')
        proxys = result.findall('.//table[@id="ip_list"]//tr')
        if len(proxys) < 100:
            nextpage = None
        else:
            index = url.split('/')
            index[-1] = str(int(index[-1]) + 1)
            nextpage = '/'.join(index)
        # yield nextpage
        yield None
        for one in proxys:
            detail = one.findall('.//td')
            if len(detail) < 6:
                continue
            ip = getHtmlNodeContent(detail[2], 'TEXT')
            port = int(getHtmlNodeContent(detail[3], 'TEXT') or 0)
            location = getHtmlNodeContent(detail[4], 'TEXT')
            safetype = getHtmlNodeContent(detail[5], 'TEXT')
            usetype = getHtmlNodeContent(detail[6], 'TEXT')
            refspeed = float(getHtmlNodeContent(detail[7].find('.//div[@class="bar"]'), {'ATTR':'title'}).replace('秒', ''))
            status = 1
            update_time = datetime.strptime('20'+getHtmlNodeContent(detail[9], 'TEXT')+':00', '%Y-%m-%d %H:%M:%S')
            yield {'proxy':(ip, port, location, safetype, usetype, refspeed, status, update_time)}

if __name__ == '__main__':

    print 'start'
    spider = SpiderXici(worknum=6, queuetype='P', worktype='COROUTINE')
    spider.fetchDatas('www', 'http://www.xicidaili.com/nn/1')
    spider.statistic()
    print 'end'
