#!/usr/bin/env python
# coding=utf-8

from datetime import *
from webcrawl.character import *
from webcrawl.task import *
from webcrawl.urlkit import URLParse
from newsspider import *
from webcrawl import request

#_print, logger = logprint(modulename(__file__), modulepath(__file__))

class SpiderYidian(SpiderNewsOrigin):

    """
       一点资讯 数据爬虫
    """

    def __init__(self, worknum=6, queuetype='P', worktype='COROUTINE', timeout=-1, tid=0, settings={}, callback=None):
        super(SpiderYidian, self).__init__(worknum=worknum, queuetype=queuetype, worktype=worktype, timeout=timeout, tid=tid, settings=settings, callback=callback)
        self.clsname = self.__class__.__name__
        self.tid = tid

    @store(withData(datacfg.W), Data.insert, update=True, method='MANY')
    @index('url')
    @timelimit(20)
    @initflow('www')
    def fetchList(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        result = request.get(url, timeout=timeout, format='JSON')
        news = result['result']
        if len(news) == 0:
            nextpage = None
        else:
            urlobj, params = URLParse.decode(url)

            span = int(params['cend']) - int(params['cstart'])
            params['cstart'] = params['cend']
            params['cend'] = str(int(params['cstart']) + span)
            
            nextpage = URLParse.encode(urlobj, params)
        yield nextpage
        for one in news:
            if not one['ctype'] == "news":
                continue
            name = one['title']
            if 'icon' in one:
                icon = one['icon']
            elif 'image_urls' in one and one['image_urls']:
                icon = 'http://i1.go2yd.com/image.php?url=%s&type=thumbnail_200x140' % one['image_urls'][0]
            else:
                icon = ''
            detail_link = one['url']
            desc = one['summary']
            src = '一点资讯'
            category = one['category']
            atime = datetime.strptime(one['date'], '%Y-%m-%d %H:%M:%S')
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
