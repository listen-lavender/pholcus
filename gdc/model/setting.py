#!/usr/bin/env python
# coding=utf8

from dbskit.mysql import orm as mysql_orm
from dbskit.mongo import orm as mongo_orm
from dbskit.mysql.suit import withMysql, dbpc as ms_dbpc
from dbskit.mongo.suit import withMongo, dbpc as mg_dbpc

RDB = 'localhost'
WDB = 'localhost'

"""
     缓存SQL配置
"""
MAXSIZE = 1000

"""
    数据库配置
"""
_DBCONN = {"mysql":{"host": "127.0.0.1",
                "port": 3307,
                "user": "root",
                "passwd": "",
                "db": "pholcus",
                "charset": "utf8",
                "use_unicode":False,},
            "mongo":{"host": "127.0.0.1",
                "port": 27018,
                "user": "root",
                "passwd": "",
                "db": "dandan-jiang",
                "charset": "utf8",
                "use_unicode":False,},
            }

_BASE_R = _DBCONN["mysql"]
_BASE_W = _DBCONN["mysql"]
_DATA_R = _DBCONN["mongo"]
LIMIT = 20
baseorm = mysql_orm
dataorm = mongo_orm
withBase = withMysql
withData = withMongo
base = ms_dbpc
data = mg_dbpc

DQ = {
    'redis':{
        'host':'localhost',
        'port':6379,
        'db':0,
        'tube':'pholcus-task',
        'log':{
            'host':'localhost',
            'port':6379,
            'db':0,
            'tube':'pholcus-log',
        }
    },
    'beanstalkd':{
        'host':'localhost',
        'port':11300,
        'tube':'pholcus-task',
    }
}
LOGWORKERNUM = 6
LOGSTATUS = [0, 1, 2]