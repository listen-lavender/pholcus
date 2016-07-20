#!/usr/bin/env python
# coding=utf-8
import time
from datetime import *
from webcrawl.character import *
from webcrawl.task import *
from newsspider import *
from webcrawl import request

#_print, logger = logprint(modulename(__file__), modulepath(__file__))

class SpiderHupu(SpiderNewsOrigin):

    """
       新浪网 数据爬虫
    """

    def __init__(self, worknum=6, queuetype='Local', timeout=-1, tid=0, settings={}):
        super(SpiderHupu, self).__init__(worknum=worknum, queuetype=queuetype, timeout=timeout, tid=tid, settings=settings)
        self.clsname = self.__class__.__name__
        self.tid = tid

    @store(withData(datacfg.W), Data.insert, update=True, method='MANY')
    @timelimit(20)
    @index('url')
    @initflow('www')
    def fetchList(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        result = request.get(url, timeout=timeout, format='JSON')
        news = result['data']['data']
        if result['data']['is_more']:
            index = url.split('=')
            index[-1] = str(int(index[-1]) + 1)
            nextpage = '='.join(index)
        else:
            nextpage = None
        nextpage = None
        yield nextpage
        for one in news:
            name = one['title']
            icon = one['img_url']
            detail_link = one['link'].strip()
            desc = one['description']
            src = '虎扑新闻'
            category = '足球'
            group = 'text'
            detail = request.get(detail_link, timeout=timeout, format='HTML')
            atime = request.getHtmlNodeContent(detail.find('.//span[@class="stime"]'), 'TEXT').strip()
            if not atime:
                atime = request.getHtmlNodeContent(detail.find('.//span[@id="pubtime_baidu"]'), 'TEXT').strip()
            else:
                atime = '%s:00' % atime
            if not atime:
                continue
            else:
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
