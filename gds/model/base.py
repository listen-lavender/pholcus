#!/usr/bin/python
# coding=utf-8

from settings import orm
MAXSIZE = 1000


class AuthModel(orm.Model):

    @classmethod
    def queryOne(cls, uid, spec, projection={}, sort=[]):
        user = super(AuthModel, Creator).queryOne({'_id':uid}, projection={'username':1}) or {'username':None}
        auth = super(AuthModel, Permit).queryOne({'cid':uid, 'otype':cls.__name__, 'oid':spec.get('_id')}, projection={'authority':1}) or {'authority':0}
        if cls.__name__ == 'Creator' or user['username'] == 'root' or auth['authority'] % 2 == 1: # 1 3 5 7 9 11 13 15
            result = super(AuthModel, cls).queryOne(spec, projection=projection, sort=sort)
        else:
            result = None
        return result

    @classmethod
    def queryAll(cls, uid, spec, projection={}, sort=[], skip=0, limit=10):
        user = super(AuthModel, Creator).queryOne({'_id':uid}, projection={'username':1}) or {'username':None}
        auth = super(AuthModel, Permit).queryOne({'cid':uid, 'otype':cls.__name__, 'oid':spec.get('_id')}, projection={'authority':1}) or {'authority':0}
        if user['username'] == 'root' or auth['authority'] % 2 == 1: # 1 3 5 7 9 11 13 15
            result = super(AuthModel, cls).queryAll(spec, projection=projection, sort=sort, skip=skip, limit=limit)
        else:
            result = None
        return result

    @classmethod
    def count(cls, uid, spec):
        user = super(AuthModel, Creator).queryOne({'_id':uid}, projection={'username':1}) or {'username':None}
        auth = super(AuthModel, Permit).queryOne({'cid':uid, 'otype':cls.__name__, 'oid':spec.get('_id')}, projection={'authority':1}) or {'authority':0}
        if user['username'] == 'root' or auth['authority'] % 2 == 1: # 1 3 5 7 9 11 13 15
            result = super(AuthModel, cls).count(spec)
        else:
            result = None
        return result

    @classmethod
    def insert(cls, uid, obj, update=True, method='SINGLE', forcexe=False, maxsize=MAXSIZE):
        user = super(AuthModel, Creator).queryOne({'_id':uid}, projection={'username':1}) or {'username':None}
        auth = super(AuthModel, Permit).queryOne({'cid':uid, 'otype':cls.__name__, 'oid':spec.get('_id')}, projection={'authority':1}) or {'authority':0}
        if user['username'] == 'root' or auth['authority'] > 7: # 8 9 10 11 12 13 14 15
            result = super(AuthModel, cls).insert(obj, update=update, method=method, forcexe=forcexe, maxsize=maxsize)
        else:
            result = None
        return result

    @classmethod
    def delete(cls, uid, spec):
        user = super(AuthModel, Creator).queryOne({'_id':uid}, projection={'username':1}) or {'username':None}
        auth = super(AuthModel, Permit).queryOne({'cid':uid, 'otype':cls.__name__, 'oid':spec.get('_id')}, projection={'authority':1}) or {'authority':0}
        if user['username'] == 'root' or auth['authority'] in (4,5,6,7,12,13,14,15):
            result = super(AuthModel, cls).delete(spec)
        else:
            result = None
        return result

    @classmethod
    def update(cls, uid, spec, doc):
        user = super(AuthModel, Creator).queryOne({'_id':uid}, projection={'username':1}) or {'username':None}
        auth = super(AuthModel, Permit).queryOne({'cid':uid, 'otype':cls.__name__, 'oid':spec.get('_id')}, projection={'authority':1}) or {'authority':0}
        if user['username'] == 'root' or auth['authority'] in (2,3,6,7,10,11,14,15):
            result = super(AuthModel, cls).update(spec, doc)
        else:
            result = None
        return result


class Article(AuthModel):
    __table__ = 'grab_article'
    uid = orm.IdField(unique='ga')
    name = orm.StrField(ddl='varchar', max_length=20, nullable=0, updatable=False, unique='ga')
    pinyin = orm.StrField(ddl='varchar', max_length=50)
    host = orm.StrField(ddl='varchar', max_length=50)
    filepath = orm.StrField(ddl='varchar', max_length=64)
    status = orm.IntField(ddl='int', max_length=1)
    extra = orm.StrField(ddl='varchar', max_length=300)
    creator = orm.IdField(updatable=False)
    updator = orm.IdField()
    create_time = orm.DatetimeField(ddl='datetime', updatable=False)
    update_time = orm.DatetimeField(ddl='timestamp')


class Codetree(AuthModel):
    __table__ = 'grab_codetree'
    bid = orm.IdField(unique='gct')
    btype = orm.StrField(ddl='varchar', max_length=30, nullable=0, updatable=False, unique='gct')
    sid = orm.IdField(unique='gct')
    stype = orm.StrField(ddl='varchar', max_length=30, nullable=0, updatable=False, unique='gct')
    pid = orm.StrField(ddl='varchar', max_length=50, nullable=0, updatable=False, unique='gct')
    name = orm.StrField(ddl='varchar', max_length=100, nullable=0, updatable=False, unique='gct')
    index = orm.StrField(ddl='varchar', max_length=100, nullable=0, updatable=False, unique='gct')
    method = orm.StrField(ddl='varchar', max_length=30, nullable=0, updatable=False, unique='gct')
    xpath = orm.StrField(ddl='varchar', max_length=500)
    default = orm.StrField(ddl='varchar', max_length=100)
    content = orm.StrField(ddl='varchar', max_length=50)
    datatype = orm.StrField(ddl='varchar', max_length=20)


class Config(AuthModel):
    __table__ = 'grab_config'
    type = orm.StrField(ddl='varchar', max_length=20, nullable=0, updatable=False, unique='gc')
    name = orm.StrField(ddl='varchar', max_length=50, nullable=0, updatable=False, unique='gc')
    key = orm.StrField(ddl='varchar', max_length=50, nullable=0, updatable=False, unique='gc')
    val = orm.StrField(ddl='varchar', max_length=200)
    filepath = orm.StrField(ddl='varchar', max_length=100)
    status = orm.IntField(ddl='int', max_length=1)
    extra = orm.StrField(ddl='varchar', max_length=300)
    creator = orm.IdField(updatable=False)
    updator = orm.IdField()
    create_time = orm.DatetimeField(ddl='datetime', updatable=False)
    update_time = orm.DatetimeField(ddl='timestamp')


class Creator(AuthModel):
    __table__ = 'grab_creator'
    username = orm.StrField(ddl='varchar', max_length=20, nullable=0, updatable=False, unique='gc')
    password = orm.StrField(ddl='varchar', max_length=20)
    group = orm.StrField(ddl='varchar', max_length=20)
    desc = orm.StrField(ddl='varchar', max_length=128)
    avartar = orm.StrField(ddl='varchar', max_length=128)
    contact = orm.StrField(ddl='varchar', max_length=500)
    notify = orm.StrField(ddl='varchar', max_length=100)
    status = orm.IntField(ddl='int', max_length=1)
    extra = orm.StrField(ddl='varchar', max_length=300)
    secret = orm.StrField(ddl='varchar', max_length=100)
    creator = orm.IdField(updatable=False)
    updator = orm.IdField()
    create_time = orm.DatetimeField(ddl='datetime', updatable=False)
    update_time = orm.DatetimeField(ddl='timestamp')


class Dataextract(AuthModel):
    __table__ = 'grab_dataextract'
    name = orm.StrField(ddl='varchar', max_length=100, nullable=0, updatable=False, unique='gde')
    method = orm.StrField(ddl='varchar', max_length=30)
    path = orm.StrField(ddl='varchar', max_length=500)
    content = orm.StrField(ddl='varchar', max_length=50)
    parameter = orm.IntField(ddl='int', max_length=1)
    store = orm.IntField(ddl='int', max_length=1)
    sid = orm.IdField()
    dsid = orm.IdField(unique='gde')
    pdeid = orm.IdField()


class Dataitem(AuthModel):
    __table__ = 'grab_dataitem'
    dmid = orm.IdField(unique='gdi')
    name = orm.StrField(ddl='varchar', max_length=64, nullable=0, updatable=False, unique='gdi')
    length = orm.IntField(ddl='int', max_length=5)
    default = orm.StrField(ddl='varchar', max_length=100)
    comment = orm.StrField(ddl='varchar', max_length=200)
    unique = orm.StrField(ddl='varchar', max_length=64)


class Datamodel(AuthModel):
    __table__ = 'grab_datamodel'
    name = orm.StrField(ddl='varchar', max_length=64, nullable=0, updatable=False, unique='gdm')
    table = orm.StrField(ddl='varchar', max_length=64)
    comment = orm.StrField(ddl='varchar', max_length=200)
    autocreate = orm.IntField(ddl='int', max_length=1)
    iscreated = orm.IntField(ddl='int', max_length=1)
    status = orm.IntField(ddl='int', max_length=1)
    extra = orm.StrField(ddl='varchar', max_length=300)
    creator = orm.IdField(updatable=False)
    updator = orm.IdField()
    create_time = orm.DatetimeField(ddl='datetime', updatable=False)
    update_time = orm.DatetimeField(ddl='timestamp')


class Datapath(AuthModel):
    __table__ = 'grab_datapath'
    bid = orm.IdField(unique='gdp')
    btype = orm.StrField(ddl='varchar', max_length=30, nullable=0, updatable=False, unique='gdp')
    sid = orm.IdField(unique='gdp')
    stype = orm.StrField(ddl='varchar', max_length=30, nullable=0, updatable=False, unique='gdp')
    pid = orm.StrField(ddl='varchar', max_length=50, nullable=0, updatable=False, unique='gdp')
    name = orm.StrField(ddl='varchar', max_length=100, nullable=0, updatable=False, unique='gdp')
    index = orm.StrField(ddl='varchar', max_length=100, nullable=0, updatable=False, unique='gdp')
    method = orm.StrField(ddl='varchar', max_length=30, nullable=0, updatable=False, unique='gdp')
    xpath = orm.StrField(ddl='varchar', max_length=500)
    default = orm.StrField(ddl='varchar', max_length=100)
    content = orm.StrField(ddl='varchar', max_length=50)
    datatype = orm.StrField(ddl='varchar', max_length=20)


class Datasource(AuthModel):
    __table__ = 'grab_datasource'
    name = orm.StrField(ddl='varchar', max_length=100, nullable=0, updatable=False, unique='gds')
    method = orm.StrField(ddl='varchar', max_length=30)
    url = orm.StrField(ddl='varchar', max_length=100)
    data = orm.StrField(ddl='varchar', max_length=100)
    headers = orm.StrField(ddl='varchar', max_length=100)
    cookies = orm.StrField(ddl='varchar', max_length=100)
    timeout = orm.IntField(ddl='int', max_length=10)
    format = orm.StrField(ddl='varchar', max_length=30)
    sid = orm.IdField(unique='gds')
    ssid = orm.IdField()


class Hash(AuthModel):
    __table__ = 'grab_hash'
    sid = orm.IdField(unique='gh')
    hashweb = orm.IntField(ddl='int', max_length=30, nullable=0, updatable=False, unique='gh')
    create_time = orm.DatetimeField(ddl='datetime', updatable=False)
    update_time = orm.DatetimeField(ddl='timestamp')


class Log(AuthModel):
    __table__ = 'grab_log'
    gsid = orm.IdField(unique='gl')
    sname = orm.StrField(ddl='varchar', max_length=20)
    succ = orm.IntField(ddl='int', max_length=10)
    fail = orm.IntField(ddl='int', max_length=10)
    timeout = orm.IntField(ddl='int', max_length=10)
    create_time = orm.DatetimeField(ddl='datetime', updatable=False)


class Permit(AuthModel):
    __table__ = 'grab_permit'
    cid = orm.IdField(unique='gp')
    oid = orm.IdField(unique='gp')
    otype = orm.StrField(ddl='varchar', max_length=50, nullable=0, updatable=False, unique='gp')
    authority = orm.IntField(ddl='int', max_length=3)
    desc = orm.StrField(ddl='char', max_length=4)
    status = orm.IntField(ddl='int', max_length=1)
    extra = orm.StrField(ddl='varchar', max_length=300)
    creator = orm.IdField(updatable=False)
    updator = orm.IdField()
    create_time = orm.DatetimeField(ddl='datetime', updatable=False)
    update_time = orm.DatetimeField(ddl='timestamp')


class ProxyStatistics(AuthModel):
    __table__ = 'grab_proxy_statistics'
    pid = orm.IdField()
    avg_elapse = orm.FloatField(ddl='float')
    total_elapse = orm.FloatField(ddl='float')
    start_time = orm.DatetimeField(ddl='datetime', updatable=False)
    end_time = orm.DatetimeField(ddl='datetime', updatable=False)
    create_time = orm.DatetimeField(ddl='datetime', updatable=False)
    update_time = orm.DatetimeField(ddl='timestamp')


class Section(AuthModel):
    __table__ = 'grab_section'
    aid = orm.IdField(unique='gs')
    next_id = orm.IdField()
    name = orm.StrField(ddl='varchar', max_length=20, nullable=0, updatable=False, unique='gs')
    step = orm.IntField(ddl='int', max_length=2)
    flow = orm.StrField(ddl='varchar', max_length=20, nullable=0, updatable=False, unique='gs')
    index = orm.StrField(ddl='varchar', max_length=20)
    retry = orm.IntField(ddl='int', max_length=1)
    timelimit = orm.IntField(ddl='int', max_length=4)
    store = orm.IntField(ddl='int', max_length=1)
    status = orm.IntField(ddl='int', max_length=1)
    extra = orm.StrField(ddl='varchar', max_length=300)
    creator = orm.IdField(updatable=False)
    updator = orm.IdField()
    create_time = orm.DatetimeField(ddl='datetime', updatable=False)
    update_time = orm.DatetimeField(ddl='timestamp')


class Statistics(AuthModel):
    __table__ = 'grab_statistics'
    tid = orm.IdField()
    succ = orm.IntField(ddl='int', max_length=10)
    fail = orm.IntField(ddl='int', max_length=10)
    timeout = orm.IntField(ddl='int', max_length=10)
    elapse = orm.FloatField(ddl='float')
    create_time = orm.DatetimeField(ddl='datetime', updatable=False)


class Task(AuthModel):
    __table__ = 'grab_task'
    aid = orm.IdField()
    sid = orm.IdField()
    name = orm.StrField(ddl='varchar', max_length=50)
    flow = orm.StrField(ddl='varchar', max_length=20)
    params = orm.StrField(ddl='varchar', max_length=3000)
    worknum = orm.IntField(ddl='int', max_length=3)
    queuetype = orm.StrField(ddl='char', max_length=1)
    worktype = orm.StrField(ddl='varchar', max_length=30)
    trace = orm.IntField(ddl='int', max_length=1)
    timeout = orm.IntField(ddl='int', max_length=4)
    category = orm.StrField(ddl='varchar', max_length=50)
    tag = orm.StrField(ddl='varchar', max_length=500)
    type = orm.StrField(ddl='varchar', max_length=8)
    push_url = orm.StrField(ddl='varchar', max_length=100)
    period = orm.IntField(ddl='int', max_length=4)
    status = orm.IntField(ddl='int', max_length=1)
    extra = orm.StrField(ddl='varchar', max_length=300)
    creator = orm.IdField(updatable=False)
    updator = orm.IdField()
    create_time = orm.DatetimeField(ddl='datetime', updatable=False)
    update_time = orm.DatetimeField(ddl='timestamp')


class Unit(AuthModel):
    __table__ = 'grab_unit'
    dmid = orm.IdField()
    name = orm.StrField(ddl='varchar', max_length=20, nullable=0, updatable=False, unique='gu')
    dirpath = orm.StrField(ddl='varchar', max_length=64)
    filepath = orm.StrField(ddl='varchar', max_length=64)
    status = orm.IntField(ddl='int', max_length=1)
    extra = orm.StrField(ddl='varchar', max_length=300)
    creator = orm.IdField(updatable=False)
    updator = orm.IdField()
    create_time = orm.DatetimeField(ddl='datetime', updatable=False)
    update_time = orm.DatetimeField(ddl='timestamp')


class Waycon(AuthModel):
    __table__ = 'grab_waycon'
    name = orm.StrField(ddl='varchar', max_length=50, nullable=0, updatable=False, unique='gw')
    desc = orm.StrField(ddl='varchar', max_length=200)
    status = orm.IntField(ddl='int', max_length=1)
    extra = orm.StrField(ddl='varchar', max_length=300)
    creator = orm.IdField(updatable=False)
    updator = orm.IdField()
    create_time = orm.DatetimeField(ddl='datetime', updatable=False)
    update_time = orm.DatetimeField(ddl='timestamp')


if __name__ == '__main__':
    import datetime
    h = Hash(sid=1, hashweb=123456666, create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
    print h
    



