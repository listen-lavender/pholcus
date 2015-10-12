#!/usr/bin/python
# coding=utf8
import json
from datakit.mysql.suit import withMysql, dbpc, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template
from views import produce

@produce.route('/dataextract/list', methods=['GET'])
@produce.route('/dataextract/list/<sid>', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def dataextractlist(sid):
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = int(request.args.get('total', 0))
    if total == 0:
        total = dbpc.handler.queryOne(""" select count(id) as total from grab_dataextract where sid = %s or '' = %s; """, (sid, sid))['total']
    count = (total - 1)/pagetotal + 1
    dataextracts = dbpc.handler.queryAll(""" select `id`, `name` from grab_dataextract where sid = %s or ''=%s; """, (sid, sid))
    return render_template('dataextractlist.html', sid=sid, dataextracts=dataextracts, pagetotal=pagetotal, page=page, total=total, count=count)

@produce.route('/dataextract/detail', methods=['GET', 'POST'])
@produce.route('/dataextract/detail/<sid>', methods=['GET', 'POST'])
@withMysql(WDB, resutype='DICT', autocommit=True)
def dataextractdetail(sid=None):
    sid = int(request.args.get('sid', 0))
    if request.method == 'GET':
        if sid is None:
            dataextract = {'sid':'', 'next_id':'', 'name':'', 'initflow':'', 'index':'', 'retry':'', 'timelimit':'', 'store':''}
        else:
            dataextract = dbpc.handler.queryOne(""" select `sid`,`next_id`,`name`,`initflow`,`index`,`retry`,`timelimit`,`store` from grab_dataextract where id = %s; """, sid)
        return render_template('dataextractdetail.html', sid=sid, dataextract=dataextract)
    elif request.method == 'POST':
        dataextract_name = request.form.get('dataextract_name')
        next_id = request.form.get('next_id')
        initflow = request.form.get('initflow')
        index = request.form.get('index')
        retry = request.form.get('retry')
        timelimit = request.form.get('timelimit')
        store = request.form.get('store')
        if sid is None:
            dbpc.handler.insert(""" insert into `grab_dataextract` (`sid`, `name`, `next_id`, `initflow`, `index`, `retry`, `timelimit`, `store`, `creator`, `updator`, `create_time`, `update_time`)values(%s, %s, %s, %s, %s, %s, %s, %s, 1, null, 0, 0, now(), now()); """, (sid, dataextract_name, next_id, initflow, index, retry, timelimit, store))
        else:
            dbpc.handler.update(""" update `grab_dataextract` set `name` = %s, `next_id` = %s, `initflow` = %s, `index` = %s, `retry` = %s, `timelimit` = %s, `store` = %s, update_time=now() where `id` = %s """, (dataextract_name, next_id, initflow, index, retry, timelimit, store, sid))
        return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        pass
