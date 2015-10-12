#!/usr/bin/python
# coding=utf-8
import time, datetime, logging, threading, sys, traceback
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
            attributes['ddl'] = 'basestring'
        super(StrField, self).__init__(**attributes)

class IntField(Field):

    def __init__(self, **attributes):
        if not 'default' in attributes:
            attributes['default'] = 0
        if not 'ddl' in attributes:
            attributes['ddl'] = 'int'
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

class ListField(Field):

    def __init__(self, **attributes):
        if not 'default' in attributes:
            attributes['default'] = []
        if not 'ddl' in attributes:
            attributes['ddl'] = 'list'
        super(ListField, self).__init__(**attributes)

class DictField(Field):

    def __init__(self, **attributes):
        if not 'default' in attributes:
            attributes['default'] = {}
        if not 'ddl' in attributes:
            attributes['ddl'] = 'dict'
        super(DictField, self).__init__(**attributes)

_triggers = frozenset(['pre_insert', 'pre_update', 'pre_delete'])

def genDoc(tablename, tablefields):
    pk = None
    uniques = {}
    doc = []
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
        doc.append(nullable and '  "%s":"(%s)"' % (f.name, ddl) or '  "%s":"%s"' % (f.name, str(f.default)))
    return '-- generating DOC for %s: \n %s {\n' % (tablename, tablename) + ',\n'.join(doc) + '};'

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
    _insertdoc = None
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
    def queryOne(cls, **kwargs):
        '''
        Find by where clause and return one result. If multiple results found, 
        only the first one returned. If no result found, return None.
        '''
        d = dbpc.handler.queryOne(cls.__table__, **kwargs)
        return cls(**d) if d else None

    @classmethod
    def queryAll(cls, **kwargs):
        '''
        Find all and return list.
        '''
        L = dbpc.handler.queryAll(cls.__table__, **kwargs)
        return [cls(**d) for d in L]

    @classmethod
    def count(cls, **kwargs):
        '''
        Find by 'select count(pk) from table where ... ' and return int.
        '''
        return len(dbpc.handler.queryAll(cls.__table__, **kwargs))

    @classmethod
    def insert(cls, obj, update=True, method='SINGLE', forcexe=False, maxsize=MAXSIZE, lastid=None):
        if cls.__lock is None:
            cls.__lock = threading.Lock()
        if obj is not None and update:
            updatekeys = {}
            for k, v in obj.__mappings__.iteritems():
                if v.unique:
                    updatekeys[k] = obj[k]
            dbpc.handler.update(cls.__table__, {'cond':updatekeys, 'data':obj}, method)
        else:
            if method == 'SINGLE':
                try:
                    if obj:
                        dbpc.handler.insert(cls.__table__, obj, method)
                except:
                    t, v, b = sys.exc_info()
                    err_messages = traceback.format_exception(t, v, b)
                    print(': ', ','.join(err_messages), '\n')
            else:
                with cls.__lock:
                    if obj is not None:
                        cls._insertdatas.append(obj)
                    if forcexe:
                        try:
                            if cls._insertdatas:
                                dbpc.handler.insert(cls.__table__, cls._insertdatas, method)
                                cls._insertdatas = []
                        except:
                            t, v, b = sys.exc_info()
                            err_messages = traceback.format_exception(t, v, b)
                            print(': ', ','.join(err_messages), '\n')
                    else:
                        if sys.getsizeof(cls._insertdatas) > maxsize:
                            try:
                                dbpc.handler.insert(cls.__table__, cls._insertdatas, method)
                                cls._insertdatas = []
                            except:
                                t, v, b = sys.exc_info()
                                err_messages = traceback.format_exception(t, v, b)
                                print(': ', ','.join(err_messages), '\n')

    @classmethod
    def delete(cls, **kwargs):
        dbpc.handler.delete(cls.__table__, **kwargs)

    @classmethod
    def update(cls, **kwargs):
        dbpc.handler.update(cls.__table__, **kwargs)

if __name__=='__main__':
    pass
