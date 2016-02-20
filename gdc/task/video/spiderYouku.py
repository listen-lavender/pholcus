#!/usr/bin/python
# coding=utf-8
import os, re, copy
from pymongo import MongoClient
from datetime import timedelta
from datetime import datetime
from webcrawl.handleRequest import requGet
from webcrawl.handleRequest import requPost
from webcrawl.handleRequest import getHtmlNodeContent
from webcrawl.handleRequest import getXmlNodeContent
from webcrawl.work import retry
from webcrawl.work import index
from webcrawl.work import initflow
from webcrawl.handleRequest import getJsonNodeContent
from webcrawl.work import store
from webcrawl.work import timelimit
from webcrawl.work import next
from webcrawl.handleRequest import ensureurl
from webcrawl.handleRequest import parturl
from videospider import Data
from videospider import TIMEOUT
from videospider import withData
from videospider import DBCONN, RDB, WDB, initDB
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

class SpiderYouku(SpiderVideoOrigin):

    """
       优酷官网 数据爬虫
    """

    def __init__(self, worknum=6, queuetype='P', worktype='COROUTINE', timeout=-1, tid=0):
        super(SpiderYouku, self).__init__(worknum=worknum, queuetype=queuetype, worktype=worktype, timeout=timeout)
        self.tid = tid
        self.clsname = self.__class__.__name__
        initDB()
        self.end = datetime.now()
        self.begin = self.end - timedelta(days=7)

    @store(withData(WDB, conn), Data.insert, update=True, method='MANY')
    @timelimit(3)
    @index('url')
    def fetchDetail(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        cat = additions['cat']

        try:
            page_result = requGet(url, timeout=TIMEOUT, format='HTML')
            pages = page_result.findall('.//div[@class="item"]')
            if len(pages) < 20:
                nextpage = None
            else:
                index = url.split('_')
                index[-1] = str(int(index[-1]) + 20)
                nextpage = '_'.join(index)
            yield nextpage

            parent_page_id = additions.get('parent_page_id')
            if additions.get('parent_page_id') is None:
                parent_page_url = getHtmlNodeContent(pages[0].find('.//div[@class="link"]//a'), {'ATTR':'href'}).split('?')[0]
                parent_page_id = hash(parent_page_url)
                additions['parent_page_id'] = parent_page_id

            base = int(url.split('_')[-1])

            for index, one in enumerate(pages):
                page_url = getHtmlNodeContent(one.find('.//div[@class="link"]//a'), {'ATTR':'href'}).split('?')[0]
                url = ''
                format = 'mp4'
                size = 0
                try:
                    during = seconds(getHtmlNodeContent(one.find('.//div[@class="time"]//span[@class="num"]'), 'TEXT').split(":"))
                except:
                    during = 0
                tag = []
                name = getHtmlNodeContent(one.find('.//div[@class="link"]//a'), {'ATTR':'title'})
                desc = getHtmlNodeContent(one.find('.//div[@class="desc"]'), 'TEXT')
                cover = getHtmlNodeContent(one.find('.//div[@class="thumb"]//img'), {'ATTR':'alt'})
                author = ''
                owner = {'avatar':'', 'name':'', 'url':''}
                snum = base + index
                src = '优酷'
                host = 'www.youku.com'
                page_id = hash(page_url)
                atime = datetime.now()

                data = Data(cat=cat, url=url, format=format,
                    size=size, during=during, tag=tag, name=name,
                    desc=desc, cover=cover, author=author,
                    owner=owner, snum=snum,
                    src=src, host=host, page_url=page_url,
                    page_id=page_id, parent_page_id=parent_page_id,
                    atime=atime, tid=self.tid)

                yield data
        except:
            page_result = requGet(url, timeout=TIMEOUT, format='JSON')
            pages = page_result['showlistnew']['items']

            yield None

            parent_page_url = 'http://v.youku.com/v_show/id_%s.html' % pages[0]['videoid']
            parent_page_id = hash(parent_page_url)

            for index, one in enumerate(pages):
                page_url = 'http://v.youku.com/v_show/id_%s.html' % one['videoid']
                url = ''
                format = 'mp4'
                size = 0
                during = int(float(one['seconds']))
                tag = []
                name = one['title']
                desc = ''
                cover = one['thumburl']
                author = ''
                owner = {'avatar':'', 'name':'', 'url':''}
                snum = index + 1
                src = '优酷'
                host = 'www.youku.com'
                page_id = hash(page_url)
                atime = datetime.now()

                data = Data(cat=cat, url=url, format=format,
                    size=size, during=during, tag=tag, name=name,
                    desc=desc, cover=cover, author=author,
                    owner=owner, snum=snum,
                    src=src, host=host, page_url=page_url,
                    page_id=page_id, parent_page_id=parent_page_id,
                    atime=atime, tid=self.tid)

                yield data


    @next(fetchDetail)
    @timelimit(20)
    @index('url')
    def fetchList(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        result = requGet(url, timeout=timeout, format='HTML')
        videos = result.findall('.//div[@class="yk-row yk-v-80"]//div[@class="yk-col3"]')
        if len(videos) < 42:
            nextpage = None
        else:
            index = url.split('_')
            sub_index = index[-1].split('.')
            sub_index[0] = int(sub_index[0]) + 1
            if sub_index[0] >5:
                nextpage = None
            else:
                sub_index[0] = str(sub_index[0])
                index[-1] = '.'.join(sub_index)
                nextpage = '_'.join(index)
            # sub_index[0] = str(sub_index[0])
            # index[-1] = '.'.join(sub_index)
            # nextpage = '_'.join(index)
        yield nextpage
        for one in videos:
            vid = getHtmlNodeContent(one.find('.//div[@class="p-meta-title"]//a'), {'ATTR':'href'})
            vid = vid[vid.rindex('/')+1:vid.rindex('.')]
            yield {'url': 'http://www.youku.com/show_point/%s.html?dt=json&tab=0&divid=point_reload_1' % vid, 'additions': {'cat':additions['cat']+[getHtmlNodeContent(one.find('.//div[@class="p-meta-title"]//a'), 'TEXT')]}}

    @next(fetchList)
    @timelimit(20)
    @initflow('www')
    def fetchCat(self, additions={}, timeout=TIMEOUT, implementor=None):
        cats = ['热血', '格斗', '恋爱', '美少女', '校园', '搞笑', 'LOLI', '神魔', '机战', '科幻', '真人', '青春', '魔法', '神话', '冒险', '运动', '竞技', '童话', '亲子', '教育', '励志', '剧情', '社会', '历史', '战争']
        for cat in cats:
            url = 'http://www.youku.com/v_olist/c_100_g_%s_a__sg__mt__lg__q__s_1_r_0_u_0_pt_1_av_0_ag_0_sg__pr__h__d_1_p_1.html' % cat
            yield {'url':url, 'additions':{'cat':['动漫', cat]}}

    
    @next(fetchDetail)
    @timelimit(20)
    @initflow('spec')
    def fetchSpec(self, additions={}, timeout=TIMEOUT, implementor=None):
        albums = [
        'http://v.youku.com/x_getAjaxData?md=showlistnew&vid=107240046',
        'http://v.youku.com/x_getAjaxData?md=showlistnew&vid=107121098',
        'http://v.youku.com/x_getAjaxData?md=showlistnew&vid=338000877',
        ]
        for index, one in enumerate(albums):
            yield {'url': one, 'additions': {'cat':['漫画', '美少女', '摇曳百合第%d季' % (index+1)]}}


if __name__ == '__main__':

    print 'start'
    spider = SpiderYouku(worknum=6, queuetype='P', worktype='COROUTINE')
    spider.fetchDatas('www')
    spider.statistic()
    print 'end'
