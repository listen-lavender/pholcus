#!/usr/bin/env python
# coding=utf-8

from setting import baseorm, dataorm


class ProxyStatistics(dataorm.Model):
    __table__ = 'grab_proxy_statistics'
    pid = baseorm.IdField(updatable=False)
    avg_elapse = dataorm.FloatField(ddl='float')
    total_elapse = dataorm.FloatField(ddl='float')
    start_time = dataorm.DatetimeField(ddl='datetime', updatable=False)
    end_time = dataorm.DatetimeField(ddl='datetime', updatable=False)
    create_time = dataorm.DatetimeField(ddl='datetime', updatable=False)
    update_time = dataorm.DatetimeField(ddl='timestamp')


class ProxyLog(dataorm.Model):
    __table__ = 'grab_proxy_log'
    pid = dataorm.IdField()
    elapse = dataorm.FloatField(ddl='float')
    create_time = dataorm.DatetimeField(ddl='datetime')


class Logsummary(dataorm.Model):
    __table__ = 'grab_logsummary'
    tid = baseorm.IdField(updatable=False)
    succ = dataorm.IntField(ddl='int', max_length=10)
    fail = dataorm.IntField(ddl='int', max_length=10)
    timeout = dataorm.IntField(ddl='int', max_length=10)
    elapse = dataorm.FloatField(ddl='float')
    create_time = dataorm.DatetimeField(ddl='datetime', updatable=False)


class Log(dataorm.Model):
    __table__ = 'grab_log'
    _id = dataorm.StrField(ddl='varchar', max_length=32, primary=True)
    tid = baseorm.IdField(updatable=False)
    status = dataorm.StrField(ddl='varchar', max_length=8)
    elapse = dataorm.IntField(ddl='float')
    desc = dataorm.StrField(ddl='varchar', default=None, max_length=1280)
    create_time = dataorm.DatetimeField(ddl='datetime', updatable=False)


if __name__ == '__main__':
    pass


