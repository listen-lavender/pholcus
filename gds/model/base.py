#!/usr/bin/env python
# coding=utf-8
import datetime

from setting import baseorm, dataorm
MAXSIZE = 1000


class AuthModel(baseorm.Model):

    @classmethod
    def queryOne(cls, user, spec, projection={}, sort=[]):
        if spec.get('_id') is None and user and not user.get('api'):
            raise Exception("Wrong detail query condition without id.")
        auth = {'authority':0}
        updatable = None
        if cls.__name__ in ('Creator', 'Article', 'Task') and user and not user.get('api'):
            auth = Permit.queryOne({'cid':user['_id'], 'otype':cls.__name__, 'oid':spec['_id']}, projection={'authority':1}) or {'authority':0}
            updatable = auth['authority'] in (2,3,6,7,10,11,14,15)
        else:
            auth['authority'] = 1
        if auth['authority'] % 2 == 1 or user['group'] == 'administrator': # 1 3 5 7 9 11 13 15
            result = super(AuthModel, cls).queryOne(spec, projection=projection, sort=sort)
            if updatable is not None:
                result['updatable'] = updatable
        else:
            result = None
        return result

    @classmethod
    def queryAll(cls, user, spec, projection={}, sort=[], skip=0, limit=10):
        if cls.__name__ in ('Creator', 'Task', 'Article'):
            result = super(AuthModel, cls).queryAll(spec, projection=projection, sort=sort, skip=skip, limit=limit)
            for one in result:
                auth = Permit.queryOne({'cid':user['_id'], 'otype':cls.__name__, 'oid':one['_id']}, projection={'authority':1}) or {'authority':0}
                one['queryable'] = auth['authority'] % 2 == 1
                one['own'] = auth['authority'] == 15
        else:
            result = super(AuthModel, cls).queryAll(spec, projection=projection, sort=sort, skip=skip, limit=limit)
        return result

    @classmethod
    def reverseQuery(cls, user, projection={}, sort=[], skip=0, limit=10):
        result = []
        if cls.__name__ in ('Creator', 'Task', 'Article'):
            for one in Permit.queryAll({'cid':user['_id'], 'otype':cls.__name__}, projection={'authority':1}, skip=0, limit=None):
                one = super(AuthModel, cls).queryOne({'_id':one['oid']}, projection=projection)
                result.append(one)
        return result

    @classmethod
    def insert(cls, user, obj, update=True, method='SINGLE', maxsize=MAXSIZE):
        if cls.__name__ in ('Datamodel', 'Unit', 'Article', 'Flow', 'Section') and not user['group'] == 'developer':
            raise Exception("Wrong user for creating script relationship.")
        if cls.__name__ == 'Creator':
            result = super(AuthModel, cls).insert(obj, update=update, method=method, maxsize=maxsize)
            user['_id'] = result
        else:
            obj['creator'] = user.get('_id')
            obj['updator'] = user.get('_id')
            result = super(AuthModel, cls).insert(obj, update=update, method=method, maxsize=maxsize)
        if cls.__name__ in ('Creator', 'Task', 'Article'):
            permit = Permit(cid=user['_id'], otype=cls.__name__, oid=result, authority=15, desc='aduq', status=1, creator=user['_id'], updator=user['_id'], create_time=datetime.datetime.now())
            Permit.insert(permit)
        return result

    @classmethod
    def delete(cls, user, spec):
        if not user['group'] == 'administrator':
            spec['creator'] = user['_id']
        return super(AuthModel, cls).update(spec, {'$set':{'status':0}})

    @classmethod
    def update(cls, user, spec, doc):
        if spec.get('_id') is None:
            raise Exception("Wrong update condition without id.")
        auth = {'authority':0}
        if cls.__name__ == 'Creator':
            if not user['group'] == 'administrator':
                spec['creator'] = user['_id']
            doc['$set'] = doc.get('$set', {})
            doc['$set']['creator'] = spec['_id']
            doc['$set']['updator'] = user['_id']
            auth['authority'] = 2
            result = super(AuthModel, cls).update(spec, doc)
        elif cls.__name__ in ('Creator', 'Article', 'Task'):
            auth = Permit.queryOne({'cid':user['_id'], 'otype':cls.__name__, 'oid':spec['_id']}, projection={'authority':1}) or {'authority':0}
        else:
            auth['authority'] = 2
        if user['group'] == 'administrator' or auth['authority'] in (2,3,6,7,10,11,14,15):
            doc['$set'] = doc.get('$set', {})
            doc['$set']['updator'] = user['_id']
            result = super(AuthModel, cls).update(spec, doc)
        else:
            result = None
        return result


class Article(AuthModel):
    __table__ = 'grab_article'
    uid = baseorm.IdField(unique='ga')
    name = baseorm.StrField(ddl='varchar', max_length=20, nullable=0, updatable=False, unique='ga', searchable='end')
    desc = baseorm.StrField(ddl='char', max_length=128, searchable='in')
    clsname = baseorm.StrField(ddl='varchar', max_length=50, searchable='end')
    filepath = baseorm.StrField(ddl='varchar', max_length=64)
    digest = baseorm.StrField(ddl='char', max_length=32, default=None)
    status = baseorm.IntField(ddl='int', max_length=1)
    extra = baseorm.StrField(ddl='varchar', max_length=300, default=None)
    creator = baseorm.IdField(updatable=False)
    updator = baseorm.IdField()
    create_time = baseorm.DatetimeField(ddl='datetime', updatable=False)
    update_time = baseorm.DatetimeField(ddl='timestamp')


class Flow(AuthModel):
    __table__ = 'grab_flow'
    aid = baseorm.IdField()
    name = baseorm.StrField(ddl='varchar', max_length=20, nullable=0, updatable=False, unique='gf')
    desc = baseorm.StrField(ddl='varchar', max_length=128, default=None)
    status = baseorm.IntField(ddl='int', max_length=1)
    creator = baseorm.IdField(updatable=False)
    updator = baseorm.IdField()
    create_time = baseorm.DatetimeField(ddl='datetime', updatable=False)
    update_time = baseorm.DatetimeField(ddl='timestamp')


class Creator(AuthModel):
    __table__ = 'grab_creator'
    username = baseorm.StrField(ddl='varchar', max_length=20, nullable=0, updatable=False, unique='gc', searchable='in')
    password = baseorm.StrField(ddl='varchar', max_length=20)
    group = baseorm.StrField(ddl='varchar', max_length=20, searchable='all')
    desc = baseorm.StrField(ddl='varchar', max_length=128)
    avatar = baseorm.StrField(ddl='varchar', max_length=128)
    contact = baseorm.StrField(ddl='varchar', default=None, max_length=500)
    notify = baseorm.StrField(ddl='varchar', max_length=100)
    status = baseorm.IntField(ddl='int', max_length=1)
    extra = baseorm.StrField(ddl='varchar', max_length=300, default=None)
    secret = baseorm.StrField(ddl='varchar', max_length=100)
    creator = baseorm.IdField(updatable=False)
    updator = baseorm.IdField()
    create_time = baseorm.DatetimeField(ddl='datetime', updatable=False)
    update_time = baseorm.DatetimeField(ddl='timestamp')


class Datamodel(AuthModel):
    __table__ = 'grab_datamodel'
    name = baseorm.StrField(ddl='varchar', max_length=64, nullable=0, updatable=False, unique='gdm')
    table = baseorm.StrField(ddl='varchar', max_length=64)
    comment = baseorm.StrField(ddl='varchar', max_length=128)
    filepath = baseorm.StrField(ddl='varchar', max_length=64)
    digest = baseorm.StrField(ddl='char', max_length=32, default=None)
    status = baseorm.IntField(ddl='int', max_length=1)
    extra = baseorm.StrField(ddl='varchar', max_length=300, default=None)
    creator = baseorm.IdField(updatable=False)
    updator = baseorm.IdField()
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
    fid = baseorm.IdField(unique='gs')
    next_id = baseorm.IdField()
    name = baseorm.StrField(ddl='varchar', max_length=20, nullable=0, updatable=False, unique='gs')
    desc = baseorm.StrField(ddl='char', max_length=128)
    step = baseorm.IntField(ddl='int', max_length=2)
    flow = baseorm.StrField(ddl='varchar', max_length=20, nullable=0, updatable=False, unique='gs')
    index = baseorm.StrField(ddl='varchar', max_length=20)
    retry = baseorm.IntField(ddl='int', max_length=1)
    timelimit = baseorm.IntField(ddl='int', max_length=4)
    store = baseorm.IntField(ddl='int', max_length=1)
    additions = baseorm.StrField(ddl='varchar', max_length=1024, default=None)
    extra = baseorm.StrField(ddl='varchar', max_length=300, default=None)
    creator = baseorm.IdField(updatable=False)
    updator = baseorm.IdField()
    create_time = baseorm.DatetimeField(ddl='datetime', updatable=False)
    update_time = baseorm.DatetimeField(ddl='timestamp')


class Task(AuthModel):
    __table__ = 'grab_task'
    aid = baseorm.IdField()
    fid = baseorm.IdField()
    sid = baseorm.IdField()
    name = baseorm.StrField(ddl='varchar', max_length=50, searchable='in')
    params = baseorm.StrField(ddl='varchar', default=None, max_length=3000)
    worknum = baseorm.IntField(ddl='int', max_length=3)
    queuetype = baseorm.StrField(ddl='char', max_length=1)
    worktype = baseorm.StrField(ddl='varchar', max_length=30)
    timeout = baseorm.IntField(ddl='int', max_length=4)
    category = baseorm.StrField(ddl='varchar', max_length=50)
    tag = baseorm.StrField(ddl='varchar', default=None, max_length=500)
    type = baseorm.StrField(ddl='varchar', max_length=8)
    push_url = baseorm.StrField(ddl='varchar', max_length=100)
    period = baseorm.IntField(ddl='int', max_length=4)
    status = baseorm.IntField(ddl='int', default=1, max_length=1)
    state = baseorm.IntField(ddl='int', default=0, max_length=1)
    count = baseorm.IntField(ddl='int', max_length=5)
    extra = baseorm.StrField(ddl='varchar', max_length=300, default=None, searchable='in')
    creator = baseorm.IdField(updatable=False)
    updator = baseorm.IdField()
    create_time = baseorm.DatetimeField(ddl='datetime', updatable=False)
    update_time = baseorm.DatetimeField(ddl='timestamp')


class Unit(AuthModel):
    __table__ = 'grab_unit'
    dmid = baseorm.IdField()
    name = baseorm.StrField(ddl='varchar', max_length=20, nullable=0, updatable=False, unique='gu')
    desc = baseorm.StrField(ddl='char', max_length=128)
    filepath = baseorm.StrField(ddl='varchar', max_length=64)
    digest = baseorm.StrField(ddl='char', max_length=32, default=None)
    status = baseorm.IntField(ddl='int', max_length=1)
    extra = baseorm.StrField(ddl='varchar', max_length=300, default=None)
    creator = baseorm.IdField(updatable=False)
    updator = baseorm.IdField()
    create_time = baseorm.DatetimeField(ddl='datetime', updatable=False)
    update_time = baseorm.DatetimeField(ddl='timestamp')


if __name__ == '__main__':
    pass
    