#!/usr/bin/python
# coding=utf-8
import time, logging, threading, sys, traceback
from suit import dbpc
MAXSIZE = 20
class Field(object):
    _count = 0
    def __init__(self, **attributes):
        self.name = attributes.get('name', None)
        self.ddl = attributes.get('ddl', None)
        self.default = attributes.get('default', None)
        self.comment = attributes.get('comment', None)
        self.nullable = attributes.get('nullable', 1)
        self.unique = attributes.get('unique', None)
        self.insertable = attributes.get('insertable', True)
        self.deleteable = attributes.get('deleteable', True)
        self.updatable = attributes.get('updatable', True)
        self.queryable = attributes.get('queryable', True)
        Field._count += 1
        self.order = Field._count

    # def __get__(self, obj, cls):
    #     return obj[self.name]
        
    # def __set__(self, obj, value):
    #     obj[self.name] = value

    def selfexamine(self):
        if not self.name:
            raise "No field name"
        if 'creator' in self.name or ('create' in self.name and 'time' in self.name):
            self.deleteable = False
            self.updatable = False
        if not self.ddl:
            raise "No field ddl"
        if self.ddl == 'timestamp':
            self.insertable = False
            self.deleteable = False
            self.updatable = False
            self.default = 'current_timestamp on update current_timestamp'
        if self.unique:
            self.nullable = 0
            self.updatable = False

    def __str__(self):
        s = ['<%s:%s,%s,default(%s)' % (self.__class__.__name__, self.name or 'None', self.ddl or 'None', self.default or 'None')]
        # self.nullable and s.append('N')
        self.insertable and s.append('I')
        self.deleteable and s.append('D')
        self.updatable and s.append('U')
        self.queryable and s.append('Q')
        s.append('>')
        self.comment and s.append(self.comment or '')
        return ''.join(s)

class StrField(Field):

    def __init__(self, **attributes):
        if not 'default' in attributes:
            attributes['default'] = ''
        if not 'ddl' in attributes:
            attributes['ddl'] = 'varchar(255)'
        super(StrField, self).__init__(**attributes)

class IntField(Field):

    def __init__(self, **attributes):
        if not 'default' in attributes:
            attributes['default'] = 0
        if not 'ddl' in attributes:
            attributes['ddl'] = 'bigint'
        super(IntField, self).__init__(**attributes)

class FloatField(Field):

    def __init__(self, **attributes):
        if not 'default' in attributes:
            attributes['default'] = 0.0
        if not 'ddl' in attributes:
            attributes['ddl'] = 'float'
        super(FloatField, self).__init__(**attributes)

class BoolField(Field):

    def __init__(self, **attributes):
        if not 'default' in attributes:
            attributes['default'] = False
        if not 'ddl' in attributes:
            attributes['ddl'] = 'bool'
        super(BoolField, self).__init__(**attributes)

class TextField(Field):

    def __init__(self, **attributes):
        if not 'default' in attributes:
            attributes['default'] = ''
        if not 'ddl' in attributes:
            attributes['ddl'] = 'text'
        super(TextField, self).__init__(**attributes)

class BlobField(Field):

    def __init__(self, **attributes):
        if not 'default' in attributes:
            attributes['default'] = ''
        if not 'ddl' in attributes:
            attributes['ddl'] = 'blob'
        super(BlobField, self).__init__(**attributes)

class DatetimeField(Field):

    def __init__(self, **attributes):
        if not 'default' in attributes:
            attributes['default'] = datetime.datetime.now()
        if not 'ddl' in attributes:
            attributes['ddl'] = 'datetime'
        super(DatetimeField, self).__init__(**attributes)

class VersionField(Field):

    def __init__(self, name=None):
        super(VersionField, self).__init__(name=name, default=0, ddl='bigint')

_triggers = frozenset(['pre_insert', 'pre_update', 'pre_delete'])

def genDoc(tablename, tablefields):
    pk = None
    uniques = {}
    doc = ['-- generating DOC for %s:' % tablename, 'create table if not exists `%s` (' % tablename]
    doc.append('`id` int(11) not null auto_increment,')
    for f in sorted(tablefields.values(), lambda x, y: cmp(x.order, y.order)):
        if not hasattr(f, 'ddl'):
            raise StandardError('no ddl in field "%s".' % n)
        ddl = f.ddl
        nullable = f.nullable
        if f.unique:
            if f.unique in uniques:
                uniques[f.unique].append(f.name)
            else:
                uniques[f.unique] = [f.name]
        doc.append(nullable and '  `%s` %s,' % (f.name, ddl) or '  `%s` %s not null default %s,' % (f.name, ddl, f.default))
    if uniques:
        doc.append('  primary key (`id`),')
        doc.append(',\n'.join('  unique key `%s` (%s)' % (key, ','.join('`'+one+'`' for one in val)) for key, val in uniques.items()))
    else:
        doc.append('  primary key (`id`)')
    doc.append(');')
    return '\n'.join(doc)

class ModelMetaclass(type):
    '''
    Metaclass for model objects.
    '''
    def __new__(cls, name, bases, attrs):
        # skip base Model class:
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)

        # store all subclasses info:
        if not hasattr(cls, 'subclasses'):
            cls.subclasses = {}
        if not name in cls.subclasses:
            cls.subclasses[name] = name
        else:
            logging.warning('Redefine class: %s' % name)

        logging.info('Scan ORMapping %s...' % name)
        mappings = dict()
        for k, v in attrs.iteritems():
            if isinstance(v, Field):
                if not v.name:
                    v.name = k
                logging.info('Found mapping: %s => %s' % (k, v))
                mappings[k] = v
        for k in mappings.iterkeys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings
        cls.genDoc = lambda self: genDoc(attrs['__table__'], mappings)
        return type.__new__(cls, name, bases, attrs)

class Model(dict):
    __table__ = None
    __metaclass__ = ModelMetaclass
    _insertsql = None
    _insertdatas = []
    __lock = None

    def __init__(self, **attributes):
        if 'id' in attributes:
            del attributes['id']
        
        super(Model, self).__init__(**attributes)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    @classmethod
    def queryOne(cls, where, *args):
        '''
        Find by where clause and return one result. If multiple results found, 
        only the first one returned. If no result found, return None.
        '''
        d = dbpc.handler.queryOne('select * from `%s` %s' % (cls.__table__, where), *args)
        return cls(**d) if d else None

    @classmethod
    def queryAll(cls, where, *args):
        '''
        Find all and return list.
        '''
        L = dbpc.handler.queryAll('select * from `%s` %s' % (cls.__table__, where), *args)
        return [cls(**d) for d in L]

    @classmethod
    def count(cls, where, *args):
        '''
        Find by 'select count(pk) from table where ... ' and return int.
        '''
        return len(dbpc.handler.queryAll('select id from `%s` %s' % (cls.__table__, where), *args))

    @classmethod
    def insert(cls, obj, update=True, method='SINGLE', forcexe=False, maxsize=MAXSIZE, lastid=None):
        if cls.__lock is None:
            cls.__lock = threading.Lock()
        if obj is not None:
            updatekeys = []
            for k, v in obj.__mappings__.iteritems():
                if v.insertable:
                    if not hasattr(obj, k):
                        setattr(obj, k, v.default)
                if update:
                    if v.updatable:
                        updatekeys.append(k)
            items = obj.items()
            items.sort(lambda x,y:cmp(x[0], y[0]))
            if cls._insertsql is None or method == 'SINGLE':
                if update:
                    cls._insertsql = 'insert into `%s` (%s) ' % (cls.__table__, ','.join('`'+one[0]+'`' for one in items)) + 'values (%s)' % ','.join('%s' for one in items) + ' on duplicate key update %s' % ','.join('`'+one+'`=values(`'+one+'`)' for one in updatekeys)
                else:
                    cls._insertsql = 'insert ignore into `%s` (%s) ' % (cls.__table__, ','.join('`'+one[0]+'`' for one in items)) + 'values (%s)' % ','.join('%s' for one in items)
            one = tuple([i[1] for i in items])
        else:
            one = None
        if method == 'SINGLE':
            if one:
                try:
                    dbpc.handler.insert(cls._insertsql, one, method)
                    dbpc.handler.commit()
                except:
                    t, v, b = sys.exc_info()
                    err_messages = traceback.format_exception(t, v, b)
                    print(': ', ','.join(err_messages), '\n')
                    dbpc.handler.rollback()
        else:
            with cls.__lock:
                if one is not None:
                    cls._insertdatas.append(one)
                if forcexe:
                    try:
                        if cls._insertdatas:
                            dbpc.handler.insert(cls._insertsql, cls._insertdatas, method)
                            dbpc.handler.commit()
                            cls._insertdatas = []
                    except:
                        t, v, b = sys.exc_info()
                        err_messages = traceback.format_exception(t, v, b)
                        print(': ', ','.join(err_messages), '\n')
                        dbpc.handler.rollback()
                else:
                    if sys.getsizeof(cls._insertdatas) > maxsize:
                        try:
                            dbpc.handler.insert(cls._insertsql, cls._insertdatas, method)
                            dbpc.handler.commit()
                            cls._insertdatas = []
                        except:
                            t, v, b = sys.exc_info()
                            err_messages = traceback.format_exception(t, v, b)
                            print(': ', ','.join(err_messages), '\n')
                            dbpc.handler.rollback()

    @classmethod
    def delete(cls, where, *args):
        dbpc.handler.delete('select id from `%s` %s' % (cls.__table__, where), *args)

    @classmethod
    def update(cls, where, *args, **kwargs):
        items = kwargs.items()
        dbpc.handler.update('update `%s` set %s %s' % (cls.__table__, ','.join('`'+one[0]+'`=%s' for one in items), where), tuple(list(*args)+[one[1] for one in items]))

if __name__=='__main__':
    pass
