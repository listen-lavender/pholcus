#!/usr/bin/env python
# coding=utf-8
import datetime
from bson import ObjectId
from webcrawl.task import *
from picspider import *
from webcrawl import request
from webcrawl.request import FILE

# FILE.dir = '/Users/uni/Desktop/img/pic/'
FILE.dir = '/home/yada/img/pic/'

class SpiderGiphy(SpiderPicOrigin):

    """
       giphy图片 数据爬虫
    """

    def __init__(self, worknum=6, queuetype='Local', timeout=-1, tid=0):
        super(SpiderGiphy, self).__init__(worknum=worknum, queuetype=queuetype, timeout=timeout, tid=tid)
        self.clsname = self.__class__.__name__
        self.tid = tid

    @store(withData(datacfg.W), Data.insert, update=True, method='MANY')
    @timelimit(20)
    @index('url')
    @initflow('www')
    def fetchList(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        result = request.get(url, timeout=timeout, format='HTML')
        images = result.findall('.//a[@class="gif-link"]//img')
        nextpage = request.getHtmlNodeContent(result.find('.//a[@id="next-page-arrow"]'), {'ATTR':'href'})
        if nextpage:
            nextpage = 'http://giphy.com%s' % nextpage
        else:
            nextpage = None
        nextpage = None
        yield nextpage

        for one in images:
            _id = ObjectId()
            url = request.getHtmlNodeContent(one, {'ATTR':'src'})
            tag = request.getHtmlNodeContent(one, {'ATTR':'alt'}).split(' ')
            src = 'giphy'
            outid = url
            atime = datetime.datetime.now()
            download = False
            request.get(url, timeout=timeout, format='PLAIN', filepath='%s/%s' % (src, str(_id)))
            download = True
            yield Data(_id=_id, url=url, tag=tag, src=src, outid=outid, atime=atime, download=download, tid=self.tid)
