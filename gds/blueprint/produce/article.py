#!/usr/bin/python
# coding=utf8
import json, datetime
from model.settings import withBase, withData, base, data, _BASE_R, _BASE_W, RDB, WDB
from webcrawl.character import unicode2utf8
from hawkeye import seearticle
from flask import Blueprint, request, Response, render_template, g
from views import produce
from model.base import Article, Permit

@produce.route('/article/list', methods=['GET'])
@produce.route('/article/list/<uid>', methods=['GET'])
@withBase(RDB, resutype='DICT')
def articlelist(uid=''):
    user = request.user
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = int(request.args.get('total', 0))
    if total == 0:
        total = Article.count(user, {})
    count = (total - 1)/pagetotal + 1
    articles = Article.queryAll(user, {}, projection={'_id':1, 'name':1, 'filepath':1, 'uid':1}, sort=[('update_time', -1)], skip=(page-1)*pagetotal, limit=pagetotal)
    return render_template('article/list.html', appname=g.appname, user=user, uid=uid, articles=articles, pagetotal=pagetotal, page=page, total=total, count=count)

@produce.route('/article/detail', methods=['GET', 'POST'])
@produce.route('/article/detail/<aid>', methods=['GET', 'POST'])
@withBase(WDB, resutype='DICT', autocommit=True)
def articledetail(aid=None):
    user = request.user
    uid = int(request.args.get('uid') or 0)
    if request.method == 'GET':
        if aid is None:
            article = {'_id':'', 'host':'', 'pinyin':''}
        else:
            article = Article.queryOne(user, {'_id':aid}, projection={'_id':1, 'host':1, 'pinyin':1})
        return render_template('article/detail.html', appname=g.appname, user=user, uid=uid, article=article)
    elif request.method == 'POST':
        user = request.user
        host = request.form.get('host')
        article_name = host.split('.')[1]
        pinyin = request.form.get('pinyin')
        filepath = 'spider%s.py' % pinyin.capitalize()
        if aid is None:
            article = Article(
                uid=uid,
                name=name,
                host=host,
                pinyin=pinyin,
                filepath=filepath,
                status=status,
                creator=user['_id'],
                updator=user['_id'],
                create_time=datetime.datetime.now(),
                update_time=datetime.datetime.now())
            aid = Article.insert(user, article)
        else:
            Article.update(user, {'_id':aid}, {'name':article_name, 'host':host, 'pinyin':pinyin, 'filepath':filepath, 'updator':user['_id'], 'update_time':datetime.datetime.now()})
        return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        pass