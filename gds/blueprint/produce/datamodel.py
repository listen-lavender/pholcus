#!/usr/bin/python
# coding=utf8
import json
from datakit.mysql.suit import withMysql, dbpc, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from views import produce

@produce.route('/datamodel/list', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def modellist():
    datamodels = dbpc.handler.queryAll(""" select * from grab_datamodel; """)
    return render_template('pdatamodellist.html', appname=g.appname, logined=True, datamodels=datamodels)

@produce.route('/datamodel/detail/<dmid>', methods=['GET'])
@withMysql(WDB, resutype='DICT', autocommit=True)
def modeldetail(dmid=None):
    rows = ['id', 'name', 'extra']
    cols = ['id', 'dmid', 'name', 'length', 'default']
    # rows = ['id', 'name', 'comment', 'autocreate', 'iscreated', 'status', 'extra', 'creator', 'updator', 'create_time', 'update_time']
    # cols = ['id', 'dmid', 'name', 'comment', 'default', 'nullable', 'unique']
    adds = ['ditype','ddl']
    rowvals = dbpc.handler.queryOne(""" select {{s}} from grab_datamodel where id = %s """.replace("{{s}}", ','.join(''.join(('`', one, '`')) for one in rows)), (dmid or '', )) or dict(zip(rows, ['' for one in rows]))
    print rowvals
    colvals = dbpc.handler.queryAll(""" select {{s}} from grab_dataitem where dmid = %s; """.replace("{{s}}", ','.join(''.join(('`', one, '`')) for one in cols)), (rowvals['id'], ))
    for col in colvals:
        # colvals[col]['datatypes'] = dbpc.handler.queryAll(""" select %s from grab_datatype where diid = %s; """, (','.join(''.join(('`', one, '`')) for one in adds), colvals[col]['id']))
        del col['dmid']
    cols.remove('dmid')
    cols.remove('id')
    rows.remove('id')
    return render_template('pdatamodeldetail.html', appname=g.appname, logined=True, rows=rows, cols=cols, rowvals=unicode2utf8(rowvals), colvals=unicode2utf8(colvals), colspan=len(cols)-1)
