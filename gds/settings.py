#!/usr/bin/python
# coding=utf8

from dbskit.mysql import orm as mysql_orm
from dbskit.mongo import orm as mongo_orm
from dbskit.mysql.suit import withMysql, dbpc as ms_dbpc
from dbskit.mongo.suit import withMongo, dbpc as mg_dbpc

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
_DBCONN = {"mysql":{"host": "127.0.0.1",
                "port": 3306,
                "user": "root",
                "passwd": "",
                "db": "pholcus",
                "charset": "utf8",
                "use_unicode":False,},
            "mongo":{"host": "127.0.0.1",
                "port": 3306,
                "user": "root",
                "passwd": "",
                "db": "pholcus",
                "charset": "utf8",
                "use_unicode":False,},
            }

_BASE_R = _DBCONN["mysql"]
_BASE_W = _DBCONN["mysql"]
_DATA_R = _DBCONN["mongo"]
LIMIT = 20
orm = mysql_orm
withBase = withMysql
withData = withMongo
baseConn = ms_dbpc
dataConn = mg_dbpc