#!/usr/bin/python
# coding=utf8
import json
from datakit.mysql.suit import withMysql, dbpc, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template
from views import produce

@produce.route('/datasource/list', methods=['GET'])
@produce.route('/datasource/list/<sid>', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def datasourcelist(sid):
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = int(request.args.get('total', 0))
    if total == 0:
        total = dbpc.handler.queryOne(""" select count(id) as total from grab_datasource where sid = %s or '' = %s; """, (sid, sid))['total']
    count = (total - 1)/pagetotal + 1
    datasources = dbpc.handler.queryAll(""" select `id`, `name` from grab_datasource where sid = %s or ''=%s; """, (sid, sid))
    return render_template('datasourcelist.html', sid=sid, datasources=datasources, pagetotal=pagetotal, page=page, total=total, count=count)

@produce.route('/datasource/detail', methods=['GET', 'POST'])
@produce.route('/datasource/detail/<sid>', methods=['GET', 'POST'])
@withMysql(WDB, resutype='DICT', autocommit=True)
def datasourcedetail(sid=None):
    sid = int(request.args.get('sid', 0))
    if request.method == 'GET':
        if sid is None:
            datasource = {'sid':'', 'next_id':'', 'name':'', 'initflow':'', 'index':'', 'retry':'', 'timelimit':'', 'store':''}
        else:
            datasource = dbpc.handler.queryOne(""" select * from grab_datasource where id = %s; """, sid)
        return render_template('datasourcedetail.html', sid=sid, datasource=datasource)
    elif request.method == 'POST':
        datasource_name = request.form.get('datasource_name')
        next_id = request.form.get('next_id')
        initflow = request.form.get('initflow')
        index = request.form.get('index')
        retry = request.form.get('retry')
        timelimit = request.form.get('timelimit')
        store = request.form.get('store')
        if sid is None:
            dbpc.handler.insert(""" insert into `grab_datasource` (`sid`, `name`, `next_id`, `initflow`, `index`, `retry`, `timelimit`, `store`, `creator`, `updator`, `create_time`, `update_time`)values(%s, %s, %s, %s, %s, %s, %s, %s, 1, null, 0, 0, now(), now()); """, (sid, datasource_name, next_id, initflow, index, retry, timelimit, store))
        else:
            dbpc.handler.update(""" update `grab_datasource` set `name` = %s, `next_id` = %s, `initflow` = %s, `index` = %s, `retry` = %s, `timelimit` = %s, `store` = %s, update_time=now() where `id` = %s """, (datasource_name, next_id, initflow, index, retry, timelimit, store, sid))
        return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        pass
