#!/usr/bin/env python
# coding=utf8
import json, datetime
from model.setting import withBase, basecfg
from webcrawl.character import unicode2utf8
from hawkeye import seearticle
from flask import Blueprint, request, Response, render_template, g
from views import produce
from model.base import Article, Section, Permit

@produce.route('/article/list', methods=['GET'])
@produce.route('/article/list/<uid>', methods=['GET'])
@withBase(basecfg.R, resutype='DICT')
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
@withBase(basecfg.W, resutype='DICT', autocommit=True)
def articledetail(aid=None):
    user = request.user
    uid = int(request.args.get('uid') or 0)
    if request.method == 'GET':
        if aid is None:
            article = {'_id':'', 'name':'', 'clsname':'', 'filepath':'', 'fileupdate':0}
        else:
            article = Article.queryOne(user, {'_id':aid}, projection={'_id':1, 'name':1, 'clsname':1, 'filepath':1, 'fileupdate':1})
            sections = Section.queryAll(user, {'aid':aid}, projection={'flow':1})
            article['flows'] = list(set([section['flow'] for section in sections]))
        return render_template('article/detail.html', appname=g.appname, user=user, uid=uid, article=article)
    elif request.method == 'POST':
        user = request.user
        name = request.form.get('name')
        clsname = request.form.get('clsname')
        filepath = request.form.get('filepath')
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
        else:
            Article.update(user, {'_id':aid}, {'name':name})
        return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        pass