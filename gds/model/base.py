#!/usr/bin/env python
# coding=utf-8
import datetime

from setting import baseorm, dataorm
MAXSIZE = 1000


class AuthModel(baseorm.Model):

    @classmethod
    def queryOne(cls, user, spec, projection={}, sort=[]):
        if not cls.__name__ == 'Creator' and user.get('_id') is None:
            user = Creator.queryOne({}, {'username':user.get('username'), 'secret':user.get('secret')})
            user['name'] = user['username']
        if spec.get('_id') is None:
            auth = {'authority':0}
        else:
            auth = Permit.queryOne({'cid':user.get('_id'), 'otype':cls.__name__, 'oid':spec.get('_id')}, projection={'authority':1}) or {'authority':0}
        if cls.__name__ == 'Creator' or user.get('name') == 'root' or auth.get('authority', 0) % 2 == 1: # 1 3 5 7 9 11 13 15
            result = super(AuthModel, cls).queryOne(spec, projection=projection, sort=sort)
        else:
            result = None
        return result

    @classmethod
    def queryAll(cls, user, spec, projection={}, sort=[], skip=0, limit=10):
        if not cls.__name__ == 'Creator' and user.get('_id') is None:
            user = Creator.queryOne({}, {'username':user.get('username'), 'secret':user.get('secret')})
            user['name'] = user['username']
        auth = Permit.queryOne({'cid':user.get('_id'), 'otype':cls.__name__, 'oid':None}, projection={'authority':1}) or {'authority':0}
        if user.get('name') == 'root' or auth.get('authority', 0) % 2 == 1:
            result = super(AuthModel, cls).queryAll(spec, projection=projection, sort=sort, skip=skip, limit=limit)
        else:
            result = []
        return result

    @classmethod
    def count(cls, user, spec):
        if not cls.__name__ == 'Creator' and user.get('_id') is None:
            user = Creator.queryOne({}, {'username':user.get('username'), 'secret':user.get('secret')})
            user['name'] = user['username']
        auth = Permit.queryOne({'cid':user.get('_id'), 'otype':cls.__name__, 'oid':None}, projection={'authority':1}) or {'authority':0}
        if user.get('name') == 'root' or auth.get('authority', 0) % 2 == 1:
            result = super(AuthModel, cls).count(spec)
        else:
            result = 0
        return result

    @classmethod
    def insert(cls, user, obj, update=True, method='SINGLE', forcexe=False, maxsize=MAXSIZE):
        if not cls.__name__ == 'Creator' and user.get('_id') is None:
            user = Creator.queryOne({}, {'username':user.get('username'), 'secret':user.get('secret')})
            user['name'] = user['username']
        auth = Permit.queryOne({'cid':user.get('_id'), 'otype':cls.__name__, 'oid':None}, projection={'authority':1}) or {'authority':0}
        if cls.__name__ == 'Creator' or user['name'] == 'root' or auth['authority'] > 7: # 8 9 10 11 12 13 14 15
            result = super(AuthModel, cls).insert(obj, update=update, method=method, forcexe=forcexe, maxsize=maxsize)
            user['_id'] = result if cls.__name__ == 'Creator' else user['_id']
            permit = Permit(cid=user['_id'], otype=cls.__name__, oid=result, authority=15, desc='aduq', status=1, creator=user['_id'], updator=user['_id'], create_time=datetime.datetime.now())
            Permit.insert(permit)
        else:
            result = None
        return result

    @classmethod
    def delete(cls, user, spec):
        if not cls.__name__ == 'Creator' and user.get('_id') is None:
            user = Creator.queryOne({}, {'username':user.get('username'), 'secret':user.get('secret')})
            user['name'] = user['username']
        if spec.get('_id') is None:
            auth = {'authority':0}
        else:
            auth = Permit.queryOne({'cid':user.get('_id'), 'otype':cls.__name__, 'oid':spec.get('_id')}, projection={'authority':1}) or {'authority':0}
        if user['name'] == 'root' or auth['authority'] in (4,5,6,7,12,13,14,15):
            # result = super(AuthModel, cls).delete(spec)
            result = super(AuthModel, cls).update(spec, {'$set':{'status':0}})
        else:
            result = None
        return result

    @classmethod
    def update(cls, user, spec, doc):
        if not cls.__name__ == 'Creator' and user.get('_id') is None:
            user = Creator.queryOne({}, {'username':user.get('username'), 'secret':user.get('secret')})
            user['name'] = user['username']
        if spec.get('_id') is None:
            auth = {'authority':0}
        else:
            auth = Permit.queryOne({'cid':user.get('_id'), 'otype':cls.__name__, 'oid':spec.get('_id')}, projection={'authority':1}) or {'authority':0}
        if not user['group'] in ('administrator', 'root') and cls.__name__ == 'Creator' and 'group' in doc:
            del doc['group']
        if user['name'] == 'root' or auth['authority'] in (2,3,6,7,10,11,14,15):
            doc['updator'] = user['_id']
            result = super(AuthModel, cls).update(spec, {'$set':doc})
        else:
            result = None
        return result


class Article(AuthModel):
    __table__ = 'grab_article'
    uid = baseorm.IdField(unique='ga')
    name = baseorm.StrField(ddl='varchar', max_length=20, nullable=0, updatable=False, unique='ga')
    desc = baseorm.StrField(ddl='char', max_length=4)
    pinyin = baseorm.StrField(ddl='varchar', max_length=50)
    host = baseorm.StrField(ddl='varchar', max_length=50)
    filepath = baseorm.StrField(ddl='varchar', max_length=64)
    fileupdate = baseorm.StrField(ddl='int', max_length=1, default=1)
    status = baseorm.IntField(ddl='int', max_length=1)
    extra = baseorm.StrField(ddl='varchar', max_length=300, default=None)
    creator = baseorm.IdField(updatable=False)
    updator = baseorm.IdField()
    create_time = baseorm.DatetimeField(ddl='datetime', updatable=False)
    update_time = baseorm.DatetimeField(ddl='timestamp')


class Codetree(baseorm.Model):
    __table__ = 'grab_codetree'
    bid = baseorm.IdField(unique='gct')
    btype = baseorm.StrField(ddl='varchar', max_length=30, nullable=0, updatable=False, unique='gct')
    sid = baseorm.IdField(unique='gct')
    stype = baseorm.StrField(ddl='varchar', max_length=30, nullable=0, updatable=False, unique='gct')
    pid = baseorm.StrField(ddl='varchar', max_length=50, nullable=0, updatable=False, unique='gct')
    name = baseorm.StrField(ddl='varchar', max_length=100, nullable=0, updatable=False, unique='gct')
    index = baseorm.StrField(ddl='varchar', max_length=100, nullable=0, updatable=False, unique='gct')
    method = baseorm.StrField(ddl='varchar', max_length=30, nullable=0, updatable=False, unique='gct')
    xpath = baseorm.StrField(ddl='varchar', max_length=500)
    default = baseorm.StrField(ddl='varchar', max_length=100)
    content = baseorm.StrField(ddl='varchar', max_length=50)
    datatype = baseorm.StrField(ddl='varchar', max_length=20)


class Config(baseorm.Model):
    __table__ = 'grab_config'
    key = baseorm.StrField(ddl='varchar', max_length=50, nullable=0, updatable=False, unique='gc')
    val = baseorm.StrField(ddl='varchar', max_length=200)
    status = baseorm.IntField(ddl='int', max_length=1)
    extra = baseorm.StrField(ddl='varchar', max_length=300, default=None)
    creator = baseorm.IdField(updatable=False)
    updator = baseorm.IdField()
    create_time = baseorm.DatetimeField(ddl='datetime', updatable=False)
    update_time = baseorm.DatetimeField(ddl='timestamp')


class Creator(AuthModel):
    __table__ = 'grab_creator'
    username = baseorm.StrField(ddl='varchar', max_length=20, nullable=0, updatable=False, unique='gc')
    password = baseorm.StrField(ddl='varchar', max_length=20)
    group = baseorm.StrField(ddl='varchar', max_length=20)
    desc = baseorm.StrField(ddl='varchar', max_length=128)
    avatar = baseorm.StrField(ddl='varchar', max_length=128)
    contact = baseorm.StrField(ddl='varchar', max_length=500)
    notify = baseorm.StrField(ddl='varchar', max_length=100)
    status = baseorm.IntField(ddl='int', max_length=1)
    extra = baseorm.StrField(ddl='varchar', max_length=300, default=None)
    secret = baseorm.StrField(ddl='varchar', max_length=100)
    creator = baseorm.IdField(updatable=False)
    updator = baseorm.IdField()
    create_time = baseorm.DatetimeField(ddl='datetime', updatable=False)
    update_time = baseorm.DatetimeField(ddl='timestamp')


class Dataextract(baseorm.Model):
    __table__ = 'grab_dataextract'
    name = baseorm.StrField(ddl='varchar', max_length=100, nullable=0, updatable=False, unique='gde')
    method = baseorm.StrField(ddl='varchar', max_length=30)
    path = baseorm.StrField(ddl='varchar', max_length=500)
    content = baseorm.StrField(ddl='varchar', max_length=50)
    parameter = baseorm.IntField(ddl='int', max_length=1)
    store = baseorm.IntField(ddl='int', max_length=1)
    sid = baseorm.IdField()
    dsid = baseorm.IdField(unique='gde')
    pdeid = baseorm.IdField()


class Dataitem(baseorm.Model):
    __table__ = 'grab_dataitem'
    dmid = baseorm.IdField(unique='gdi')
    name = baseorm.StrField(ddl='varchar', max_length=64, nullable=0, updatable=False, unique='gdi')
    length = baseorm.IntField(ddl='int', max_length=5)
    default = baseorm.StrField(ddl='varchar', max_length=100)
    comment = baseorm.StrField(ddl='varchar', max_length=200)
    unique = baseorm.StrField(ddl='varchar', max_length=64)


class Datamodel(baseorm.Model):
    __table__ = 'grab_datamodel'
    name = baseorm.StrField(ddl='varchar', max_length=64, nullable=0, updatable=False, unique='gdm')
    table = baseorm.StrField(ddl='varchar', max_length=64)
    comment = baseorm.StrField(ddl='varchar', max_length=200)
    autocreate = baseorm.IntField(ddl='int', max_length=1)
    iscreated = baseorm.IntField(ddl='int', max_length=1)
    filepath = baseorm.StrField(ddl='varchar', max_length=64)
    fileupdate = baseorm.StrField(ddl='int', max_length=1, default=1)
    status = baseorm.IntField(ddl='int', max_length=1)
    extra = baseorm.StrField(ddl='varchar', max_length=300, default=None)
    creator = baseorm.IdField(updatable=False)
    updator = baseorm.IdField()
    create_time = baseorm.DatetimeField(ddl='datetime', updatable=False)
    update_time = baseorm.DatetimeField(ddl='timestamp')


class Datapath(baseorm.Model):
    __table__ = 'grab_datapath'
    bid = baseorm.IdField(unique='gdp')
    btype = baseorm.StrField(ddl='varchar', max_length=30, nullable=0, updatable=False, unique='gdp')
    sid = baseorm.IdField(unique='gdp')
    stype = baseorm.StrField(ddl='varchar', max_length=30, nullable=0, updatable=False, unique='gdp')
    pid = baseorm.StrField(ddl='varchar', max_length=50, nullable=0, updatable=False, unique='gdp')
    name = baseorm.StrField(ddl='varchar', max_length=100, nullable=0, updatable=False, unique='gdp')
    index = baseorm.StrField(ddl='varchar', max_length=100, nullable=0, updatable=False, unique='gdp')
    method = baseorm.StrField(ddl='varchar', max_length=30, nullable=0, updatable=False, unique='gdp')
    xpath = baseorm.StrField(ddl='varchar', max_length=500)
    default = baseorm.StrField(ddl='varchar', max_length=100)
    content = baseorm.StrField(ddl='varchar', max_length=50)
    datatype = baseorm.StrField(ddl='varchar', max_length=20)


class Datasource(baseorm.Model):
    __table__ = 'grab_datasource'
    name = baseorm.StrField(ddl='varchar', max_length=100, nullable=0, updatable=False, unique='gds')
    method = baseorm.StrField(ddl='varchar', max_length=30)
    url = baseorm.StrField(ddl='varchar', max_length=100)
    data = baseorm.StrField(ddl='varchar', max_length=100)
    headers = baseorm.StrField(ddl='varchar', max_length=100)
    cookies = baseorm.StrField(ddl='varchar', max_length=100)
    timeout = baseorm.IntField(ddl='int', max_length=10)
    format = baseorm.StrField(ddl='varchar', max_length=30)
    sid = baseorm.IdField(unique='gds')
    ssid = baseorm.IdField()


class Hash(baseorm.Model):
    __table__ = 'grab_hash'
    sid = baseorm.IdField(unique='gh')
    hashweb = baseorm.IntField(ddl='int', max_length=30, nullable=0, updatable=False, unique='gh')
    create_time = baseorm.DatetimeField(ddl='datetime', updatable=False)
    update_time = baseorm.DatetimeField(ddl='timestamp')


class Permit(baseorm.Model):
    __table__ = 'grab_permit'
    cid = baseorm.IdField(unique='gp')
    oid = baseorm.IdField(unique='gp', default=None)
    otype = baseorm.StrField(ddl='varchar', max_length=50, nullable=0, updatable=False, unique='gp')
    authority = baseorm.IntField(ddl='int', max_length=3)
    desc = baseorm.StrField(ddl='char', max_length=4)
    status = baseorm.IntField(ddl='int', max_length=1)
    extra = baseorm.StrField(ddl='varchar', max_length=300, default=None)
    creator = baseorm.IdField(updatable=False)
    updator = baseorm.IdField()
    create_time = baseorm.DatetimeField(ddl='datetime', updatable=False)
    update_time = baseorm.DatetimeField(ddl='timestamp')


class Section(AuthModel):
    __table__ = 'grab_section'
    aid = baseorm.IdField(unique='gs')
    next_id = baseorm.IdField()
    name = baseorm.StrField(ddl='varchar', max_length=20, nullable=0, updatable=False, unique='gs')
    step = baseorm.IntField(ddl='int', max_length=2)
    flow = baseorm.StrField(ddl='varchar', max_length=20, nullable=0, updatable=False, unique='gs')
    index = baseorm.StrField(ddl='varchar', max_length=20)
    retry = baseorm.IntField(ddl='int', max_length=1)
    timelimit = baseorm.IntField(ddl='int', max_length=4)
    store = baseorm.IntField(ddl='int', max_length=1)
    status = baseorm.IntField(ddl='int', max_length=1)
    additions = baseorm.IntField(ddl='varchar', max_length=1024, default=None)
    extra = baseorm.StrField(ddl='varchar', max_length=300, default=None)
    creator = baseorm.IdField(updatable=False)
    updator = baseorm.IdField()
    create_time = baseorm.DatetimeField(ddl='datetime', updatable=False)
    update_time = baseorm.DatetimeField(ddl='timestamp')


class Task(AuthModel):
    __table__ = 'grab_task'
    aid = baseorm.IdField()
    sid = baseorm.IdField()
    name = baseorm.StrField(ddl='varchar', max_length=50)
    flow = baseorm.StrField(ddl='varchar', max_length=20)
    params = baseorm.StrField(ddl='varchar', max_length=3000)
    worknum = baseorm.IntField(ddl='int', max_length=3)
    queuetype = baseorm.StrField(ddl='char', max_length=1)
    worktype = baseorm.StrField(ddl='varchar', max_length=30)
    trace = baseorm.IntField(ddl='int', max_length=1)
    timeout = baseorm.IntField(ddl='int', max_length=4)
    category = baseorm.StrField(ddl='varchar', max_length=50)
    tag = baseorm.StrField(ddl='varchar', max_length=500)
    type = baseorm.StrField(ddl='varchar', max_length=8)
    push_url = baseorm.StrField(ddl='varchar', max_length=100)
    period = baseorm.IntField(ddl='int', max_length=4)
    status = baseorm.IntField(ddl='int', max_length=1)
    extra = baseorm.StrField(ddl='varchar', max_length=300, default=None)
    creator = baseorm.IdField(updatable=False)
    updator = baseorm.IdField()
    create_time = baseorm.DatetimeField(ddl='datetime', updatable=False)
    update_time = baseorm.DatetimeField(ddl='timestamp')


class Unit(baseorm.Model):
    __table__ = 'grab_unit'
    dmid = baseorm.IdField()
    name = baseorm.StrField(ddl='varchar', max_length=20, nullable=0, updatable=False, unique='gu')
    desc = baseorm.StrField(ddl='char', max_length=4)
    filepath = baseorm.StrField(ddl='varchar', max_length=64)
    fileupdate = baseorm.StrField(ddl='int', max_length=1, default=1)
    status = baseorm.IntField(ddl='int', max_length=1)
    extra = baseorm.StrField(ddl='varchar', max_length=300, default=None)
    creator = baseorm.IdField(updatable=False)
    updator = baseorm.IdField()
    create_time = baseorm.DatetimeField(ddl='datetime', updatable=False)
    update_time = baseorm.DatetimeField(ddl='timestamp')


class Node(baseorm.Model):
    __table__ = 'grab_node'
    dmid = baseorm.IdField()
    ip = baseorm.StrField(ddl='varchar', max_length=20, nullable=0, updatable=False, unique='gn')
    port = baseorm.IntField(ddl='int', max_length=6)
    status = baseorm.IntField(ddl='int', max_length=1)
    extra = baseorm.StrField(ddl='varchar', max_length=300, default=None)
    creator = baseorm.IdField(updatable=False)
    updator = baseorm.IdField()
    create_time = baseorm.DatetimeField(ddl='datetime', updatable=False)
    update_time = baseorm.DatetimeField(ddl='timestamp')


class Waycon(baseorm.Model):
    __table__ = 'grab_waycon'
    name = baseorm.StrField(ddl='varchar', max_length=50, nullable=0, updatable=False, unique='gw')
    desc = baseorm.StrField(ddl='varchar', max_length=200)
    status = baseorm.IntField(ddl='int', max_length=1)
    extra = baseorm.StrField(ddl='varchar', max_length=300, default=None)
    creator = baseorm.IdField(updatable=False)
    updator = baseorm.IdField()
    create_time = baseorm.DatetimeField(ddl='datetime', updatable=False)
    update_time = baseorm.DatetimeField(ddl='timestamp')


if __name__ == '__main__':
    import datetime
    h = Hash(sid=1, hashweb=123456666, create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
    print h
    



