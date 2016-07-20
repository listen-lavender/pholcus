#!/usr/bin/env python
# coding=utf-8

from webcrawl.spider import SpiderOrigin
from model.data import Pic as Data
from model.setting import withData, datacfg

TIMEOUT = 120

class SpiderPicOrigin(SpiderOrigin):

    def __del__(self):
        pass

    def __init__(self, queuetype='P', timeout=-1, worknum=6, tid=0, settings={}):
        super(SpiderPicOrigin, self).__init__(queuetype=queuetype, timeout=timeout, worknum=worknum, tid=tid, settings=settings)

if __name__ == "__main__":
    pass
