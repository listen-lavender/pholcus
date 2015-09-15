#!/usr/bin/python
# coding=utf-8

try:
    import mysql.connector as dblib
    dbtype = 1
    class MySQLCursorDict(dblib.cursor.MySQLCursor):
        def _row_to_python(self, rowdata, desc=None):
            row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
            if row:
                return dict(zip(self.column_names, row))
            return None
    print "use mysql.connector."
except:
    print "use MySQLdb."
    try:
        import MySQLdb as dblib
        dbtype = 0
    except:
        raise "No database libary available."

class DBHandler(object):
    def __init__(self, markname, conn, curs=None, resutype='TUPLE', autocommit=False, db=''):
        self._markname = markname
        self._conn = conn
        try:
            self._resutype = {'TUPLE':'TUPLE', 'DICT':'DICT'}[resutype]
        except:
            raise 'result type error, you must choose TUPLE or DICT.'
        if curs:
            self._curs = curs
        else:
            if self._resutype == 'TUPLE':
                self._curs = conn.cursor()
            else:
                if dbtype:
                    self._curs = conn.cursor(cursor_class=MySQLCursorDict)
                else:
                    self._curs = conn.cursor(dblib.cursors.DictCursor)
            if dbtype:
                self._conn.autocommit = autocommit
            else:
                self._conn.autocommit(autocommit)
        self.db = db

    def __del__(self):
        self._curs.close()
        del self._conn, self._curs

    def operate(self, sql, data, method='SINGLE'):
        """
            操作数据
            @param sql:
            @param data: 数据
            @param method: 执行方式SINGLE, MANY
            @return : 影响行数
        """
        try:
            method = {'SINGLE':'SINGLE', 'MANY':'MANY'}[method]
        except:
            raise 'executing method error, you must choose SINGLE or MANY.'
        if method == 'SINGLE':
            num = self._curs.execute(sql, data)
        else: # MANY
            num = self._curs.executemany(sql, data)
        return num

    def queryAll(self, sql, data=None):
        self._curs.execute(sql, data)
        return self._curs.fetchall()

    def queryOne(self, sql, data=None):
        self._curs.execute(sql, data)
        return self._curs.fetchone()

    def query(self, sql, data=None, qt='all'):
        self._curs.execute(sql, data)
        if qt.lower() == 'one':
            return self._curs.fetchone()
        else:
            return self._curs.fetchall()

    def update(self, sql, data=None, method='SINGLE'):
        return self.operate(sql, data, method=method)

    def delete(self, sql, data=None, method='SINGLE'):
        return self.operate(sql, data, method=method)

    def insert(self, sql, data=None, method='SINGLE', lastid=None):
        if lastid == 'CURS':
            return (self.operate(sql, data, method=method), int(self._curs.lastrowid))
        elif lastid == 'CONN':
            return (self.operate(sql, data, method=method), int(self._conn.insert_id()))
        else:
            return self.operate(sql, data, method=method)

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
        tables = self.queryAll(sql, (self.db, table))
        usetype = {'DICT':{'column_name':'column_name', 'data_type':'data_type'}, 'TUPLE':{'column_name':0, 'data_type':1}}[self._resutype]
        for col in tables:
            colname = str(col[usetype['column_name']])
            coltype = str(col[usetype['data_type']])
            if 'int' in coltype.lower():
                columns[colname] = int
            elif 'double' in coltype or 'float' in coltype:
                columns[colname] = float
            else:
                columns[colname] = str
        return columns

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

class ExampleDBHandler(DBHandler):
    pass
