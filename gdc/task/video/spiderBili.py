#!/usr/bin/python
# coding=utf-8
import os, re, copy
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
from videospider import Data
from videospider import TIMEOUT
from videospider import SpiderVideoOrigin

try:
    # from adesk.db import mongo_v2
    # conn = mongo_v2.conn
    # conn = MongoClient(host='localhost', port=27019)
    conn = MongoClient('localhost')
except:
    conn = MongoClient('localhost')
#_print, logger = logprint(modulename(__file__), modulepath(__file__))

bili_re = re.compile('duration: *\'.*\'')

def seconds(tl):
    assert len(tl) < 3
    num = 0
    for index, one in enumerate(tl[::-1]):
        num += pow(60, index) * int(one)
    return num

class SpiderBilibili(SpiderVideoOrigin):

    """
       哔哩官网 数据爬虫
    """

    def __init__(self, worknum=6, queuetype='P', worktype='COROUTINE', timeout=-1, tid=0):
        super(SpiderBilibili, self).__init__(worknum=worknum, queuetype=queuetype, worktype=worktype, timeout=timeout, tid=tid)
        self.clsname = self.__class__.__name__
        self.headers = {"Accept":"application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Accept-Language":"en-US,en;q=0.8",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            "Host":"www.bilibili.com",
            "User-Agent":"Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.20 Mobile Safari/537.36",
            "X-Requested-With":"XMLHttpRequest"}
        self.end = datetime.now()
        self.begin = self.end - timedelta(days=7)

    @store(withData(datacfg.W), Data.insert, update=True, method='MANY')
    @timelimit(3)
    def fetchDetail(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        cat = additions['cat']

        if 'mobile' in url:
            outid = url[url.rindex('/')+1:url.rindex('.')].replace('av', '')
        else:
            outid = url.strip('/').split('/')[-1].replace('av', '')
            url = 'http://www.bilibili.com/mobile/video/av%s.html' % outid

        page_result = get('http://app.bilibili.com/bangumi/avseason/%s.ver' % outid, dirtys=[('seasonJsonCallback({', '{'), ('});', '}')], timeout=TIMEOUT, format='JSON')
        # if not page_result['code'] == '0':
        #     www_result = get(url[:url.rindex('.')].replace('/mobile', '') + '/', timeout=TIMEOUT, format='HTML')

        wap_result = get(url, timeout=TIMEOUT, format='HTML')
        headers = {"Accept":"application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Accept-Language":"en-US,en;q=0.8",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            "Host":"www.bilibili.com",
            "Referer":"http//www.bilibili.com/mobile/video/av%s.html?tg" % outid,
            "User-Agent":"Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.20 Mobile Safari/537.36",
            "X-Requested-With":"XMLHttpRequest"}
        data_result = get('http://www.bilibili.com/m/html5?aid=%s' % outid, headers=headers, timeout=TIMEOUT, format='JSON')
        
        page_url = url
        url = data_result.get('src')
        format = 'mp4'
        size = 0
        durtxt = ''.join(getHtmlNodeContent(one, 'TEXT') for one in wap_result.findall('.//script'))
        try:
            during = seconds(bili_re.search(durtxt).group().replace("duration:", "").replace(" ", "").replace("'", "").split(":"))
        except:
            during = 0
        tag = [getHtmlNodeContent(one, 'TEXT') for one in wap_result.findall('.//div[@class="tag-wrap"]//li')]
        name = additions['name']
        desc = getHtmlNodeContent(wap_result.find('.//meta[@name="description"]'), {'ATTR':'content'})
        cover = getHtmlNodeContent(wap_result.find('.//img[@id="share_pic"]'), {'ATTR':'src'}) or data_result.get('img')
        author = ''
        owner = {'avatar':'', 'name':'', 'url':''}
        owner['avatar'] = getHtmlNodeContent(wap_result.find('.//div[@class="up-pic"]//img'), {'ATTR':'src'})
        owner['name'] = getHtmlNodeContent(wap_result.find('.//div[@class="up-pic"]//img'), {'ATTR':'alt'})
        owner['url'] = getHtmlNodeContent(wap_result.find('.//a[@class="up-detail"]'), {'ATTR':'href'})
        snum = 0
        src = '哔哩哔哩'
        host = 'www.bilibili.com'
        # page_url = url
        page_id = hash(page_url)
        parent_page_id = None
        try:
            atime = datetime.strptime(getHtmlNodeContent(wap_result.find('.//span[@class="up-time"]'), 'TEXT'), '%Y-%m-%d %H:%M:%S')
        except:
            atime = datetime.now()

        data = Data(cat=cat, url=url, format=format,
            size=size, during=during, tag=tag, name=name,
            desc=desc, cover=cover, author=author,
            owner=owner, snum=snum,
            src=src, host=host, page_url=page_url,
            page_id=page_id, parent_page_id=parent_page_id,
            atime=atime, tid=self.tid)

        pages = wap_result.findall('.//div[@id="part_list"]//li')
        if pages:
            first = getHtmlNodeContent(pages[0], {'ATTR':'page'})
            parent_page_id = hash('http://www.bilibili.com/mobile/video/av%s.html#page=%s' % (outid, first))
            for one in pages:
                pagenum = getHtmlNodeContent(one, {'ATTR':'page'})
                data_result = get('http://www.bilibili.com/m/html5?aid=%s&page=%s' % (outid, pagenum), headers=headers, timeout=TIMEOUT, format='JSON')
                page_data = copy.deepcopy(data)
                page_data['name'] = getHtmlNodeContent(one.find('.//a'), 'TEXT')
                try:
                    page_data['url'] = data_result['src']
                except:
                    page_data['url'] = ''
                page_data['page_url'] = 'http://www.bilibili.com/mobile/video/av%s.html#page=%s' % (outid, pagenum)
                page_data['page_id'] = hash(page_data['page_url'])
                page_data['parent_page_id'] = parent_page_id
                page_data['snum'] = int(pagenum)
                page_data['cover'] = data_result.get('img')
                yield page_data
        elif page_result['code'] == 0:
            first = page_result['result']['episodes'][-1]['av_id']
            first = page_result['result']['episodes'][-1]['danmaku'] if first == outid else first
            parent_page_id = hash('http://www.bilibili.com/mobile/video/av%s.html' % first)
            for one in page_result['result']['episodes']:
                aid = one['danmaku'] if one['av_id'] == outid else one['av_id']
                data_result = get('http://www.bilibili.com/m/html5?aid=%s&page=%s' % (one['av_id'], one['page']), headers=headers, timeout=TIMEOUT, format='JSON')
                page_data = copy.deepcopy(data)
                try:
                    page_data['url'] = data_result['src']
                except:
                    page_data['url'] = ''
                page_data['page_url'] = 'http://www.bilibili.com/mobile/video/av%s.html#page=%s' % (one['av_id'], one['page'])
                page_data['page_id'] = hash('http://www.bilibili.com/mobile/video/av%s.html' % aid)
                page_data['parent_page_id'] = parent_page_id
                if page_data['page_id'] == page_data['parent_page_id']:
                    page_data['desc'] = page_result['result']['evaluate']
                else:
                    page_data['desc'] = ''
                try:
                    page_data['snum'] = int(one['index'])
                except:
                    page_data['snum'] = len(page_result['result']['episodes'])
                page_data['name'] = one.get('index_title') or additions.get('name')
                page_data['atime'] = datetime.strptime(one['update_time'][:one['update_time'].rindex('.')], '%Y-%m-%d %H:%M:%S')
                page_data['cover'] = one['cover']
                yield page_data
        else:
            yield data

    @next(fetchDetail)
    @timelimit(20)
    @index('url')
    def fetchList(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        result = get(url, headers=self.headers, timeout=timeout, format='HTML')
        videos = result.findall('.//a[@class="list-item"]')
        if len(videos) < 20:
            nextpage = None
        else:
            index = url.split('-')
            index[2] = int(index[2]) + 1
            if index[2] >5:
                nextpage = None
            else:
                index[2] = str(index[2])
                nextpage = '-'.join(index)
        yield nextpage
        for one in videos:
            url = 'http://www.bilibili.com%s' % getHtmlNodeContent(one, {'ATTR':'href'})
            name = getHtmlNodeContent(one.find('.//div[@class="title"]'), 'TEXT')
            yield {'url': url, 'additions': {'cat':additions['cat'], 'name':name}}

    @next(fetchList)
    @timelimit(20)
    @initflow('www')
    def fetchCat(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        result = get(url, headers=self.headers, timeout=timeout, format='JSON')
        for upcat in result['0']:
            for downcat in result[str(upcat['tid'])]:
                url = 'http://www.bilibili.com/mobile/list/default-%s-1-%s~%s.html' % (str(downcat['tid']), self.begin.strftime('%Y-%m-%d'), self.end.strftime('%Y-%m-%d'))
                cat = [upcat['typename'], downcat['typename']]
                yield {'url':url, 'additions':{'cat':cat}}

if __name__ == '__main__':

    print 'start'
    spider = SpiderBilibili(worknum=6, queuetype='P', worktype='THREAD')
    spider.fetchDatas('www', 0, 'http://www.bilibili.com/html/js/types.json')
    spider.statistic()
    print 'end'
