﻿#!/usr/bin/env python
# coding=utf-8

from webcrawl.spider import SpiderOrigin
from model.data import Proxy as Data

TIMEOUT = 120

class SpiderProxyOrigin(SpiderOrigin):

    def __del__(self):
        pass

    def __init__(self, queuetype='P', timeout=-1, worknum=6, worktype='COROUTINE', tid=0, settings={}, callback=None):
        super(SpiderProxyOrigin, self).__init__(queuetype=queuetype, timeout=timeout, worknum=worknum, worktype=worktype, tid=tid, settings=settings, callback=callback)

if __name__ == "__main__":
    pass

