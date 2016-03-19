#!/usr/bin/env python
# coding=utf8
import json
from model.setting import withBase, basecfg
from webcrawl.character import unicode2utf8
from hawkeye import seeunit
from flask import Blueprint, request, Response, render_template, g
from views import produce
from model.base import Unit, Datamodel, Config

@produce.route('/unit/list', methods=['GET'])
@withBase(basecfg.R, resutype='DICT')
def unitlist():
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = int(request.args.get('total', 0))
    if total == 0:
        total = Unit.count({})
    count = (total - 1)/pagetotal + 1
    units = []
    for unit in Unit.queryAll({}, projection={'dmid':1, 'name':1}, sort=[('update_time', -1)], skip=(page-1)*pagetotal, limit=pagetotal):
        datamodel = Datamodel.queryOne({'_id':unit['dmid']}, projection={'name':1})
        unit['unit_name'] = unit['name']
        unit['datamodel_name'] = datamodel['name']
        units.append(unit)
    return render_template('unit/list.html', appname=g.appname, user=user, units=units, pagetotal=pagetotal, page=page, total=total, count=count)

@produce.route('/unit/detail', methods=['GET', 'POST'])
@produce.route('/unit/detail/<uid>', methods=['GET', 'POST'])
@withBase(basecfg.W, resutype='DICT', autocommit=True)
def unitdetail(uid=None):
    datamodels = Datamodel.queryAll({'status':1}, projection={'_id':1, 'name':1}, sort=[('_id', -1)])
    if request.method == 'GET':
        if uid is None:
            unit = {'_id':'', 'unit_name':'', 'datamodel_name':'', 'extra':'', 'dmid':'', 'filepath':'', 'fileupdate':0}
        else:
            config = Config.queryOne({'key':'task'})
            unit = Unit.queryOne({'_id':uid}, projection={'_id':1, 'name':1, 'extra':1, 'filepath':1, 'fileupdate':1})
            unit['filepath'] = '%s%s' % (config['val'], unit['filepath'])
            datamodel = Datamodel.queryOne({'_id':unit['dmid']}, projection={'name':1, '_id':1})
            unit['unit_name'] = unit['name']
            unit['datamodel_name'] = datamodel['name']
            unit['dmid'] = datamodel['_id']
        return render_template('unit/detail.html', appname=g.appname, user=user, unit=unit, datamodels=datamodels)
    elif request.method == 'POST':
        user = request.user
        unit_name = request.form.get('unit_name')
        filepath = request.form.get('filepath')
        extra = request.form.get('extra')
        dmid = request.form.get('dmid')
        print request.form
        if uid is None:
            unit = Unit(name=unit_name,
                filepath=filepath,
                status=1, 
                extra=extra,
                dmid=dmid,
                creator=user['_id'],
                updator=user['_id'],
                create_time=datetime.datetime.now(),
                update_time=datetime.datetime.now()
            )
            uid = Unit.insert(unit)
            # seeunit(baseConn, uid)
        else:
            doc = {
                'extra':extra,
                'updator':user['_id'],
                'update_time':datetime.datetime.now()
            }
            Unit.update({'_id':uid}, {'$set':doc})
            # seeunit(baseConn, uid)
        return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        pass