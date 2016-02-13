#!/usr/bin/python
# coding=utf-8

from settings import orm


class Article(orm.Model):
    __table__ = 'grab_article'
    uid = orm.IntField(ddl='int', max_length='11', unique='ga')
    name = orm.StrField(ddl='varchar', max_length='20', unique='ga')
    pinyin = orm.StrField(ddl='varchar', max_length='50')
    host = orm.StrField(ddl='varchar', max_length='50')
    filepath = orm.StrField(ddl='varchar', max_length='64')
    status = orm.IntField(ddl='int', max_length='1')
    extra = orm.StrField(ddl='varchar', max_length='300')
    creator = orm.IntField(ddl='int', max_length='11')
    updator = orm.IntField(ddl='int', max_length='11')
    create_time = orm.DatetimeField(ddl='datetime')
    update_time = orm.DatetimeField(ddl='datetime')


class Codetree(orm.Model):
    __table__ = 'grab_codetree'
    bid = orm.IntField(ddl='int', max_length='11', unique='gct')
    btype = orm.StrField(ddl='varchar', max_length='30', unique='gct')
    sid = orm.IntField(ddl='int', max_length='11', unique='gct')
    stype = orm.StrField(ddl='varchar', max_length='30', unique='gct')
    pid = orm.StrField(ddl='varchar', max_length='50', unique='gct')
    name = orm.StrField(ddl='varchar', max_length='100', unique='gct')
    index = orm.StrField(ddl='varchar', max_length='100', unique='gct')
    method = orm.StrField(ddl='varchar', max_length='30', unique='gct')
    xpath = orm.StrField(ddl='varchar', max_length='500')
    default = orm.StrField(ddl='varchar', max_length='100')
    content = orm.StrField(ddl='varchar', max_length='50')
    datatype = orm.StrField(ddl='varchar', max_length='20')


class Config(orm.Model):
    __table__ = 'grab_config'
    type = orm.StrField(ddl='varchar', max_length='20', unique='gc')
    name = orm.StrField(ddl='varchar', max_length='50', unique='gc')
    key = orm.StrField(ddl='varchar', max_length='50', unique='gc')
    val = orm.StrField(ddl='varchar', max_length='200')
    filepath = orm.StrField(ddl='varchar', max_length='100')
    status = orm.IntField(ddl='int', max_length='1')
    extra = orm.StrField(ddl='varchar', max_length='300')
    creator = orm.IntField(ddl='int', max_length='11')
    updator = orm.IntField(ddl='int', max_length='11')
    create_time = orm.DatetimeField(ddl='datetime')
    update_time = orm.DatetimeField(ddl='datetime')


class Creator(orm.Model):
    __table__ = 'grab_creator'
    username = orm.StrField(ddl='varchar', max_length='20', unique='gc')
    password = orm.StrField(ddl='varchar', max_length='20')
    authority = orm.IntField(ddl='int', max_length='3')
    desc = orm.StrField(ddl='char', max_length='4')
    contact = orm.StrField(ddl='varchar', max_length='500')
    notify = orm.StrField(ddl='varchar', max_length='100')
    status = orm.IntField(ddl='int', max_length='1')
    extra = orm.StrField(ddl='varchar', max_length='300')
    secret = orm.StrField(ddl='varchar', max_length='100')
    creator = orm.IntField(ddl='int', max_length='11')
    updator = orm.IntField(ddl='int', max_length='11')
    create_time = orm.DatetimeField(ddl='datetime')
    update_time = orm.DatetimeField(ddl='datetime')


class Dataextract(orm.Model):
    __table__ = 'grab_dataextract'
    name = orm.StrField(ddl='varchar', max_length='100', unique='gde')
    method = orm.StrField(ddl='varchar', max_length='30')
    path = orm.StrField(ddl='varchar', max_length='500')
    content = orm.StrField(ddl='varchar', max_length='50')
    parameter = orm.IntField(ddl='int', max_length='1')
    store = orm.IntField(ddl='int', max_length='1')
    sid = orm.IntField(ddl='int', max_length='11')
    dsid = orm.IntField(ddl='int', max_length='11', unique='gde')
    pdeid = orm.IntField(ddl='int', max_length='11')


class Dataitem(orm.Model):
    __table__ = 'grab_dataitem'
    dmid = orm.IntField(ddl='int', max_length='11', unique='gdi')
    name = orm.StrField(ddl='varchar', max_length='64', unique='gdi')
    length = orm.IntField(ddl='int', max_length='11')
    default = orm.StrField(ddl='varchar', max_length='100')
    comment = orm.StrField(ddl='varchar', max_length='200')
    unique = orm.StrField(ddl='varchar', max_length='64')


class Datamodel(orm.Model):
    __table__ = 'grab_datamodel'
    name = orm.StrField(ddl='varchar', max_length='64', unique='gdm')
    table = orm.StrField(ddl='varchar', max_length='64')
    comment = orm.StrField(ddl='varchar', max_length='200')
    autocreate = orm.IntField(ddl='int', max_length='1')
    iscreated = orm.IntField(ddl='int', max_length='1')
    status = orm.IntField(ddl='int', max_length='1')
    extra = orm.StrField(ddl='varchar', max_length='300')
    creator = orm.IntField(ddl='int', max_length='11')
    updator = orm.IntField(ddl='int', max_length='11')
    create_time = orm.DatetimeField(ddl='datetime')
    update_time = orm.DatetimeField(ddl='datetime')


class Datapath(orm.Model):
    __table__ = 'grab_datapath'
    bid = orm.IntField(ddl='int', max_length='11', unique='gdp')
    btype = orm.StrField(ddl='varchar', max_length='30', unique='gdp')
    sid = orm.IntField(ddl='int', max_length='11', unique='gdp')
    stype = orm.StrField(ddl='varchar', max_length='30', unique='gdp')
    pid = orm.StrField(ddl='varchar', max_length='50', unique='gdp')
    name = orm.StrField(ddl='varchar', max_length='100', unique='gdp')
    index = orm.StrField(ddl='varchar', max_length='100', unique='gdp')
    method = orm.StrField(ddl='varchar', max_length='30', unique='gdp')
    xpath = orm.StrField(ddl='varchar', max_length='500')
    default = orm.StrField(ddl='varchar', max_length='100')
    content = orm.StrField(ddl='varchar', max_length='50')
    datatype = orm.StrField(ddl='varchar', max_length='20')


class Datasource(orm.Model):
    __table__ = 'grab_datasource'
    name = orm.StrField(ddl='varchar', max_length='100', unique='gds')
    method = orm.StrField(ddl='varchar', max_length='30')
    url = orm.StrField(ddl='varchar', max_length='100')
    data = orm.StrField(ddl='varchar', max_length='100')
    headers = orm.StrField(ddl='varchar', max_length='100')
    cookies = orm.StrField(ddl='varchar', max_length='100')
    timeout = orm.IntField(ddl='int', max_length='11')
    format = orm.StrField(ddl='varchar', max_length='30')
    sid = orm.IntField(ddl='int', max_length='11', unique='gds')
    ssid = orm.IntField(ddl='int', max_length='11')


class Hash(orm.Model):
    __table__ = 'grab_hash'
    sid = orm.IntField(ddl='int', max_length='11', unique='gh')
    hashweb = orm.IntField(ddl='int', max_length='30', unique='gh')
    create_time = orm.DatetimeField(ddl='datetime')
    update_time = orm.DatetimeField(ddl='datetime')


class Log(orm.Model):
    __table__ = 'grab_log'
    gsid = orm.IntField(ddl='int', max_length='11', unique='gl')
    sname = orm.StrField(ddl='varchar', max_length='20')
    succ = orm.IntField(ddl='int', max_length='11')
    fail = orm.IntField(ddl='int', max_length='11')
    timeout = orm.IntField(ddl='int', max_length='11')
    create_time = orm.DatetimeField(ddl='datetime')


class Permit(orm.Model):
    __table__ = 'grab_permit'
    cid = orm.IntField(ddl='int', max_length='11', unique='gp')
    oid = orm.IntField(ddl='int', max_length='11', unique='gp')
    otype = orm.StrField(ddl='char', max_length='1', unique='gp')
    authority = orm.IntField(ddl='int', max_length='3')
    desc = orm.StrField(ddl='char', max_length='4')
    status = orm.IntField(ddl='int', max_length='1')
    extra = orm.StrField(ddl='varchar', max_length='300')
    creator = orm.IntField(ddl='int', max_length='11')
    updator = orm.IntField(ddl='int', max_length='11')
    create_time = orm.DatetimeField(ddl='datetime')
    update_time = orm.DatetimeField(ddl='datetime')


class ProxyStatistics(orm.Model):
    __table__ = 'grab_proxy_statistics'
    pid = orm.IntField(ddl='int', max_length='11')
    avg_elapse = orm.FloatField(ddl='float')
    total_elapse = orm.FloatField(ddl='float')
    start_time = orm.DatetimeField(ddl='datetime')
    end_time = orm.DatetimeField(ddl='datetime')
    create_time = orm.DatetimeField(ddl='datetime')
    update_time = orm.DatetimeField(ddl='datetime')


class Section(orm.Model):
    __table__ = 'grab_section'
    aid = orm.IntField(ddl='int', max_length='11', unique='gs')
    next_id = orm.IntField(ddl='int', max_length='11')
    name = orm.StrField(ddl='varchar', max_length='20', unique='gs')
    step = orm.IntField(ddl='int', max_length='2')
    flow = orm.StrField(ddl='varchar', max_length='20', unique='gs')
    index = orm.StrField(ddl='varchar', max_length='20')
    retry = orm.IntField(ddl='int', max_length='1')
    timelimit = orm.IntField(ddl='int', max_length='4')
    store = orm.IntField(ddl='int', max_length='1')
    status = orm.IntField(ddl='int', max_length='1')
    extra = orm.StrField(ddl='varchar', max_length='300')
    creator = orm.IntField(ddl='int', max_length='11')
    updator = orm.IntField(ddl='int', max_length='11')
    create_time = orm.DatetimeField(ddl='datetime')
    update_time = orm.DatetimeField(ddl='datetime')


class Statistics(orm.Model):
    __table__ = 'grab_statistics'
    tid = orm.IntField(ddl='int', max_length='11')
    succ = orm.IntField(ddl='int', max_length='11')
    fail = orm.IntField(ddl='int', max_length='11')
    timeout = orm.IntField(ddl='int', max_length='11')
    elapse = orm.FloatField(ddl='float')
    create_time = orm.DatetimeField(ddl='datetime')


class Task(orm.Model):
    __table__ = 'grab_task'
    aid = orm.IntField(ddl='int', max_length='11')
    sid = orm.IntField(ddl='int', max_length='11')
    name = orm.StrField(ddl='varchar', max_length='50')
    flow = orm.StrField(ddl='varchar', max_length='20')
    params = orm.StrField(ddl='varchar', max_length='3000')
    worknum = orm.IntField(ddl='int', max_length='3')
    queuetype = orm.StrField(ddl='char', max_length='1')
    worktype = orm.StrField(ddl='varchar', max_length='30')
    trace = orm.IntField(ddl='int', max_length='1')
    timeout = orm.IntField(ddl='int', max_length='4')
    category = orm.StrField(ddl='varchar', max_length='50')
    tag = orm.StrField(ddl='varchar', max_length='500')
    type = orm.StrField(ddl='varchar', max_length='8')
    push_url = orm.StrField(ddl='varchar', max_length='100')
    period = orm.IntField(ddl='int', max_length='4')
    status = orm.IntField(ddl='int', max_length='1')
    extra = orm.StrField(ddl='varchar', max_length='300')
    creator = orm.IntField(ddl='int', max_length='11')
    updator = orm.IntField(ddl='int', max_length='11')
    create_time = orm.DatetimeField(ddl='datetime')
    update_time = orm.DatetimeField(ddl='datetime')


class Unit(orm.Model):
    __table__ = 'grab_unit'
    dmid = orm.IntField(ddl='int', max_length='11')
    name = orm.StrField(ddl='varchar', max_length='20', unique='gu')
    dirpath = orm.StrField(ddl='varchar', max_length='64')
    filepath = orm.StrField(ddl='varchar', max_length='64')
    status = orm.IntField(ddl='int', max_length='1')
    extra = orm.StrField(ddl='varchar', max_length='300')
    creator = orm.IntField(ddl='int', max_length='11')
    updator = orm.IntField(ddl='int', max_length='11')
    create_time = orm.DatetimeField(ddl='datetime')
    update_time = orm.DatetimeField(ddl='datetime')


class Waycon(orm.Model):
    __table__ = 'grab_waycon'
    name = orm.StrField(ddl='varchar', max_length='50', unique='gw')
    desc = orm.StrField(ddl='varchar', max_length='200')
    status = orm.IntField(ddl='int', max_length='1')
    extra = orm.StrField(ddl='varchar', max_length='300')
    creator = orm.IntField(ddl='int', max_length='11')
    updator = orm.IntField(ddl='int', max_length='11')
    create_time = orm.DatetimeField(ddl='datetime')
    update_time = orm.DatetimeField(ddl='datetime')


if __name__ == '__main__':
    pass



