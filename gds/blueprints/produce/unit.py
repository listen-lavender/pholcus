#!/usr/bin/python
# coding=utf8
import json
from datakit.mysql.suit import withMysql, dbpc, RDB, WDB
from webcrawl.character import unicode2utf8
from hawkeye import seeunit
from flask import Blueprint, request, Response, render_template
from views import produce

@produce.route('/unit/list', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def unitlist():
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = int(request.args.get('total', 0))
    if total == 0:
        total = dbpc.handler.queryOne(""" select count(gu.id) as total from grab_unit gu join grab_datamodel gdm on gu.dmid = gdm.id; """)['total']
    count = (total - 1)/pagetotal + 1
    units = dbpc.handler.queryAll(""" select gu.id, gu.name as unit_name, gdm.name as datamodel_name from grab_unit gu join grab_datamodel gdm on gu.dmid = gdm.id order by gu.update_time desc limit %s, %s; """, ((page-1)*pagetotal, pagetotal))
    return render_template('unitlist.html', units=units, pagetotal=pagetotal, page=page, total=total, count=count)

@produce.route('/unit/detail', methods=['GET', 'POST'])
@produce.route('/unit/detail/<uid>', methods=['GET', 'POST'])
@withMysql(WDB, resutype='DICT', autocommit=True)
def unitdetail(uid=None):
    datamodels = dbpc.handler.queryAll(""" select `id`, `name` from grab_datamodel where `status` = 1 order by `id` desc; """)
    if request.method == 'GET':
        if uid is None:
            unit = {'id':'', 'unit_name':'', 'datamodel_name':'', 'extra':'', 'dmid':''}
        else:
            unit = dbpc.handler.queryOne(""" select gu.id, gu.name as unit_name, gdm.name as datamodel_name, gu.extra, gdm.id as dmid from grab_unit gu join grab_datamodel gdm on gu.dmid = gdm.id where gu.id = %s; """, (uid,))
        return render_template('unitdetail.html', unit=unit, datamodels=datamodels)
    elif request.method == 'POST':
        unit_name = request.form.get('unit_name')
        dirpath = request.form.get('dirpath')
        filepath = request.form.get('filepath')
        extra = request.form.get('extra')
        dmid = request.form.get('dmid')
        print request.form
        if uid is None:
            dbpc.handler.insert(""" insert into `grab_unit` (`dmid`, `name`, `dirpath`, `filepath`, `status`, `extra`, `dmid`, `creator`, `updator`, `create_time`, `update_time`)values(1, %s, %s, %s, 1, %s, 0, 0, now(), now()); """, (unit_name, dirpath, filepath, extra, dmid))
            uid = dbpc.handler.queryOne(""" select * from grab_unit where `name` = %s """, (unit_name,))['id']
            # seeunit(dbpc, uid)
        else:
            dbpc.handler.update(""" update `grab_unit` set `name` = %s, `dirpath` = %s, `filepath` = %s, `extra` = %s, `dmid` = %s, update_time=now() where `id` = %s """, (unit_name, dirpath, filepath, extra, dmid, uid))
            # seeunit(dbpc, uid)
        return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        pass