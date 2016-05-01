#!/usr/bin/env python
# coding=utf-8

from webcrawl.spider import SpiderOrigin
from model.data import Media as Data

TIMEOUT = 120

class SpiderMediaOrigin(SpiderOrigin):

    def __del__(self):
        pass

    def __init__(self, queuetype='P', timeout=-1, worknum=6, worktype='COROUTINE', tid=0):
        super(SpiderMediaOrigin, self).__init__(queuetype=queuetype, timeout=timeout, worknum=worknum, worktype=worktype, tid=tid)

if __name__ == "__main__":
    pass

