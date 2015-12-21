#!/usr/bin/python
# coding=utf-8

LIMIT = 20
USE = 'local'
WDB = 'local'
RDB = 'local'
_DBCONN = {"local":{"host": "127.0.0.1",
                "port": 3306,
                "user": "root",
                "passwd": "",
                "db": "pholcus",
                "charset": "utf8",
                "use_unicode":False,},
            "use":{
                "rdb":"local",
                "wdb":"local"}
            }
