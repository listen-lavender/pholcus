#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
from model.setting import withBase, withData, base, data, _BASE_R, _BASE_W, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from views import monitor
from model.base import Section, Creator
from model.log import Statistics

@monitor.route('/section', methods=['GET', 'POST'])
@monitor.route('/section/<tid>', methods=['GET'])
@withBase(RDB, resutype='DICT')
def section(tid=None):
    paras = dict(urlparse.parse_qsl(urlparse.urlparse(request.url).query))
    user = Creator.queryOne({}, {'username':paras['appKey']})
    if checksign(paras, user['secret']):
        user['name'] = user['username']
    else:
        user = {}
    if request.method == 'GET':
        if tid is None:
            Section.queryAll(user, {})
        else:
            Section.queryOne(user, {'_id':tid})
    elif request.method == 'POST':
        article_id = request.form.get('article_id')
        next_id = request.form.get('next_id')
        name = request.form.get('name')
        flow = request.form.get('flow')
        step = request.form.get('step')
        index = request.form.get('index')
        retry = request.form.get('retry')
        timelimit = request.form.get('store')
        section = Section(aid=article_id, next_id=next_id, name=name, flow=flow, step=step, index=index, retry=retry, timelimit=timelimit, store=store, create_time=datetime.datetime.now())
        sid = Section.insert(user, section)
        return json.dumps({'stat':1, 'desc':'Section %s %s is set successfully.' % (flow, section_name), 'sid':sid}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')

