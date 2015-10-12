#!/usr/bin/python
# coding=utf-8
import time
from webcrawl.godhand import cook
from datakit.mysql.suit import withMysql, dbpc
from task.config.db.mysql import RDB, WDB
from task.model.mysql import initDB
from webcrawl.handleRequest import parturl
from do import makeunit, makearticle

initDB()

units = ["""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
  ({{uid}}, 'unit', 0, '', '', '%s', '', 'init', null, null, null, 'module');
""",
"""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
  ({{uid}}, 'unit', {{mid}}, 'module', '', 'withDB', '', 'import', 'from datakit.mysql.suit import', null, 'withMysql', 'decorator'),
  ({{uid}}, 'unit', {{mid}}, 'module', '', 'Data', '', 'import', 'from task.model.mysql import', null, '%s', 'class'),
  ({{uid}}, 'unit', {{mid}}, 'module', '', 'initDB', '', 'import', 'from task.model.mysql import', null, 'initDB', 'function'),
  ({{uid}}, 'unit', {{mid}}, 'module', '', 'WDB', '', 'import', 'from task.config.db.mysql import', null, 'WDB', 'str'),
  ({{uid}}, 'unit', {{mid}}, 'module', '', 'RDB', '', 'import', 'from task.config.db.mysql import', null, 'RDB', 'str'),
  ({{uid}}, 'unit', {{mid}}, 'module', '', 'Spider%sOrigin', '', 'init', null, null, null, 'class');
""",
"""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
  ({{uid}}, 'unit', {{cid}}, 'class', '1', 'SpiderOrigin', '', 'params', null, null, null, 'class'),
  ({{uid}}, 'unit', {{cid}}, 'class', '', '__init__', '', 'init', null, null, null, 'function'),
  ({{uid}}, 'unit', {{cid}}, 'class', '', '__del__', '', 'init', null, null, null, 'function');
""",
"""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
  ({{uid}}, 'unit', {{fid}}, 'function', '%s', '', '', 'init', null, null, null, 'execute');
"""]

articles = ["""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
({{aid}}, 'article', 0, '', '', '%s', '', 'init', null, null, null, 'module');
""",
"""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
({{aid}}, 'article', {{mid}}, 'module', '', 'Data', '', 'import', 'from %s import', null, 'Data', 'class'),
({{aid}}, 'article', {{mid}}, 'module', '', '%s', '', 'init', null, null, null, 'class'),
({{aid}}, 'article', {{mid}}, 'module', '', '%s', '', 'import', 'from %s import', null, '%s', 'class');
""",
"""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
({{aid}}, 'article', {{pcid}}, 'class', '', 'queuetype', '', 'params', null, 'P', null, 'str'),
({{aid}}, 'article', {{pcid}}, 'class', '', 'timeout', '', 'params', null, '-1', null, 'int'),
({{aid}}, 'article', {{pcid}}, 'class', '', 'worknum', '', 'params', null, '6', null, 'int'),
({{aid}}, 'article', {{pcid}}, 'class', '', 'worktype', '', 'params', null, 'COROUTINE', null, 'str');
""",
"""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
({{aid}}, 'article', {{cid}}, 'class', '', '__init__', '', 'init', null, null, null, 'function'),
({{aid}}, 'article', {{cid}}, 'class', '%s', '%s', '', 'params', null, null, null, 'class');
""",
"""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
({{aid}}, 'article', {{fid}}, 'function', '', 'clsname', '', '=', null, 'self.__class__.__name__', null, 'object'),
({{aid}}, 'article', {{fid}}, 'function', '', 'tid', '', '=', null, 'tid', null, 'object'),
({{aid}}, 'article', {{fid}}, 'function', '', 'tid', '', 'params', null, '0', null, 'int');
"""
]

sections = ["""insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
    ({{sid}}, 'section', {{cid}}, 'class', '', '%s', '', 'init', null, null, null, 'function');
""",
"""
insert into `grab_datapath` (`id`, `bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
    ({{sid}}, 'section', {{fid}}, 'function', '{{next}}', 'next', '', '@', null, null, null, 'function');
    ({{sid}}, 'section', {{fid}}, 'function', '', 'initflow', '', '@', null, {{flow}}, null, 'str'),
    ({{sid}}, 'section', {{fid}}, 'function', '', 'index', '', '@', null, {{index}}, null, 'str'),
    ({{sid}}, 'section', {{fid}}, 'function', '', 'retry', '', '@', null, {{retry}}, null, 'int'),
    ({{sid}}, 'section', {{fid}}, 'function', '', 'timelimit', '', '@', null, {{timelimit}}, null, 'int'),
    ({{sid}}, 'section', {{fid}}, 'function', '', 'store', '', '@', null, {{store}}, null, 'None');
""",
"""
insert into `grab_datapath` (`id`, `bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
    ({{sid}}, 'section', {{fid}}, 'function', '', 'url', '', 'params', null, null, null, 'str');
"""
]

@withMysql(WDB, resutype='DICT', autocommit=True)
def newunit(uid):
    unit = dbpc.handler.queryOne(""" select * from grab_unit where id = %s """, (uid,))
    try:
        dbpc.handler.insert(units[0].replace('{{uid}}', str(uid)) % unit['filepath'].replace('.py', ''))
    except:
        pass
    mid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='unit' and sid = 0 """, (uid,))['id']
    try:
        dbpc.handler.insert(units[1].replace('{{uid}}', str(uid)).replace('{{mid}}', str(mid)) % (unit['name'].capitalize(), unit['name'].capitalize()))
    except:
        pass
    cid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='unit' and `name` = %s """, (uid, 'Spider%sOrigin' % unit['name'].capitalize()))['id']
    try:
        dbpc.handler.insert(units[2].replace('{{uid}}', str(uid)).replace('{{cid}}', str(cid)))
    except:
        pass
    fid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='unit' and `sid` = %s and `name` = '__init__' """, (uid, cid))['id']
    did = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='unit' and `sid` = %s and `name` = 'initDB' """, (uid, mid))['id']
    try:
        dbpc.handler.insert(units[3].replace('{{uid}}', str(uid)).replace('{{fid}}', str(fid)) % (did))
    except:
        pass

@withMysql(WDB, resutype='DICT', autocommit=True)
def newarticle(uid, aid):
    unit = dbpc.handler.queryOne(""" select * from grab_unit where id = %s """, (uid,))
    article = dbpc.handler.queryOne(""" select * from grab_article where id = %s """, (aid,))
    try:
        dbpc.handler.insert(articles[0].replace('{{aid}}', str(aid)) % article['filepath'].replace('.py', ''))
    except:
        pass
    mid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and sid = 0 """, (aid,))['id']
    try:
        dbpc.handler.insert(articles[1].replace('{{aid}}', str(aid)).replace('{{mid}}', str(mid)) % (unit['filepath'].replace('.py', ''), 'Spider%s' % article['name'].capitalize(), 'Spider%sOrigin' % unit['name'].capitalize(), unit['filepath'].replace('.py', ''), 'Spider%sOrigin' % unit['name'].capitalize()))
    except:
        pass
    pcid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and `pid`='' and `name` = %s """, (aid, 'Spider%sOrigin' % unit['name'].capitalize()))['id']
    try:
        dbpc.handler.insert(articles[2].replace('{{aid}}', str(aid)).replace('{{pcid}}', str(pcid)))
    except:
        pass
    cid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and `name` = %s """, (aid, 'Spider%s' % article['name'].capitalize()))['id']
    try:
        dbpc.handler.insert(articles[3].replace('{{aid}}', str(aid)).replace('{{cid}}', str(cid)) % (pcid, 'Spider%sOrigin' % unit['name'].capitalize()))
    except:
        pass
    fid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and `sid` = %s and `name` = '__init__' """, (aid, cid))['id']
    try:
        dbpc.handler.insert(articles[4].replace('{{aid}}', str(aid)).replace('{{fid}}', str(fid)))
    except:
        pass

@withMysql(WDB, resutype='DICT', autocommit=True)
def newsection(uid, aid, sid):
    unit = dbpc.handler.queryOne(""" select * from grab_unit where id = %s """, (uid,))
    article = dbpc.handler.queryOne(""" select * from grab_article where id = %s """, (aid,))
    section = dbpc.handler.queryOne(""" select * from grab_section where id = %s """, (sid,))
    source = dbpc.handler.queryAll(""" select * from grab_datasource where sid = %s """, (sid,))
    extract = dbpc.handler.queryAll(""" select * from grab_dataextract where sid = %s """, (sid,))
    cid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and `name` = %s """, (aid, 'Spider%s' % article['name'].capitalize()))['id']
    try:
        print sections[0].replace('{{sid}}', str(sid)).replace('{{cid}}', str(cid)) % ('fetch%s%s' % (section['flow'].upper(), section['name'].capitalize()))
        dbpc.handler.insert(sections[0].replace('{{sid}}', str(sid)).replace('{{cid}}', str(cid)) % ('fetch%s%s' % (section['flow'].upper(), section['name'].capitalize())))
    except:
        pass
    fid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='section' and `name` = %s """, (sid, 'fetch%s%s' % (section['flow'].upper(), section['name'].capitalize())))['id']
    try:
        sql = sections[1].replace('{{sid}}', str(sid)).replace('{{fid}}', str(fid))
        sql = sql.replace('{{flow}}', section['flow'] and "'%s'" % section['flow'] or 'null')
        sql = sql.replace('{{index}}', section['index'] and "'%s'" % section['index'] or 'null')
        sql = sql.replace('{{retry}}', section['retry'] and "'%s'" % section['retry'] or 'null')
        sql = sql.replace('{{timelimit}}', section['timelimit'] and "'%s'" % section['timelimit'] or 'null')
        sql = sql.replace('{{store}}', section['store'] and "'%s'" % section['store'] or 'null')
        print sql
        dbpc.handler.insert(sql)
    except:
        pass
    try:
        print sections[2].replace('{{sid}}', str(sid)).replace('{{fid}}', str(fid))
        dbpc.handler.insert(sections[2].replace('{{sid}}', str(sid)).replace('{{fid}}', str(fid)))
    except:
        pass

if __name__ == '__main__':
    # newunit(12)
    # makeunit(1)
    # newarticle({{sid}}, 3)
    # makearticle(3)
    print 'eee'
    newsection(1, 1, 1)
    print 'dddd'
