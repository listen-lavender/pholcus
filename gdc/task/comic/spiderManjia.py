#!/usr/bin/env python
# coding=utf-8
import os, re, copy, json, time
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
from comicspider import Data
from comicspider import TIMEOUT
from comicspider import SpiderComicOrigin

#_print, logger = logprint(modulename(__file__), modulepath(__file__))

dmzj_re = re.compile('initIntroData\(\[.*\]\);')

class SpiderDmzj(SpiderComicOrigin):

    """
       哔哩官网 数据爬虫
    """

    def __init__(self, worknum=6, queuetype='P', worktype='COROUTINE', timeout=-1, tid=0):
        super(SpiderDmzj, self).__init__(worknum=worknum, queuetype=queuetype, worktype=worktype, timeout=timeout, tid=tid)
        self.clsname = self.__class__.__name__
        self.headers = {}
        self.end = datetime.now()
        self.begin = self.end - timedelta(days=7)

    @store(withData(datacfg.W), Data.insert, update=True, method='MANY')
    @timelimit(3)
    def fetchDetail(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        cat = additions['cat']
        tag = additions['tag']
        name = additions['name']
        desc = additions['desc']
        cover = additions['cover']
        author = additions['author']
        atime = additions['atime']
        owner = {}
        snum = 0
        src = '漫画之家'
        host = 'www.dmzj.com'

        wap_result = get(url, timeout=TIMEOUT, format='HTML')
        page_url = url
        url = ''
        format = 'h5'
        page_id = hash(page_url)
        parent_page_id = hash(page_url)

        owner['name'] = getHtmlNodeContent(wap_result.find('.//a[@class="pd introName"]'), 'TEXT')
        owner['url'] = 'http://m.dmzj.com%s' % getHtmlNodeContent(wap_result.find('.//a[@class="pd introName"]'), {'ATTR':'href'})

        pages = ''.join(getHtmlNodeContent(one, 'TEXT') for one in wap_result.findall('.//script'))
        try:
            pages = json.loads(dmzj_re.search(pages).group().replace("initIntroData([", "").replace("]);", "")).get('data', [])
            pages = sorted(pages, key=lambda v:v['chapter_order'])
        except:
            pages = []

        for index, chapter in enumerate(pages):
            url = 'http://m.dmzj.com/view/%s/%s.html' % (chapter['comic_id'], chapter['id'])
            page_url = url
            page_id = hash(page_url)
            snum = index + 1
            page_data = Data(cat=cat, url=url, tag=tag, name=name,
                desc=desc, cover=cover, author=author,
                owner=owner, snum=snum,
                src=src, host=host, page_url=page_url,
                page_id=page_id, parent_page_id=parent_page_id,
                atime=atime, tid=self.tid)
            yield page_data

    @next(fetchDetail)
    @timelimit(20)
    @index('url')
    def fetchList(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        result = get(url, timeout=timeout, format='JSON')
        if len(result) < 15:
            nextpage = None
        else:
            index = url.split('-')
            sub_index = index[-1].split('.')
            sub_index[0] = int(sub_index[0]) + 1
            # if sub_index[0] >5:
            #     nextpage = None
            # else:
            #     sub_index[0] = str(sub_index[0])
            #     index[-1] = '.'.join(sub_index)
            #     nextpage = '-'.join(index)
            sub_index[0] = str(sub_index[0])
            index[-1] = '.'.join(sub_index)
            nextpage = '-'.join(index)
        yield nextpage
        for one in result:
            additions = {
                'cat':additions['cat'],
                'name':one['name'],
                'tag':one['types'].split('/'),
                'desc':one['description'] or one['introduction'],
                'author':one['authors'],
                'cover':'http://images.dmzj.com/%s' % one['cover'],
                'atime':time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(one['last_updatetime']))
            }
            tags = one['types'].split('/')
            yield {'url': 'http://m.dmzj.com/info/%s.html' % str(one['id']), 'additions':additions}

    @next(fetchList)
    @timelimit(20)
    @initflow('www')
    def fetchCat(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        result = get(url, timeout=timeout, format='HTML')
        print len(result.findall('.//div[@id="classCon"]//ul'))
        result = result.find('.//div[@id="classCon"]//ul')
        for cat in result.findall('.//a'):
            cid = getHtmlNodeContent(cat, {'ATTR':'onclick'}).replace('itemClickAction(0,', '').replace(')', '').replace(' ', '')
            if int(cid) > 0:
                yield {'url':'http://m.dmzj.com/classify/%s-0-0-0-0-0.json' % cid, 'additions':{'cat':['漫画', getHtmlNodeContent(cat, 'TEXT')]}}

    @next(fetchDetail)
    @timelimit(20)
    @initflow('spec')
    def fetchSpec(self, additions={}, timeout=TIMEOUT, implementor=None):
        yield {'url': 'http://m.dmzj.com/info/2125.html', 'additions': {'cat':['漫画', '青春', '校园'], 'name':'妄想学生会', 'tag':['欢乐向', '校园', '节操', '搞笑'], 'desc':'动漫之家手机漫画提供妄想学生会359在线漫画，是国内妄想学生会漫画最全更新最快的手机漫画网。妄想学生会漫画介绍：创校已有50年，原本是女校的私立樱才学园，因受到少子化的影响，于今年起变更为男女合校。因为是第一年，男生人数还相当稀少，全校男女生的比率为女生524人，男生28人。对男生来说，正常应该像是后宫一般(？)………但是！以主角津田隆利的立场来看，恐怕完全没这...', 'author':'氏家卜全', 'cover':'http://images.dmzj.com/webpic/7/1204wangxiangxueshenghuifml.jpg', 'atime':datetime.now()}}

if __name__ == '__main__':

    print 'start'
    spider = SpiderDmzj(worknum=6, queuetype='P', worktype='COROUTINE')
    spider.fetchDatas('www', 0, 'http://m.dmzj.com/classify.html')
    spider.statistic()
    print 'end'
