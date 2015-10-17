#!/usr/bin/python
# coding=utf8
import json
from datakit.mysql.suit import withMysql, dbpc, RDB, WDB
from webcrawl.character import unicode2utf8
from hawkeye import seearticle
from flask import Blueprint, request, Response, render_template
from views import produce

@produce.route('/article/list', methods=['GET'])
@produce.route('/article/list/<uid>', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def articlelist(uid):
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = int(request.args.get('total', 0))
    if total == 0:
        total = dbpc.handler.queryOne(""" select count(id) as total from grab_article where uid = %s or '' = %s; """, (uid, uid))['total']
    count = (total - 1)/pagetotal + 1
    articles = dbpc.handler.queryAll(""" select `id`, `name`, `filepath`, `uid` from grab_article where uid = %s or '' = %s order by update_time desc limit %s, %s; """, (uid, uid, (page-1)*pagetotal, pagetotal))
    return render_template('articlelist.html', uid=uid, articles=articles, pagetotal=pagetotal, page=page, total=total, count=count)

@produce.route('/article/detail', methods=['GET', 'POST'])
@produce.route('/article/detail/<aid>', methods=['GET', 'POST'])
@withMysql(WDB, resutype='DICT', autocommit=True)
def articledetail(aid=None):
    uid = int(request.args.get('uid', 0))
    if request.method == 'GET':
        if aid is None:
            article = {'id':'', 'host':'', 'pinyin':''}
        else:
            article = dbpc.handler.queryOne(""" select `id`, `host`, `pinyin` from grab_article where id = %s; """, (aid,))
        print aid, article
        return render_template('articledetail.html', uid=uid, article=article)
    elif request.method == 'POST':
        host = request.form.get('host')
        article_name = host.split('.')[1]
        pinyin = request.form.get('pinyin')
        filepath = 'spider%s.py' % pinyin.capitalize()
        if aid is None:
            dbpc.handler.insert(""" insert into `grab_article` (`uid`, `name`, `host`, `pinyin`, `filepath`, `filepath`, `status`, `extra`, `creator`, `updator`, `create_time`, `update_time`)values(%s, %s, %s, %s, %s, 1, null, 0, 0, now(), now()); """, (uid, article_name, host, pinyin, filepath))
            aid = dbpc.handler.queryOne(""" select * from grab_article where `uid` = %s and `name` = %s """, (uid, article_name))['id']
            # seearticle(dbpc, uid, aid)
        else:
            dbpc.handler.update(""" update `grab_article` set `name` = %s, `host` = %s, `pinyin` = %s, `filepath` = %s, update_time=now() where `id` = %s """, (article_name, host, pinyin, filepath, aid))
            # seearticle(dbpc, uid, aid)
        return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        pass