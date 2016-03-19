#!/usr/bin/env python
# coding=utf-8
import copy, time, json
from pymongo import MongoClient
from datetime import timedelta
from datetime import datetime
from webcrawl.request import requGet
from webcrawl.request import requPost
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
from audiospider import Data
from audiospider import TIMEOUT
from audiospider import withData, RDB, WDB
from audiospider import SpiderAudioOrigin

from task.util.wangyi import encrypt_163

#_print, logger = logprint(modulename(__file__), modulepath(__file__))

class Spider163(SpiderAudioOrigin):

    """
       网易云音乐官网 数据爬虫
    """

    def __init__(self, worknum=6, queuetype='P', worktype='COROUTINE', timeout=-1, tid=0):
        super(Spider163, self).__init__(worknum=worknum, queuetype=queuetype, worktype=worktype, timeout=timeout, tid=tid)
        self.clsname = self.__class__.__name__

    @store(withData(WDB), Data.insert, update=True, method='MANY')
    @timelimit(3)
    def fetchDetail(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        result = requGet(url, timeout=timeout, format='HTML')
        album_result = requGet(url, timeout=timeout, format='HTML')
        tag = [getHtmlNodeContent(one, 'TEXT') for one in album_result.findall('.//div[@class="tags f-cb"]//a')]
        pages = json.loads(getHtmlNodeContent(album_result.find('.//textarea[@style="display:none;"]'), 'TEXT') or '[]')
        cat = additions['cat']
        if pages:
            parent_page_id = hash('http://music.163.com/outchain/player?type=2&id=%s' % str(pages[0]['id']))
            for index, one in enumerate(pages):
                url_result = requPost('http://music.163.com/weapi/song/detail/', encrypt_163('{"id":"%s","ids":"[%s]","csrf_token":""}' % (str(one['id']), str(one['id']))), format='JSON')
                url = url_result['songs'][0]['mp3Url']
                format = 'mp3'
                size = 0
                during = one['duration']/1000.0
                
                name = one['name']
                desc = getHtmlNodeContent(album_result.find('.//p[@id="album-desc-more"]'), 'TEXT') if index == 0 else ''
                cover = one['album']['picUrl']
                snum = index + 1
                singer = one['artists'][0]['name']
                src = '网易'
                host = 'music.163.com'
                page_url = 'http://music.163.com/outchain/player?type=2&id=%s' % str(one['id'])
                page_id = hash(page_url)
                parent_page_id = parent_page_id
                atime = datetime.now()
                data = Data(cat=cat, url=url, format=format,
                    size=size, during=during, tag=tag, name=name,
                    desc=desc, cover=cover, snum=snum, singer=singer,
                    src=src, host=host, page_url=page_url,
                    page_id=page_id, parent_page_id=parent_page_id,
                    atime=atime, tid=self.tid)
                yield data

    @next(fetchDetail)
    @timelimit(20)
    @index('url')
    def fetchList(self, url, additions={}, timeout=TIMEOUT, implementor=None):
        result = requGet(url, timeout=timeout, format='HTML')
        audios = result.findall('.//ul[@id="m-pl-container"]//li')
        if len(audios) < additions['pagesize']:
            nextpage = None
        else:
            index = url.split('=')
            index[-1] = int(index[-1]) + 1
            if index[-1] > 5:
                nextpage = None
            else:
                index[-1] = str(index[-1])
                nextpage = '='.join(index)
        yield nextpage
        for one in audios:
            album_url = getHtmlNodeContent(audios[0].find('.//p[@class="dec"]//a'), {'ATTR':'href'})
            yield {'url': 'http://music.163.com/playlist?id=%s' % album_url.split('=')[-1], 'additions':{'cat':additions['cat']}}

    @next(fetchList)
    @initflow('www')
    @timelimit(20)
    def fetchCat(self, additions={}, timeout=TIMEOUT, implementor=None):
        cats = ['日本', '90后', '00后', '另类/独立']
        cats = ['华语', '欧美', '日语', '韩语', '粤语', '小语种', '风格', '流行', '摇滚', '民谣', '电子', '舞曲', '说唱', '轻音乐', '爵士', '乡村', 'R&B/Soul', '古典', '民族', '英伦', '金属', '朋克', '蓝调', '雷鬼', '世界音乐', '拉丁', '另类/独立', 'New Age', '古风', '后摇', 'Bossa Nova', '场景', '清晨', '夜晚', '学习', '工作', '午休', '下午茶', '地铁', '驾车', '运动', '旅行', '散步', '酒吧', '情感', '怀旧', '清新', '浪漫', '性感', '伤感', '治愈', '放松', '孤独', '感动', '兴奋', '快乐', '安静', '思念', '主题', '影视原声', 'ACG', '校园', '游戏', '70后', '80后', '90后', '网络歌曲', 'KTV', '经典', '翻唱', '吉他', '钢琴', '器乐', '儿童', '榜单', '00后']
        pagesize = 35
        for one in cats:
            yield {'url':'http://music.163.com/discover/playlist/?order=hot&cat=%s&limit=%d&offset=0' % (one, pagesize), 'additions':{'cat':[one,], 'pagesize':pagesize}}


if __name__ == '__main__':

    print 'start'
    spider = Spider163fou(worknum=6, queuetype='P', worktype='COROUTINE')
    spider.fetchDatas('www')
    spider.statistic()
    print 'end'