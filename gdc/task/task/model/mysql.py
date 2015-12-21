#!/usr/bin/python
# coding=utf-8

from datakit.mysql.orm import *
from datakit.mysql.suit import dbpc
from task.config.db.mysql import RDB, WDB, LIMIT, _DBCONN, USE

def initDB():
    dbpc.addDB(RDB, LIMIT, host=_DBCONN[USE]['host'],
                port=_DBCONN[USE]['port'],
                user=_DBCONN[USE]['user'],
                passwd=_DBCONN[USE]['passwd'],
                db=_DBCONN[USE]['db'],
                charset=_DBCONN[USE]['charset'],
                use_unicode=_DBCONN[USE]['use_unicode'],
                override=False)
    dbpc.addDB(WDB, LIMIT, host=_DBCONN[USE]['host'],
                port=_DBCONN[USE]['port'],
                user=_DBCONN[USE]['user'],
                passwd=_DBCONN[USE]['passwd'],
                db=_DBCONN[USE]['db'],
                charset=_DBCONN[USE]['charset'],
                use_unicode=_DBCONN[USE]['use_unicode'],
                override=False)

'''
@comment('代理数据')
'''
class Proxy(MarkModel):
    __table__ = 'grab_proxy'
    ip = StrField(ddl='str', unique='daili')
    port = IntField(ddl='int(5)', unique='daili')
    location = StrField(ddl='varchar(30)')
    safetype = StrField(ddl='varchar(30)')
    usetype = StrField(ddl='varchar(30)')
    refspeed = FloatField(ddl='float')
    usespeed = FloatField(ddl='float')
    usenum = IntField(ddl='int(10)')
    status = Field(ddl='tinyint(1)')


class ProxyLog(Model):
    __table__ = 'grab_proxy_log'
    pid = IntField(ddl='int(11)')
    elapse = FloatField(ddl='float')
    create_time = DatetimeField(ddl='datetime')

if __name__ == '__main__':
    pass


