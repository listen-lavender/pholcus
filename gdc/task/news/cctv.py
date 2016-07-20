#!/usr/bin/env python
# coding=utf-8

from datetime import *
from webcrawl.character import *
from webcrawl.task import *
from newsspider import *
from webcrawl import request

#_print, logger = logprint(modulename(__file__), modulepath(__file__))

class SpiderCCTV(SpiderNewsOrigin):

    """
       cctv 数据爬虫
    """

    def __init__(self, worknum=6, queuetype='Local', timeout=-1, tid=0, settings={}):
        super(SpiderCCTV, self).__init__(worknum=worknum, queuetype=queuetype, timeout=timeout, tid=tid, settings=settings)
        self.clsname = self.__class__.__name__
        self.tid = tid

    @store(withData(datacfg.W), Data.insert, update=True, method='MANY')
    @timelimit(20)
    @initflow('www')
    def fetchList(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        result = request.get(url, timeout=timeout, format='HTML')
        news = result.findall('.//dl[@id="idcur"]//dd')
        news.append(result.find('.//dl[@id="idcur"]//dt'))
        for one in news:
            name = request.getHtmlNodeContent(one.find('.//p'), 'TEXT')
            icon = request.getHtmlNodeContent(one.find('.//img'), {'ATTR':'src'})
            detail_link = request.getHtmlNodeContent(one.find('.//a'), {'ATTR':'href'})
            detail = request.get(detail_link, timeout=timeout, format='HTML')
            desc = ''
            src = 'cctv'
            category = '足球'
            atime = request.getHtmlNodeContent(detail.find('.//div[@class="font_xx"]'), 'TEXT').strip()
            atime = ('20%s' % atime.replace('日 ', 'T').split(' 20')[-1]).replace('年', '-').replace('月', '-')
            atime = datetime.strptime(atime, '%Y-%m-%dT%H:%M')
            create_time = datetime.now()
            update_time = datetime.now()
            data = {"name":name,
                "icon":icon,
                "detail_link":detail_link,
                "desc":desc,
                "src":src,
                "category":category,
                'group':'pic',
                'content':'',
                "atime":atime,
                "create_time":create_time,
                "update_time":update_time,
                'tid':self.tid}
            yield Data(**data)
        news = result.findall('.//ul[@class="il_w120_b1"]//li')
        for one in news:
            name = request.getHtmlNodeContent(one.find('.//div[@class="text"]//a'), 'TEXT').replace('[高清组图]', '')
            icon = request.getHtmlNodeContent(one.find('.//div[@class="image"]//img'), {'ATTR':'src'})
            detail_link = request.getHtmlNodeContent(one.find('.//div[@class="image"]//a'), {'ATTR':'href'})
            detail = request.get(detail_link, timeout=timeout, format='HTML')
            desc = ''
            src = 'cctv'
            category = '足球'
            atime = request.getHtmlNodeContent(detail.find('.//div[@class="font_xx"]'), 'TEXT').strip()
            atime = ('20%s' % atime.replace('日 ', 'T').split(' 20')[-1]).replace('年', '-').replace('月', '-')
            atime = datetime.strptime(atime, '%Y-%m-%dT%H:%M')
            create_time = datetime.now()
            update_time = datetime.now()
            data = {"name":name,
                "icon":icon,
                "detail_link":detail_link,
                "desc":desc,
                "src":src,
                "category":category,
                'group':'pic',
                'content':'',
                "atime":atime,
                "create_time":create_time,
                "update_time":update_time,
                'tid':self.tid}
            yield Data(**data)
        news = result.findall('.//div[@class="text_list"]//ul//li')
        for one in news:
            name = request.getHtmlNodeContent(one.find('.//a'), 'TEXT')
            detail_link = request.getHtmlNodeContent(one.find('.//a'), {'ATTR':'href'})
            detail = request.get(detail_link, timeout=timeout, format='HTML')
            icon = request.getHtmlNodeContent(detail.find('.//p[@align="center"]//img'), {'ATTR':'src'})
            desc = ''
            src = 'cctv'
            category = '足球'
            atime = request.getHtmlNodeContent(detail.find('.//div[@class="function"]//span[@class="info"]//i'), 'TEXT').strip()
            atime = ('20%s' % atime.replace('日 ', 'T').split(' 20')[-1]).replace('年', '-').replace('月', '-')
            atime = datetime.strptime(atime, '%Y-%m-%dT%H:%M')
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
