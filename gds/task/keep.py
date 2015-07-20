#!/usr/bin/python
# coding=utf-8
import sys
import functools
import datetime
import traceback

import threading
from task.config.db.mysql import RDB, WDB, LIMIT, _DBCONN, USE
from multilog.aboutfile import modulename, modulepath
from multilog.prettyprint import logprint

from datakit.mysql.suit import withMysql, dbpc as msdbpc
from datakit.mongo.suit import withMongo, dbpc as mgdbpc
from webcrawl.work import dispatch

_print, logger = logprint(modulename(__file__), modulepath(__file__))

MAXSIZE = 1000

class Keeper(object):
    """
        Store receiving datas.
    """
    def __init__(self):
        if not hasattr(self, 'clsname'):
            self.clsname = str(self.__class__).split(".")[-1].replace("'>", "")
        self.__lock = threading.Lock()
        self.strorage = {}
        self.onway = None
        msdbpc.addDB(RDB, LIMIT, host=_DBCONN[USE]['host'],
                    port=_DBCONN[USE]['port'],
                    user=_DBCONN[USE]['user'],
                    passwd=_DBCONN[USE]['passwd'],
                    db=_DBCONN[USE]['db'],
                    charset=_DBCONN[USE]['charset'],
                    use_unicode=_DBCONN[USE]['use_unicode'],
                    override=False)
        msdbpc.addDB(WDB, LIMIT, host=_DBCONN[USE]['host'],
                    port=_DBCONN[USE]['port'],
                    user=_DBCONN[USE]['user'],
                    passwd=_DBCONN[USE]['passwd'],
                    db=_DBCONN[USE]['db'],
                    charset=_DBCONN[USE]['charset'],
                    use_unicode=_DBCONN[USE]['use_unicode'],
                    override=False)
        mgdbpc.addDB(RDB, 10, host="127.0.0.1",
            port=27017,
            db="kuaijie")
        mgdbpc.addDB(WDB, 10, host="127.0.0.1",
            port=27017,
            db="kuaijie")
        # msdbpc = DBPoolCollector(DBHandler, delegate=True)

    # @dispatch(True)
    # def store(self, source, belong, template=''):
    #     source = self.clsname + ':' + source
    #     self.strorage[source] = {'datas':[], 'template':template}
    #     self.onway = {'mysql':functools.partial(self.toMysql, source=source, exemethod='MANY'),
    #                   'mongo':functools.partial(self.toMongo, source=source, exemethod='MANY'),
    #                   'file':functools.partial(self.toFile, source=source, exemethod='MANY'),
    #                   'console':functools.partial(self.toConsole, source=source, exemethod='MANY')}[belong.lower()]
    #     self.onway.__name__ = {'mysql':'toMysql', 
    #                            'mongo':'toMongo',
    #                            'file':'toFile',
    #                            'console':'toConsole'}[belong.lower()]
    #     return self.onway

    @withMysql(WDB)
    def toMysql(self, one, source, exemethod='SINGLE', forcexe=False, maxsize=MAXSIZE):
        """
            抓取的酒店数据入库
            @param hotel: 一条数据
            @param exemethod: 执行方式SINGLE, MANY
            @param forcexe: 是否强制执行MANY
            @param maxsize: MANY方式的SQL缓冲容量
            @return : 插入行数
        """
        if exemethod == 'SINGLE':
            try:
                msdbpc.handler.insert(self.strorage[source]['template'], one, exemethod)
                msdbpc.handler.commit()
            except:
                t, v, b = sys.exc_info()
                err_messages = traceback.format_exception(t, v, b)
                _print(source, ': ', ','.join(err_messages), '\n')
                msdbpc.handler.rollback()
        else:
            with self.__lock:
                if one is not None:
                    self.strorage[source]['datas'].append(one)
                if forcexe:
                    try:
                        msdbpc.handler.insert(self.strorage[source]['template'], self.strorage[source]['datas'], exemethod)
                        msdbpc.handler.commit()
                        self.strorage[source]['datas'] = []
                    except:
                        t, v, b = sys.exc_info()
                        err_messages = traceback.format_exception(t, v, b)
                        _print(source, ': ', ','.join(err_messages), '\n')
                        msdbpc.handler.rollback()
                else:
                    if sys.getsizeof(self.strorage[source]['datas']) > maxsize:
                        try:
                            msdbpc.handler.insert(self.strorage[source]['template'], self.strorage[source]['datas'], exemethod)
                            msdbpc.handler.commit()
                            self.strorage[source]['datas'] = []
                        except:
                            t, v, b = sys.exc_info()
                            err_messages = traceback.format_exception(t, v, b)
                            _print(source, ': ', ','.join(err_messages), '\n')
                            msdbpc.handler.rollback()
                        

    @withMongo(WDB)
    def toMongo(self, one, source, exemethod='SINGLE', forcexe=False, maxsize=MAXSIZE):
        """
            抓取的酒店数据入库
            @param hotel: 一条数据
            @param exemethod: 执行方式SINGLE, MANY
            @param forcexe: 是否强制执行MANY
            @param maxsize: MANY方式的SQL缓冲容量
            @return : 插入行数
        """
        if exemethod == 'SINGLE':
            try:
                mgdbpc.handler.insert(self.strorage[source]['template'], one, exemethod)
            except:
                t, v, b = sys.exc_info()
                err_messages = traceback.format_exception(t, v, b)
                _print(source, ': ', ','.join(err_messages), '\n')
        else:
            with self.__lock:
                if one is not None:
                    self.strorage[source]['datas'].append(one)
                if forcexe:
                    try:
                        mgdbpc.handler.insert(self.strorage[source]['template'], self.strorage[source]['datas'], exemethod)
                        self.strorage[source]['datas'] = []
                    except:
                        t, v, b = sys.exc_info()
                        err_messages = traceback.format_exception(t, v, b)
                        _print(source, ': ', ','.join(err_messages), '\n')
                else:
                    if sys.getsizeof(self.strorage[source]['datas']) > maxsize:
                        try:
                            mgdbpc.handler.insert(self.strorage[source]['template'], self.strorage[source]['datas'], exemethod)
                            self.strorage[source]['datas'] = []
                        except:
                            t, v, b = sys.exc_info()
                            err_messages = traceback.format_exception(t, v, b)
                            _print(source, ': ', ','.join(err_messages), '\n')

    def toFile(self, one, source, exemethod='SINGLE', forcexe=False, maxsize=MAXSIZE):
        """
            抓取的酒店数据入库
            @param hotel: 一条数据
            @param exemethod: 执行方式SINGLE, MANY
            @param forcexe: 是否强制执行MANY
            @param maxsize: MANY方式的SQL缓冲容量
            @return : 插入行数
        """
        if exemethod == 'SINGLE':
            pass
        else:
            if one is not None:
                self.strorage[source]['datas'].append(one)
            if forcexe:
                with self.__lock:
                    self.strorage[source]['datas'] = []
            else:
                if sys.getsizeof(self.strorage[source]['datas']) > maxsize:
                    with self.__lock:
                        self.strorage[source]['datas'] = []

    def toConsole(self, one, source, exemethod='SINGLE', forcexe=False, maxsize=MAXSIZE):
        """
            抓取的酒店数据入库
            @param hotel: 一条数据
            @param exemethod: 执行方式SINGLE, MANY
            @param forcexe: 是否强制执行MANY
            @param maxsize: MANY方式的SQL缓冲容量
            @return : 插入行数
        """
        if exemethod == 'SINGLE':
            pass
        else:
            if one is not None:
                self.strorage[source]['datas'].append(one)
            if forcexe:
                with self.__lock:
                    self.strorage[source]['datas'] = []
            else:
                if sys.getsizeof(self.strorage[source]['datas']) > maxsize:
                    with self.__lock:
                        self.strorage[source]['datas'] = []
    @withMysql(WDB)
    def lasttime(self):
        t = msdbpc.handler.queryOne(" select max(create_time) as create_time from official_hotel_info ")
        if t and t[0]:
            return t[0]
        else:
            return datetime.datetime.strptime('1949-10-01 00:00:00', '%Y-%m-%d %H:%M:%S')

    def __del__(self):
        pass

if __name__ == '__main__':
    pass
