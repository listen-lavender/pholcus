#!/usr/bin/env python
# coding=utf8
import json
from model.setting import withBase, basecfg, pack
from model.base import Article, Flow, Creator, Permit
from flask import Blueprint, request, Response, render_template, g
from .. import select, unselect

script = Blueprint('script', __name__, template_folder='template')

from step import *

@script.route('/list', methods=['GET'])
@script.route('/list/<uid>', methods=['GET'])
@withBase(basecfg.R, resutype='DICT')
def scriptlist(uid=''):
    user = request.user
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 10))
    keyword = request.args.get('keyword')

    condition = {'status':1}
    if keyword:
        pack(Article, keyword, condition)
    total = Article.count(condition)
    articles = Article.queryAll(user, condition, projection={'name':1, 'desc':1}, sort=[('update_time', -1)], skip=skip, limit=limit)
    result = {"appname":g.appname, "user":user, "uid":uid, "script":articles, "total":total}
    result = json.dumps({'code':1, 'msg':'', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result


@script.route('/<aid>', methods=['POST', 'GET'])
@withBase(basecfg.W, resutype='DICT', autocommit=True)
def scriptdetail(aid=None):
    user = request.user
    if request.method == 'GET':
        if aid is None:
            article = {'_id':'', 'name':'', 'clsname':'', 'desc':1, 'filepath':'', 'digest':0, 'flows':[], 'own':True}
        else:
            article = Article.queryOne(user, {'_id':aid}, projection={'name':1, 'clsname':1, 'desc':1, 'filepath':1, 'digest':1, 'creator':1})
            article['own'] = str(article['creator']) == user['_id']
            article['flows'] = list(Flow.queryAll(user, {'aid':aid}, projection={'name':1, '_id':1}))

        projection = {'_id':1, 'username':1}
        article['creators'] = [{'text':one['username'], 'value':one['_id']} for one in Creator.queryAll(user, {'_id':{'$ne':user['_id']}}, projection=projection, limit=None)]
        article['select_updators'] = ','.join([str(one['cid']) for one in Permit.queryAll({'creator':user['_id'], 'oid':aid, 'otype':'Article', 'authority':{'$in':[2,3,6,7,10,11,14,15]}}, projection={'cid':1}, limit=None)])
        article['select_queryers'] = ','.join([str(one['cid']) for one in Permit.queryAll({'creator':user['_id'], 'oid':aid, 'otype':'Article', 'authority':{'$mod':[2, 1]}}, projection={'cid':1}, limit=None)])

        result = {"appname":g.appname, "user":user, "script":article}
        result = json.dumps({'code':1, 'msg':'', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
        return result
    elif request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('desc')
        select_updators = request.form.get('select_updators')
        unselect_updators = request.form.get('unselect_updators')
        select_queryers = request.form.get('select_queryers')
        unselect_queryers = request.form.get('unselect_queryers')
        result = {'code':1, 'msg':'', 'res':{"appname":g.appname, "user":user}}
        if aid is None:
            result['msg'] = 'Not create article.'
        else:
            Article.update(user, {'_id':aid}, {'$set':{'name':name, 'desc':desc}})
            result['msg'] = 'Update article successfully.'
            select(select_updators, 'Article', aid, user['_id'], 'update')
            unselect(unselect_updators, 'Article', aid, user['_id'])
            select(select_queryers, 'Article', aid, user['_id'], 'query')
            unselect(unselect_queryers, 'Article', aid, user['_id'])
        result = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
        return result
    else:
        pass
