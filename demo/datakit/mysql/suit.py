#!/usr/bin/python
# coding=utf-8

import time
import functools
import threading
import Queue
threading.queue = Queue
import weakref
import traceback
import sys

import handler
from error import ConnectionNotInPoolError, \
                  ConnectionPoolOverLoadError, \
                  ClassAttrNameConflictError, \
                  ConnectionNotFoundError, \
                  ConnectionNameConflictError

RDB = 'rdb'
WDB = 'wdb'
MINLIMIT = 10
MAXLIMIT = 40
customattrs = lambda cls:[attr for attr in dir(cls) if not attr.startswith('_')]

def singleton(cls):
    instances = {}
    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _singleton

class DBConnect(handler.DBHandler):

    def __init__(self, settings, autocommit=False, resutype='TUPLE'):
        super(DBConnect, self).__init__('', handler.dblib.connect(**settings), resutype=resutype, autocommit=autocommit)

class DBPool(object):

    def __init__(self, markname, minlimit=MINLIMIT, maxlimit=MAXLIMIT, **settings):
        self.markname = markname
        self.minlimit = minlimit
        self.maxlimit = maxlimit
        self.settings = settings
        self._lock = threading.Lock()
        self.queue = threading.queue.Queue(self.maxlimit)
        self._openconnects = []
        self._liveconnects = 0
        self._peakconnects = 0

    def __repr__(self):
        return "<%s::%s>" % (self.__class__.__name__, self.markname)

    @property
    def alive(self):
        return self._liveconnects

    @property
    def peak(self):
        return self._peakconnects

    def clearIdle(self):
        while self.queue.qsize() > self.minlimit:
            connect = self.queue.get()
            connect.close()
            del connect
            with self._lock:
                self._liveconnects -= 1

    def connect(self):
        if self.queue.empty():
            with self._lock:
                if self._liveconnects >= self.maxlimit:
                    raise ConnectionPoolOverLoadError("Connections of %s reach limit!" % self.__repr__())
                else:
                    self.queue.put(handler.dblib.connect(**self.settings))
                    self._liveconnects += 1
                connect = self.queue.get()
        else:
            try:
                connect = self.queue.get()
                connect.ping()
            except:
                del connect
                connect = handler.dblib.connect(**self.settings)
        self._appendOpenconnect(connect)
        return connect

    def release(self, conn):
        self._removeOpenconnect(conn)
        with self._lock:
            try:
                conn.rollback()
            except handler.dblib.OperationalError:
                print "connection seems closed, drop it."
            else:
                self.queue.put(conn)
            finally:
                pass
        self.clearIdle()

    def _appendOpenconnect(self, conn):
        with self._lock:
            self._openconnects.append(conn)
            if self._peakconnects < len(self._openconnects):
                self._peakconnects = len(self._openconnects)

    def _removeOpenconnect(self, conn):
        with self._lock:
            try:
                self._openconnects.remove(conn)
            except Exception:
                raise ConnectionNotInPoolError("Connection seems not belong to %s" % self.__repr__())

@singleton
class DBPoolCollector(object):

    def __init__(self, handler=None, delegate=False):
        """
        Global DBPoolCollector with specific connection handler,
        call DBPoolCollector.connect to passing the mysql connection to this handler
        and use DBPoolCollector.db access
        current database connection wrapper class.
        :param handler:
        :return:
        """
        self._handler = handler
        self._collection = {}
        # self._instance_lock = threading.Lock()
        self._current = None
        # self._lock = threading.Lock()
        # the queue stores available handler instance
        # with self._instance_lock:
        #     self._instance = self
        self.setDelegate(delegate)

    def __getattr__(self, attr):
        if not self._delegate or (attr.startswith('_') or not hasattr(self._current,"handler")):
            return self.__getattribute__(attr)
        else:
            return getattr(self._current.handler, attr)

    def setDelegate(self, delegate):
        if delegate:
            if set(customattrs(self._handler)).intersection(set(customattrs(self))):
                raise ClassAttrNameConflictError("If open delegate, ConnectionHandler's attr name should not appear in DBPoolCollector")
            self._delegate = True
        else:
            self._delegate = False

    def addDB(self, markname, minlimit=MINLIMIT, maxlimit=MAXLIMIT, **settings):
        """
        :param markname: string database name
        :param settings: connection kwargs
        :return:
        """
        if self._current is None:
            self._current = threading.local()
            self._current.connect = None
            self._current.markname = None
            self._current.handler = None
        override = settings.pop("override", False)
        if not override and self._collection.has_key(markname):
            msg = "Alreay exist connection '%s',override or rename it." % markname
            print msg
            # raise ConnectionNameConflictError(msg)
        else:
            self._collection[markname] = DBPool(markname, minlimit, maxlimit, **settings)

    def deleteDB(self, markname):
        """
        :param markname: string database name
        """
        if self._current.markname == markname:
            self.release()
        if hasattr(self._collection, markname):
            del self._collection[markname]


    def connect(self, markname, resutype='TUPLE', autocommit=False):
        """
        Mapping current connection handler's method to DBPoolCollector
        :return:
        """
        if not hasattr(self._current, "connect") or self._current.connect is None:
            self._current.connect = self._collection[markname].connect()
            self._current.markname = markname
            self._current.handler = handler.DBHandler(markname, self._current.connect, resutype=resutype, autocommit=autocommit, db=self._collection[markname].settings['db'])
            self._current.connect._cursor = weakref.proxy(self._current.handler._curs)
        else:
            try:
                self._current.connect.ping()
                if handler.dbtype == 1:
                    self._current.handler._curs._connection = weakref.proxy(self._current.connect)
                else:
                    self._current.handler._curs.connection = weakref.proxy(self._current.connect)
            except:
                self._current.connect = handler.dblib.connect(**self._collection[markname].settings)
                self._current.handler = self._handler(markname, self._current.connect, resutype=resutype, autocommit=autocommit, db=self._collection[markname].settings['db'])
            self._current.connect._cursor = weakref.proxy(self._current.handler._curs)
            # raise AlreadyConnectedError("Database:'%s' is already connected !" % markname)

    def release(self):
        """
        :return:
        """
        # print "start...", self._current.markname, self._current.connect
        if hasattr(self._current, 'connect') and self._current.connect is not None:
            self._collection[self._current.markname].release(self._current.connect)
            del self._current.handler, self._current.connect
        # print "end..."

    @property
    def handler(self):
        if hasattr(self._current, 'handler') and self._current.handler is not None:
            return weakref.proxy(self._current.handler)
        else:
            return None
            

    # @staticmethod
    # def instance():
    #     if not hasattr(DBPoolCollector, "_instance"):
    #         with DBPoolCollector._instance_lock:
    #             if not hasattr(DBPoolCollector, "_instance"):
    #                 DBPoolCollector._instance = DBPoolCollector()
    #     return DBPoolCollector._instance

dbpc = DBPoolCollector(handler.DBHandler, delegate=True)
# dbpc = None

def withMysql(markname, resutype='TUPLE', autocommit=False):
    """
    :param markname:
    :return:the decorator with specific db connection
    """
    def wrapped(fun):
        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            if not dbpc._collection.has_key(markname):
                raise ConnectionNotFoundError("Not found connection for '%s', use dbpc.addDB add the connection")
            if dbpc.handler is None:
                dbpc.connect(markname, resutype=resutype, autocommit=autocommit)
            try:
                res = fun(*args, **kwargs)
            except:
                t, v, b = sys.exc_info()
                err_messages = traceback.format_exception(t, v, b)
                print ('Business error: %s' % ','.join(err_messages))
                res = None
            finally:
                dbpc.release()
            return res
        return wrapper
    return wrapped

@withMysql(RDB, resutype='DICT')
def withMysqlQuery(sql, data=None, qt='all'):
    """
    :param markname:
    :return:the decorator with specific db connection
    """
    return dbpc.handler.query(sql, data, qt)

@withMysql(WDB, autocommit=True)
def withMysqlInsert(sql, data=None, method='SINGLE'):
    """
    :param markname:
    :return:the decorator with specific db connection
    """
    return dbpc.handler.insert(sql, data, method)

@withMysql(WDB, autocommit=True)
def withMysqlDelete(sql, data=None, method='SINGLE'):
    """
    :param markname:
    :return:the decorator with specific db connection
    """
    return dbpc.handler.delete(sql, data, method)

@withMysql(WDB, autocommit=True)
def withMysqlUpdate(sql, data=None, method='SINGLE'):
    """
    :param markname:
    :return:the decorator with specific db connection
    """
    return dbpc.handler.update(sql, data, method)

if __name__ == "__main__":

    dbpc.addDB("local", 1, host="127.0.0.1",
                    port=3306,
                    user="root",
                    passwd="",
                    db="kuaijie",
                    charset="utf8",
                    use_unicode=False,
                    override=False)

    @withMysql('local')
    def test1():
        for one in dbpc.handler.showColumns('hotel_info_collection'):
            # print ''
            pass

    @withMysql('local')
    def test2():
        for one in dbpc.handler.showColumns('hotel_info_original'):
            # print ''
            pass

    @withMysql('local')
    def test3():
        for one in dbpc.handler.showColumns('hotel_info_mapping'):
            pass
            # print ''

    from threading import Thread
    a = Thread(target=test1)
    b = Thread(target=test2)
    c = Thread(target=test3)
    a.start()
    # a.join()
    b.start()
    # b.join()
    c.start()
    # c.join()
    a.join()
    b.join()
    c.join()




