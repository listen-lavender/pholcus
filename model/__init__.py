#!/usr/bin/python
# coding=utf-8

# from base import *
# from log import *
# from data import *

def initDB():
    from settings import withBase, withData, base, data, _BASE_R, _BASE_W, _DATA_R, RDB, WDB, LIMIT
    base.addDB(RDB, LIMIT, host=_BASE_R['host'],
                        port=_BASE_R['port'],
                        user=_BASE_R['user'],
                        passwd=_BASE_R['passwd'],
                        db=_BASE_R['db'],
                        charset=_BASE_R['charset'],
                        use_unicode=_BASE_R['use_unicode'],
                        override=False)

    base.addDB(WDB, LIMIT, host=_BASE_W['host'],
                        port=_BASE_W['port'],
                        user=_BASE_W['user'],
                        passwd=_BASE_W['passwd'],
                        db=_BASE_W['db'],
                        charset=_BASE_W['charset'],
                        use_unicode=_BASE_W['use_unicode'],
                        override=False)

    data.addDB(RDB, LIMIT, host=_DATA_R['host'],
                        port=_DATA_R['port'],
                        user=_DATA_R['user'],
                        passwd=_DATA_R['passwd'],
                        db=_DATA_R['db'],
                        charset=_DATA_R['charset'],
                        use_unicode=_DATA_R['use_unicode'],
                        override=False)

initDB()