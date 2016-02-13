#!/usr/bin/python
# coding=utf8
import json
from settings import withBase, withData, baseConn, dataConn, _BASE_R, _BASE_W
from webcrawl.character import unicode2utf8
from hawkeye import seeunit
from flask import Blueprint, request, Response, render_template, g
from views import produce
from model.base import Unit, Datamodel

@produce.route('/unit/list', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def unitlist():
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = int(request.args.get('total', 0))
    if total == 0:
        total = Unit.count({})
    count = (total - 1)/pagetotal + 1
    units = []
    for unit in Unit.queryAll({}, projection={'dmid':1, 'name':1}, sort=[('update_time', -1)], skip=(page-1)*pagetotal, limit=pagetotal):
        datamodel = Datamodel.queryOne({'id':unit['dmid']}, projection={'name':1})
        unit['unit_name'] = unit['name']
        unit['datamodel_name'] = datamodel['name']
        units.append(unit)
    return render_template('punitlist.html', appname=g.appname, logined=True, units=units, pagetotal=pagetotal, page=page, total=total, count=count)

@produce.route('/unit/detail', methods=['GET', 'POST'])
@produce.route('/unit/detail/<uid>', methods=['GET', 'POST'])
@withMysql(WDB, resutype='DICT', autocommit=True)
def unitdetail(uid=None):
    datamodels = Datamodel.queryAll({'status':1}, projection={'id':1, 'name':1}, sort=[('id', -1)])
    if request.method == 'GET':
        if uid is None:
            unit = {'id':'', 'unit_name':'', 'datamodel_name':'', 'extra':'', 'dmid':''}
        else:
            unit = Unit.queryOne({'id':uid}, projection={'id':1, 'name':1, 'extra':1})
            datamodel = Datamodel.queryOne({'id':unit['dmid']}, projection={'name':1, 'id':1})
            unit['unit_name'] = unit['name']
            unit['datamodel_name'] = datamodel['name']
            unit['dmid'] = datamodel['id']
        return render_template('punitdetail.html', appname=g.appname, logined=True, unit=unit, datamodels=datamodels)
    elif request.method == 'POST':
        user = request.user
        unit_name = request.form.get('unit_name')
        dirpath = request.form.get('dirpath')
        filepath = request.form.get('filepath')
        extra = request.form.get('extra')
        dmid = request.form.get('dmid')
        print request.form
        if uid is None:
            unit = Unit(name=unit_name,
                dirpath=dirpath,
                filepath=filepath,
                status=1, 
                extra=extra,
                dmid=dmid,
                creator=user['id'],
                updator=user['id'],
                create_time=datetime.datetime.now(),
                update_time=datetime.datetime.now()
            )
            uid = Unit.insert(unit)
            # seeunit(baseConn, uid)
        else:
            doc = {
                'name':unit_name,
                'dirpath':dirpath,
                'filepath':filepath,
                'extra':extra,
                'dmid':dmid,
                'updator':user['id'],
                'update_time':datetime.datetime.now()
            }
            baseConn.handler.update({'id':uid}, doc)
            # seeunit(baseConn, uid)
        return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        pass