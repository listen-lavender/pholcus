#!/usr/bin/env python
# coding=utf-8

from datetime import *
from webcrawl.character import *
from webcrawl.task import *
from webcrawl.urlkit import URLParse
from newsspider import *
from webcrawl import request

#_print, logger = logprint(modulename(__file__), modulepath(__file__))

class SpiderToutiao(SpiderNewsOrigin):

    """
       今日头条 数据爬虫
    """

    def __init__(self, worknum=6, queuetype='P', worktype='COROUTINE', timeout=-1, tid=0, settings={}, callback=None):
        super(SpiderToutiao, self).__init__(worknum=worknum, queuetype=queuetype, worktype=worktype, timeout=timeout, tid=tid, settings=settings, callback=callback)
        self.clsname = self.__class__.__name__
        self.tid = tid

    @store(withData(datacfg.W), Data.insert, update=True, method='MANY')
    @index('url')
    @timelimit(20)
    @initflow('www')
    def fetchList(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        result = request.get(url, timeout=timeout, format='JSON')
        news = result['data']
        if not 'next' in result:
            nextpage = None
        else:
            urlobj, params = URLParse.decode(url)
            if str(params['max_behot_time']) == str(result['next']['max_behot_time']):
                nextpage = None
            else:
                params['max_behot_time'] = result['next']['max_behot_time']
                nextpage = URLParse.encode(urlobj, params)
        yield nextpage
        for one in news:
            name = one['title']
            if 'image_url' in one:
                icon = one['image_url']
            elif 'image_list' in one and one['image_list']:
                icon = one['image_list'][0]['url']
            else:
                icon = ''
            detail_link = one['display_url']
            desc = one['source'] + '，' + one['abstract']
            src = '今日头条'
            category = additions.get('category', '') # '财经'
            atime = datetime.strptime(one['datetime'], '%Y-%m-%d %H:%M')
            create_time = datetime.now()
            update_time = datetime.now()
            data = {"name":name,
                "icon":icon,
                "detail_link":detail_link,
                "desc":desc,
                "src":src,
                "category":category,
                "atime":atime,
                "create_time":create_time,
                "update_time":update_time,
                'tid':self.tid}
            yield Data(**data)


if __name__ == '__main__':
    import time
    spider = SpiderToutiao(worknum=2, queuetype='P', worktype='THREAD')
    spider.fetchDatas('www', 0, datetime.datetime.now().strftime('%Y%m%d'), 'http://www.toutiao.com/api/article/recent/?source=2&count=2&category=news_finance&max_behot_time=%s&utm_source=toutiao&offset=0&max_create_time=1464674041&_=1464682558376' % str(int(time.time())))
