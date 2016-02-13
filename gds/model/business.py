#!/usr/bin/python
# coding=utf-8

from settings import orm

class MarkModel(orm.Model):

    def __init__(self, **attributes):
        self.__mappings__['create_time'] = orm.DatetimeField(ddl='datetime')
        self.__mappings__['update_time'] = orm.DatetimeField(ddl='datetime')
        self.__mappings__['tid'] = orm.IntField(ddl='int')
        attributes['create_time'] = attributes.get('create_time', datetime.datetime.now())
        attributes['update_time'] = attributes.get('update_time', datetime.datetime.now())
        for key in self.__mappings__:
            if not key in attributes:
                raise Exception('Need field %s. ' % key)
            attributes[key] = self.__mappings__[key].check_value(attributes[key])
        super(MarkModel, self).__init__(**attributes)

    def __setstate__(self, state):
        self.__dict__ = state

    def __getstate__(self):
        return self.__dict__


'''
@comment('代理数据')
'''
class Proxy(MarkModel):
    __table__ = 'grab_proxy'
    ip = orm.StrField(ddl='varchar(20)', unique='gp')
    port = orm.IntField(ddl='int(10)', unique='gp')
    location = orm.StrField(ddl='varchar(30)')
    safetype = orm.StrField(ddl='varchar(30)')
    protocol = orm.StrField(ddl='varchar(30)')
    refspeed = orm.FloatField(ddl='float')
    usespeed = orm.FloatField(ddl='float')
    usenum = orm.IntField(ddl='int(10)')
    status = orm.IntField(ddl='tinyint(1)')
    extra = orm.StrField(ddl='varchar(300)')
    creator = orm.IntField(ddl='int(11)')
    updator = orm.IntField(ddl='int(11)')


class ProxyLog(orm.Model):
    __table__ = 'grab_proxy_log'
    pid = orm.IntField(ddl='int(11)')
    elapse = orm.FloatField(ddl='float')
    create_time = orm.DatetimeField(ddl='datetime')

if __name__ == '__main__':
    pass


