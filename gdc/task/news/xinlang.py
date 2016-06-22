#!/usr/bin/env python
# coding=utf-8
import time
from datetime import *
from webcrawl.character import *
from webcrawl.task import *
from newsspider import *
from webcrawl import request

#_print, logger = logprint(modulename(__file__), modulepath(__file__))

class SpiderSina(SpiderNewsOrigin):

    """
       新浪网 数据爬虫
    """

    def __init__(self, worknum=6, queuetype='P', worktype='COROUTINE', timeout=-1, tid=0, settings={}, callback=None):
        super(SpiderSina, self).__init__(worknum=worknum, queuetype=queuetype, worktype=worktype, timeout=timeout, tid=tid, settings=settings, callback=callback)
        self.clsname = self.__class__.__name__
        self.tid = tid

    @store(withData(datacfg.W), Data.insert, update=True, method='MANY')
    @timelimit(20)
    @index('url')
    @initflow('www')
    def fetchList(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        result = request.get(url, timeout=timeout, format='JSON')
        news = result['result']['data']
        if len(news) < 30:
            nextpage = None
        else:
            index = url.split('=')
            index[-1] = str(int(index[-1]) + 1)
            nextpage = '='.join(index)
        nextpage = None
        yield nextpage
        for one in news:
            name = one['stitle']
            icon = one['img']['u']
            detail_link = one.get('wapurl') or one.get('url', '')
            desc = one['intro']
            src = '新浪新闻'
            category = '足球'
            group = 'text'
            if 'http://video.sina.com.cn' in detail_link:
                group = 'video'
            atime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(one['ctime'])))
            atime = datetime.strptime(atime, '%Y-%m-%d %H:%M:%S')
            create_time = datetime.now()
            update_time = datetime.now()
            data = {"name":name,
                "icon":icon,
                "detail_link":detail_link,
                "desc":desc,
                "src":src,
                "category":category,
                'group':group,
                'content':'',
                "atime":atime,
                "create_time":create_time,
                "update_time":update_time,
                'tid':self.tid}
            yield Data(**data)


if __name__ == '__main__':
    pass
