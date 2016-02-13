#!/usr/bin/python
# coding=utf8
import json, datetime
from settings import withBase, withData, baseConn, dataConn, _BASE_R, _BASE_W
from webcrawl.character import unicode2utf8
from hawkeye import seearticle
from flask import Blueprint, request, Response, render_template, g
from views import produce
from model.base import Article

@produce.route('/article/list', methods=['GET'])
@produce.route('/article/list/<uid>', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def articlelist(uid=''):
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = int(request.args.get('total', 0))
    if total == 0:
        total = Article.count({'$or':[{'uid':uid}, {'""':uid}]})
    count = (total - 1)/pagetotal + 1
    articles = Article.queryAll({'$or':[{'uid':uid}, {'""':uid}]}, projection={'id':1, 'name':1, 'filepath':1, 'uid':1}, sort=[('update_time', -1)], skip=(page-1)*pagetotal, limit=pagetotal)
    return render_template('particlelist.html', appname=g.appname, logined=True, uid=uid, articles=articles, pagetotal=pagetotal, page=page, total=total, count=count)

@produce.route('/article/detail', methods=['GET', 'POST'])
@produce.route('/article/detail/<aid>', methods=['GET', 'POST'])
@withMysql(WDB, resutype='DICT', autocommit=True)
def articledetail(aid=None):
    uid = int(request.args.get('uid') or 0)
    if request.method == 'GET':
        if aid is None:
            article = {'id':'', 'host':'', 'pinyin':''}
        else:
            article = Article.queryOne({'id':aid}, projection={'id':1, 'host':1, 'pinyin':1})
        return render_template('particledetail.html', appname=g.appname, logined=True, uid=uid, article=article)
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
                creator=user['id'],
                updator=user['id'],
                create_time=datetime.datetime.now(),
                update_time=datetime.datetime.now())
            aid = Article.insert(article)
        else:
            Article.update({'id':aid}, {'$set':{'name':article_name, 'host':host, 'pinyin':pinyin, 'filepath':filepath, 'updator':user['id'], 'update_time':datetime.datetime.now()}})
        return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        pass