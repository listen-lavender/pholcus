#!/usr/bin/python
# coding=utf8
import json
from model.settings import withBase, withData, base, data, _BASE_R, _BASE_W, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from views import produce
from model.base import Datamodel, Dataitem

@produce.route('/datamodel/list', methods=['GET'])
@withBase(RDB, resutype='DICT')
def modellist():
    datamodels = Datamodel.queryAll({})
    return render_template('datamodel/list.html', appname=g.appname, user=user, datamodels=datamodels)

@produce.route('/datamodel/detail/<dmid>', methods=['GET'])
@withBase(WDB, resutype='DICT', autocommit=True)
def modeldetail(dmid=None):
    rows = ['_id', 'name', 'extra']
    cols = ['_id', 'dmid', 'name', 'length', 'default']
    # rows = ['_id', 'name', 'comment', 'autocreate', 'iscreated', 'status', 'extra', 'creator', 'updator', 'create_time', 'update_time']
    # cols = ['_id', 'dmid', 'name', 'comment', 'default', 'nullable', 'unique']
    adds = ['ditype', 'ddl']
    rowvals = Datamodel.queryOne({'$or':[{'_id':dmid}, {'_id':''}]}, projection=dict(zip(rows, [1 for one in rows]))) or dict(zip(rows, ['' for one in rows]))
    colvals = Dataitem.queryAll({'$or':[{'_id':rowvals['_id']}, {'_id':''}]}, projection=dict(zip(cols, [1 for one in cols])))
    for col in colvals:
        del col['dmid']
    cols.remove('dmid')
    cols.remove('_id')
    rows.remove('_id')
    return render_template('datamodel/detail.html', appname=g.appname, user=user, rows=rows, cols=cols, rowvals=unicode2utf8(rowvals), colvals=unicode2utf8(colvals), colspan=len(cols)-1)
