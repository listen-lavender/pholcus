#!/usr/bin/env python
# coding=utf8
import json
from webcrawl.character import unicode2utf8
from model.setting import withBase, basecfg
from model.base import Article, Creator
from flask import Blueprint, request, Response, render_template, g

script = Blueprint('script', __name__, template_folder='template')

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
    print result
    return result

@script.route('/article', methods=['POST'])
@script.route('/article/<aid>', methods=['POST'])
@withBase(basecfg.R, resutype='DICT')
def article(aid=None):
    user = request.user
    condition = request.form.get('condition', '{}')
    condition = json.loads(condition)
    data = request.form.get('data', '{}')
    data = json.loads(data)
    pyfile = request.files.get('file')
    projection = request.form.get('projection', '{}')
    projection = json.loads(projection)

    limit = request.form.get('limit', 'one')

    if aid is not None:
        condition['_id'] = aid
    POST = False
    if pyfile:
        POST = True
        result = {'stat':0, 'desc':'请上传正确格式的python文件', 'datamodel':''}
        if pyfile and allowed(pyfile.filename):
            filename = pyfile.filename
            pyfile.save(exepath(filename))
            result['stat'] = 1
            result['desc'] = '上传成功'
        result = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    if data:
        POST = True
        data['updator'] = user['_id']
        if '_id' in condition:
            Article.update(user, condition, data)
            aid = condition['_id']
        else:
            data['creator'] = user['_id']
            data = Article(**data)
            aid = Article.insert(user, data)
        result = json.dumps({'stat':1, 'desc':'Article is set successfully.', 'aid':aid}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    if not POST:
        if limit == 'one':
            result = Article.queryOne(user, condition, projection=projection)
            if result:
                result = format_datetime(result)
        else:
            result = []
            for one in Article.queryAll(user, condition, projection=projection):
                one = format_datetime(one)
                result.append(one)
        result = json.dumps({'stat':1, 'desc':'', 'article':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result