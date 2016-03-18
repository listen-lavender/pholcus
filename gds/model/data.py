#!/usr/bin/env python
# coding=utf-8
import datetime
from setting import baseorm, dataorm

class MarkModel(dataorm.Model):
    create_time = dataorm.DatetimeField(ddl='datetime', updatable=False)
    update_time = dataorm.DatetimeField(ddl='timestamp')
    tid = baseorm.IdField(unique='data', updatable=False)

    def __init__(self, **attributes):
        # self.__mappings__['create_time'] = dataorm.DatetimeField(ddl='datetime')
        # self.__mappings__['update_time'] = dataorm.DatetimeField(ddl='datetime')
        # self.__mappings__['tid'] = baseorm.IdField(unique='data', updatable=False)
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
    ip = dataorm.StrField(ddl='varchar', max_length=20, unique='data', updatable=False)
    port = dataorm.IntField(ddl='int', max_length=10, unique='data', updatable=False)
    location = dataorm.StrField(ddl='varchar', max_length=30)
    safetype = dataorm.StrField(ddl='varchar', max_length=30)
    protocol = dataorm.StrField(ddl='varchar', max_length=30)
    refspeed = dataorm.FloatField(ddl='float')
    usespeed = dataorm.FloatField(ddl='float')
    usenum = dataorm.IntField(ddl='int', max_length=10)
    status = dataorm.IntField(ddl='int', max_length=1)
    extra = dataorm.StrField(ddl='varchar', max_length=300)
    creator = dataorm.IdField()
    updator = dataorm.IdField()


if __name__ == '__main__':
    pass


