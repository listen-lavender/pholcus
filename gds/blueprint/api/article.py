#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
from model.setting import withBase, withData, base, data, _BASE_R, _BASE_W, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from views import monitor
from model.base import Article, Creator
from model.log import Statistics

@monitor.route('/article', methods=['GET', 'POST'])
@monitor.route('/article/<tid>', methods=['GET'])
@withBase(RDB, resutype='DICT')
def article(tid=None):
    paras = dict(urlparse.parse_qsl(urlparse.urlparse(request.url).query))
    user = Creator.queryOne({}, {'username':paras['appKey']})
    if checksign(paras, user['secret']):
        user['name'] = user['username']
    else:
        user = {}
    if request.method == 'GET':
        if tid is None:
            return Article.queryAll(user)
        else:
            return Article.queryOne(user, {'_id':tid})
    elif request.method == 'POST':
        uid = request.form.get('uid')
        name = request.form.get('name')
        pinyin = request.form.get('pinyin')
        host = request.form.get('host')
        filepath = request.form.get('filepath')
        extra = request.form.get('extra')
        article = Article(uid=uid, name=name, pinyin=pinyin, host=host, filepath=filepath, create_time=datetime.datetime.now())
        aid = Article.insert(user, article)
        return json.dumps({'stat':1, 'desc':'Article %s is set successfully.' % name, 'aid':aid}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
