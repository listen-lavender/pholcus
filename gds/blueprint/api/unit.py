#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
from model.setting import withBase, withData, base, data, _BASE_R, _BASE_W, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from views import monitor
from model.base import Unit, Creator
from model.log import Statistics

@monitor.route('/unit', methods=['GET', 'POST'])
@monitor.route('/unit/<uid>', methods=['GET'])
@withBase(RDB, resutype='DICT')
def unit(uid=None):
    paras = dict(urlparse.parse_qsl(urlparse.urlparse(request.url).query))
    user = Creator.queryOne({}, {'username':paras['appKey']})
    if checksign(paras, user['secret']):
        user['name'] = user['username']
    else:
        user = {}
    if request.method == 'GET':
        cond = dict(urlparse.parse_qsl(urlparse.urlparse(request.url).query))
        if uid is None:
            result = Unit.queryAll(user, cond)
        else:
            result = Unit.queryOne(user, {'_id':uid})
        return json.dumps({'stat':1, 'desc':'', 'unit':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    elif request.method == 'POST':
        dmid = request.form.get('dmid')
        name = request.form.get('name')
        filepath = request.form.get('filepath')
        extra = request.form.get('extra')
        unit = Unit(dmid=dmid, name=name, filepath=filepath, status=1, extra=extra, create_time=datetime.datetime.now())
        uid = Unit.insert(user, unit)
        return json.dumps({'stat':1, 'desc':'Unit %s is set successfully.' % name, 'uid':uid}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')

