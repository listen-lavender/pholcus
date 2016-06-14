#!/usr/bin/env python
# coding=utf-8

from datetime import *
from webcrawl.character import *
from webcrawl.task import *
from newsspider import *
from webcrawl import request

#_print, logger = logprint(modulename(__file__), modulepath(__file__))

class Spider163(SpiderNewsOrigin):

    """
       网易新闻 数据爬虫
    """

    def __init__(self, worknum=6, queuetype='P', worktype='COROUTINE', timeout=-1, tid=0, settings={}, callback=None):
        super(Spider163, self).__init__(worknum=worknum, queuetype=queuetype, worktype=worktype, timeout=timeout, tid=tid, settings=settings, callback=callback)
        self.clsname = self.__class__.__name__
        self.tid = tid

    @store(withData(datacfg.W), Data.insert, update=True, method='MANY')
    @index('url')
    @timelimit(20)
    @initflow('www')
    def fetchList(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        result = request.get(url, timeout=timeout, dirtys=[('artiList({', '{'), ('})', '}')], format='JSON')
        news = result['BA8E6OEOwangning']
        start, end = url[url.rindex('/')+1:url.rindex('.')].split('-')

        span = int(end) - int(start)
        if len(news) < span:
            nextpage = None
        else:
            start = end
            end = str(int(start) + span)
            nextpage = '%s/%s-%s.html' % (url[:url.rindex('/')], start, end)
        yield nextpage

        for one in news:
            if '|' in url:
                continue
            name = one['title']
            icon = one['imgsrc']
            detail_link = 'http://3g.163.com/touch/article.html?channel=sports&docid=%s' % one['docid']
            desc = one['digest']
            src = '网易新闻'
            category = additions.get('category')
            atime = datetime.strptime(one['ptime'], '%Y-%m-%d %H:%M:%S')
            create_time = datetime.now()
            update_time = datetime.now()
            data = {"name":name,
                "icon":icon,
                "detail_link":detail_link,
                "desc":desc,
                "src":src,
                "category":category,
                'group':'text',
                'content':'',
                "atime":atime,
                "create_time":create_time,
                "update_time":update_time,
                'tid':self.tid}
            yield Data(**data)


if __name__ == '__main__':
    pass
