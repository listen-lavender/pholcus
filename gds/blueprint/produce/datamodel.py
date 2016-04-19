#!/usr/bin/env python
# coding=utf8
import json
from model.setting import withBase, basecfg
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from views import produce
from model.base import Datamodel, Dataitem
from . import allow_cross_domain

@produce.route('/datamodel/list', methods=['GET'])
@allow_cross_domain
@withBase(basecfg.R, resutype='DICT')
def modellist():
    datamodels = Datamodel.queryAll({})
    if request.headers.get('User-Agent') == 'test':
        result = {"appname":g.appname, "user":user, "datamodels":datamodels}
        return json.dumps({'stat':1, 'desc':'success', 'result':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        return render_template('datamodel/list.html', appname=g.appname, user=user, datamodels=datamodels)

@produce.route('/datamodel/detail/<dmid>', methods=['GET'])
@allow_cross_domain
@withBase(basecfg.W, resutype='DICT', autocommit=True)
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
    if request.headers.get('User-Agent') == 'test':
        result = {"appname":g.appname, "user":user, "rows":rows, "cols":cols, "rowvals":unicode2utf8(rowvals), "colvals":unicode2utf8(colvals), "colspan":len(cols)-1}
        return json.dumps({'stat':1, 'desc':'success', 'result':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        return render_template('datamodel/detail.html', appname=g.appname, user=user, rows=rows, cols=cols, rowvals=unicode2utf8(rowvals), colvals=unicode2utf8(colvals), colspan=len(cols)-1)
