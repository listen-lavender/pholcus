#!/usr/bin/python
# coding=utf8

# cache timeout, 30 mins
CACHE_TIMEOUT = 60 * 30

# PERMANENT_SESSION_LIFETIME
PERMANENT_SESSION_LIFETIME = 60 * 60 * 15

# port
useport = 7001

# static files saving path
staticfilepath = "static/"
GITPKG = {}

"""
     缓存SQL配置
"""
MAXSIZE = 1000

"""
    数据库配置
"""
_DBCONN = {"localhost":{"host": "127.0.0.1",
                "port": 3306,
                "user": "root",
                "passwd": "",
                "db": "kuaijie",
                "charset": "utf8",
                "use_unicode":False,},
            }

_DBCONN_R = _DBCONN["localhost"]
_DBCONN_W = _DBCONN["localhost"]
LIMIT = 20