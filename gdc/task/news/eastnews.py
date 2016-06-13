#!/usr/bin/env python
# coding=utf-8

from datetime import *
from webcrawl.character import *
from webcrawl.task import *
from newsspider import *
from webcrawl import request
from lxml import etree

#_print, logger = logprint(modulename(__file__), modulepath(__file__))

class SpiderEastnews(SpiderNewsOrigin):

    """
       东方网头条新闻池 数据爬虫
    """

    def __init__(self, worknum=6, queuetype='P', worktype='COROUTINE', timeout=-1, tid=0, settings={}, callback=None):
        super(SpiderEastnews, self).__init__(worknum=worknum, queuetype=queuetype, worktype=worktype, timeout=timeout, tid=tid, settings=settings, callback=callback)
        self.clsname = self.__class__.__name__
        self.tid = tid

    @store(withData(datacfg.W), Data.insert, update=True, method='MANY')
    @timelimit(20)
    @initflow('www')
    def fetchList(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        result = request.get(url, timeout=timeout, format='HTML')
        news = result.findall('.//div[@class="news_nr"]//li')
        news = zip(*[iter(news)]*5)
        for one in news:
            category, name, detail_link, _, icon = one
            name = request.getHtmlNodeContent(name.find('.//div'), 'TEXT')
            icon = request.getHtmlNodeContent(icon.find('.//div'), 'TEXT').replace('"', '')
            detail_link = request.getHtmlNodeContent(detail_link.find('.//div'), 'TEXT').replace('"', '')
            detail = request.get(detail_link, timeout=timeout, format='HTML')
            desc = ''
            src = '东方网'
            category = request.getHtmlNodeContent(category, 'TEXT')
            atime = request.getHtmlNodeContent(detail.find('.//div[@id="title"]//span[@class="src"]'), 'TEXT').split(u'\u2003')[-1]
            atime = datetime.strptime(atime, '%Y-%m-%d %H:%M')
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
    pass
