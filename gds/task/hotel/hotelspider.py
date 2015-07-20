#!/usr/bin/python
# coding=utf-8

"""
   Basic spider of fetching hotel datas.
"""

import datetime, time

from task.config.web.hotel import CLSCON
from task.keep import Keeper
from webcrawl.spider import SpiderOrigin
from multilog.aboutfile import modulename, modulepath
from multilog.prettyprint import logprint
_print, logger = logprint(modulename(__file__), modulepath(__file__))

# class SpiderHotelOrigin(SpiderOrigin, Keeper):
class SpiderHotelOrigin(SpiderOrigin):
    """
        Basic spider of fetching hotel datas.
    """
    def __init__(self, worknum=30, queuetype='P', worktype='COROUTINE', timeout=-1):
        """
            初始化
        """
        # super(SpiderHotelOrigin, self).__init__(worknum=worknum, queuetype=queuetype, worktype=worktype, timeout=timeout)
        SpiderOrigin.__init__(self, worknum=worknum, queuetype=queuetype, worktype=worktype, timeout=timeout)
        # Keeper.__init__(self)
        SpiderHotelOrigin.uniquetime(lasttime=self.lasttime())
        self.clscon = CLSCON[self.__class__.__name__]
        self.useenv = CLSCON['useenv']
        self.predicttotal = self.clscon['predicttotal']

    def lasttime(self):
        return datetime.datetime.strptime('1949-10-01 00:00:00', '%Y-%m-%d %H:%M:%S')

    def __del__(self):
        pass

if __name__ == '__main__':
    print 'start...'
    print 'end...'
