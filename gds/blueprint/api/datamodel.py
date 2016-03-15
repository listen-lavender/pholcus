#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
from model.setting import withBase, withData, base, data, _BASE_R, _BASE_W, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from views import monitor
from model.base import Datamodel, Creator
from model.log import Statistics

@monitor.route('/datamodel', methods=['GET', 'POST'])
@monitor.route('/datamodel/<tid>', methods=['GET'])
@withBase(RDB, resutype='DICT')
def datamodel(tid=None):
    paras = dict(urlparse.parse_qsl(urlparse.urlparse(request.url).query))
    user = Creator.queryOne({}, {'username':paras['appKey']})
    if checksign(paras, user['secret']):
        user['name'] = user['username']
    else:
        user = {}
    if request.method == 'GET':
        if tid is None:
            Datamodel.queryAll(user)
        else:
            Datamodel.queryOne(user, {'_id':tid})
    elif request.method == 'POST':
        name = request.form.get('name')
        table = request.form.get('name')
        comment = request.form.get('comment')
        datamodel = Datamodel(name=model, table=table, comment=comment, autocreate=1, iscreated=1, status=1, create_time=datetime.datetime.now())
        dmid = Datamodel.insert(datamodel)
        return json.dumps({'stat':1, 'desc':'Data model %s is set successfully.' % name, 'dmid':dmid}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
