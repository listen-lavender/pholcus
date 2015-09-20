#!/usr/bin/python
# coding=utf-8

import pymongo as dblib

class DBHandler(object):
    def __init__(self, markname, conn, check=(lambda tips, data:data), resutype='DICT', autocommit=False, db=''):
        self._markname = markname
        self._conn = conn
        self._check = check
        self._resutype = {'TUPLE':'TUPLE', 'DICT':'DICT'}[resutype]
        self.db = db

    @classmethod
    def wrap(cls, tpl):
        if type(tpl) == dict:
            tpl['tips'] = tpl.get('tips')
        else:
            tpl = {'collection':tpl, 'tips':None}
        return tpl
    
    def check(self, tips, data):
    	return self._check(tips, data)

    def queryAll(self, tpl, data=None):
        tpl = DBHandler.wrap(tpl)
        return self._conn[self.db][tpl['collection']].find(self.check(tpl['tips'], data))

    def queryOne(self, tpl, data=None):
        tpl = DBHandler.wrap(tpl)
        return self._conn[self.db][tpl['collection']].find_one(self.check(tpl['tips'], data))

    def query(self, tpl, data=None, qt='all'):
        tpl = DBHandler.wrap(tpl)
        if qt.lower() == 'one':
            return self._conn[self.db][tpl['collection']].find_one(self.check(tpl['tips'], data))
        else:
            return self._conn[self.db][tpl['collection']].find(self.check(tpl['tips'], data))

    def update(self, tpl, data=None, method='SINGLE'):
        tpl = DBHandler.wrap(tpl)
        return self._conn[self.db][tpl['collection']].update(data['cond'], self.check(tpl['tips'], data['data']), upsert=True)

    def delete(self, tpl, data=None, method='SINGLE'):
        tpl = DBHandler.wrap(tpl)
        return self._conn[self.db][tpl['collection']].remove(self.check(tpl['tips'], data))

    def insert(self, tpl, data=None, method='SINGLE', lastid=None):
        tpl = DBHandler.wrap(tpl)
        if method == 'SINGLE':
            return self._conn[self.db][tpl['collection']].insert_one(self.check(tpl['tips'], data)).inserted_id
        else:
            return self._conn[self.db][tpl['collection']].insert_many(self.check(tpl['tips'], data)).inserted_ids

    def showColumns(self, table):
        """
            查看表的列
            @param table: 表名称
            @return columns: 列名
        """
        sql = """ select `column_name`, `data_type`
                    from information_schema.columns
                where `table_schema` = %s and `table_name`=%s
        """
        columns = {}
        tables = self._conn[self.db][table].find_one()
        if tables:
            for key, val in tables.items():
                columns[key] = type(val)
        return columns

class ExampleDBHandler(DBHandler):
    pass
