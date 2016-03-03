#!/usr/bin/env python
# coding=utf-8

from setting import baseorm, dataorm

class Log(dataorm.Model):
    __table__ = 'grab_log'
    gsid = baseorm.IdField(updatable=False)
    sname = dataorm.StrField(ddl='varchar', max_length=20)
    succ = dataorm.IntField(ddl='int', max_length=10)
    fail = dataorm.IntField(ddl='int', max_length=10)
    timeout = dataorm.IntField(ddl='int', max_length=10)
    create_time = dataorm.DatetimeField(ddl='datetime', updatable=False)


class ProxyStatistics(dataorm.Model):
    __table__ = 'grab_proxy_statistics'
    pid = baseorm.IdField(updatable=False)
    avg_elapse = dataorm.FloatField(ddl='float')
    total_elapse = dataorm.FloatField(ddl='float')
    start_time = dataorm.DatetimeField(ddl='datetime', updatable=False)
    end_time = dataorm.DatetimeField(ddl='datetime', updatable=False)
    create_time = dataorm.DatetimeField(ddl='datetime', updatable=False)
    update_time = dataorm.DatetimeField(ddl='timestamp')


class Statistics(dataorm.Model):
    __table__ = 'grab_statistics'
    tid = baseorm.IdField(updatable=False)
    succ = dataorm.IntField(ddl='int', max_length=10)
    fail = dataorm.IntField(ddl='int', max_length=10)
    timeout = dataorm.IntField(ddl='int', max_length=10)
    elapse = dataorm.FloatField(ddl='float')
    create_time = dataorm.DatetimeField(ddl='datetime', updatable=False)


class ProxyLog(dataorm.Model):
    __table__ = 'grab_proxy_log'
    pid = dataorm.IdField()
    elapse = dataorm.FloatField(ddl='float')
    create_time = dataorm.DatetimeField(ddl='datetime')

class RunLog(dataorm.Model):
    __table__ = 'grab_runlog'
    tid = baseorm.IdField(updatable=False)
    sname = dataorm.StrField(ddl='varchar', max_length=20)
    priority = dataorm.IntField(ddl='int', max_length=5)
    times = dataorm.IntField(ddl='int', max_length=2)
    args = dataorm.StrField(ddl='varchar', max_length=20)
    kwargs = dataorm.StrField(ddl='varchar', max_length=20)
    txt = dataorm.StrField(ddl='varchar', max_length=20)
    create_time = dataorm.DatetimeField(ddl='datetime')

if __name__ == '__main__':
    pass


