#!/usr/bin/env python
# coding=utf8
import json
from webcrawl.character import unicode2utf8
from model.setting import withBase, basecfg
from model.base import Article, Flow, Section, Creator
from flask import Blueprint, request, Response, render_template, g

script = Blueprint('script', __name__, template_folder='template')

from step import *

@script.route('/list', methods=['GET'])
@script.route('/list/<uid>', methods=['GET'])
@withBase(basecfg.R, resutype='DICT')
def script_list(uid=''):
    user = request.user
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = int(request.args.get('total', 0))
    if total == 0:
        total = Article.count(user, {})
    count = (total - 1)/pagetotal + 1
    articles = Article.queryAll(user, {}, projection={'_id':1, 'name':1, 'filepath':1, 'uid':1}, sort=[('update_time', -1)], skip=(page-1)*pagetotal, limit=pagetotal)
    result = {"appname":g.appname, "user":user, "uid":uid, "script":articles, "pagetotal":pagetotal, "page":page, "total":total, "count":count}
    result = json.dumps({'code':1, 'msg':'', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result

@script.route('/', methods=['POST'])
@script.route('/<aid>', methods=['POST', 'GET'])
@withBase(basecfg.R, resutype='DICT', autocommit=True)
def script_detail(aid=None):
    user = request.user
    if request.method == 'GET':
        if aid is None:
            article = {'_id':'', 'name':'', 'clsname':'', 'desc':1, 'filepath':'', 'fileupdate':0, 'flows':[]}
        else:
            article = Article.queryOne(user, {'_id':aid}, projection={'_id':1, 'name':1, 'clsname':1, 'desc':1, 'filepath':1, 'fileupdate':1})
            article['flows'] = list(Flow.queryAll({'aid':aid}, projection={'name':1, '_id':1}))
        result = {"appname":g.appname, "user":user, "script":article}
        result = json.dumps({'code':1, 'msg':'', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
        return result
    elif request.method == 'POST':
        name = request.form.get('name')
        clsname = request.form.get('clsname')
        desc = request.form.get('desc')
        filepath = request.form.get('filepath')
        result = {'code':1, 'msg':'', 'res':{"appname":g.appname, "user":user}}
        if aid is None:
            article = Article(
                uid=user['_id'],
                name=name,
                clsname=clsname,
                filepath=filepath,
                status=status,
                creator=user['_id'],
                updator=user['_id'],
                create_time=datetime.datetime.now(),
                update_time=datetime.datetime.now())
            aid = Article.insert(user, article)
            result['msg'] = 'Create article successfully.'
        else:
            Article.update(user, {'_id':aid}, {'desc':desc})
            result['msg'] = 'Update article successfully.'
        result = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
        return result
    else:
        pass
