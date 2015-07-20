#!/usr/bin/python
# coding=utf-8

LIMIT = 20
USE = 'local'
WDB = 'local'
RDB = 'local'
_DBCONN = {"113":{"host": "58.83.130.113",
                "port": 3306,
                "user": "query",
                "passwd": "queryonly",
                "db": "hotel20",
                "charset": "utf8",
                "use_unicode":False,},
            "112":{"host": "58.83.130.112",
                "port": 3306,
                "user": "hotel2",
                "passwd": "hotel0115",
                "db": "hotel20",
                "charset": "utf8",
                "use_unicode":False,},
            "111":{"host": "58.83.130.111",
                "port": 3306,
                "user": "innmall",
                "passwd": "innmall0930",
                "db": "innmall",
                "charset": "utf8",
                "use_unicode":False,},
            "local":{"host": "127.0.0.1",
                "port": 3306,
                "user": "root",
                "passwd": "",
                "db": "kuaijie",
                "charset": "utf8",
                "use_unicode":False,},
            }
