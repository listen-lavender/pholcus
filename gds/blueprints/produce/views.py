#!/usr/bin/python
# coding=utf8
from datakit.mysql.suit import withMysql, dbpc, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template

produce = Blueprint('produce', __name__, template_folder='templates')

model = {}

@produce.route('/datamodel/list', methods=['GET'])
@withMysql(RDB, methods=['GET'])
def modellist():
    datamodels = dbpc.handler.queryAll(""" select * from grabtask_datamodel; """)
    return render_template('datamodellist.html')

@produce.route('/datamodel/detail/<dmid>', methods=['GET', 'POST'])
@withMysql(RDB, resutype='DICT')
def modeldetail(dmid):
    rows = ['id', 'name', 'autocreate', 'iscreated', 'status', 'extra', 'creator', 'updator', 'create_time', 'update_time']
    cols = ['id', 'dmid', 'name', 'default', 'nullable', 'unique']
    # rows = ['id', 'name', 'comment', 'autocreate', 'iscreated', 'status', 'extra', 'creator', 'updator', 'create_time', 'update_time']
    # cols = ['id', 'dmid', 'name', 'comment', 'default', 'nullable', 'unique']
    adds = ['ditype','ddl']
    rowvals = dbpc.handler.queryOne(""" select {{s}} from grabtask_datamodel where id = %s """.replace("{{s}}", ','.join(''.join(('`', one, '`')) for one in rows)), (dmid or '', )) or dict(zip(rows, ['' for one in rows]))
    colvals = dbpc.handler.queryAll(""" select {{s}} from grabtask_dataitem where dmid = %s; """.replace("{{s}}", ','.join(''.join(('`', one, '`')) for one in cols)), (rowvals['id'], ))
    for col in colvals:
        # colvals[col]['datatypes'] = dbpc.handler.queryAll(""" select %s from grabtask_datatype where diid = %s; """, (','.join(''.join(('`', one, '`')) for one in adds), colvals[col]['id']))
        del col['dmid']
    cols.remove('dmid')
    cols.remove('id')
    rows.remove('id')
    return render_template('datamodeldetail.html', rows=rows, cols=cols, rowvals=unicode2utf8(rowvals), colvals=unicode2utf8(colvals), colspan=len(cols)-1)

@produce.route('/task/unit', methods=['GET'])
def unit():
    return render_template('unit.html')

@produce.route('/task/unit/insert', methods=['POST'])
def insertUnit():
    pass

@produce.route('/task/unit/delete', methods=['POST'])
def deleteUnit():
    pass

@produce.route('/task/unit/update', methods=['POST'])
def updateUnit():
    pass

@produce.route('/task/unit/query', methods=['GET'])
def queryUnit():
    pass

@produce.route('/task/article', methods=['GET'])
def article():
    return render_template('article.html')

@produce.route('/task/article/insert', methods=['POST'])
def insertArticle():
    pass

@produce.route('/task/article/delete', methods=['POST'])
def deleteArticle():
    pass

@produce.route('/task/article/update', methods=['POST'])
def updateArticle():
    pass

@produce.route('/task/article/query', methods=['GET'])
def queryArticle():
    pass

@produce.route('/task/section', methods=['GET'])
def section():
    return render_template('section.html')

@produce.route('/task/section/insert', methods=['POST'])
def insertSection():
    pass

@produce.route('/task/section/delete', methods=['POST'])
def deleteSection():
    pass

@produce.route('/task/section/update', methods=['POST'])
def updateSection():
    pass

@produce.route('/task/section/query', methods=['GET'])
def querySection():
    pass