#!/usr/bin/python
# coding=utf8
import json
import time, datetime
from settings import withBase, withData, baseConn, dataConn, _BASE_R, _BASE_W
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from views import monitor

@monitor.route('/task/data/<tid>', methods=['GET'])
@withMysql(RDB)
def taskdata(tid):
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = int(request.args.get('total', 0))
    count = (total - 1)/pagetotal + 1
    model = baseConn.handler.queryOne(""" select gdm.name 
                                from grab_task gt join grab_article ga join grab_unit gu join grab_datamodel gdm
                                    on gdm.id = gu.dmid and gu.id = ga.uid and gt.aid = ga.id where gt.id = %s; """, (tid, ))

    tid = 0
    columns = []
    datas = []
    pagetotal = 0
    page = 0
    total = 0
    count =0 
    return render_template('mtaskdata.html', appname=g.appname, logined=True, title=model['name'], columns=columns, rows=datas, pagetotal=pagetotal, page=page, total=total, count=count)
