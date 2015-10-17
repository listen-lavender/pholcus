#!/usr/bin/python
# coding=utf-8
import time
from webcrawl.godhand import cook
from datakit.mysql.suit import withMysql, dbpc
from task.config.db.mysql import RDB, WDB
from task.model.mysql import initDB
# from do import makeunit, makearticle

initDB()

initsqls = ["""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
    (0, 'article', 0, 'module', '', 'datetime', '', 'import', 'from datetime import', null, 'datetime', 'datetime'),
    (0, 'article', 0, 'module', '', 'ensureurl', '', 'import', 'from webcrawl.handleRequest import', null, 'ensureurl', 'function'),
    (0, 'article', 0, 'module', '', 'getHtmlNodeContent', '', 'import', 'from webcrawl.handleRequest import', null, 'getHtmlNodeContent', 'function'),
    (0, 'article', 0, 'module', '', 'getJsonNodeContent', '', 'import', 'from webcrawl.handleRequest import', null, 'getJsonNodeContent', 'function'),
    (0, 'article', 0, 'module', '', 'getXmlNodeContent', '', 'import', 'from webcrawl.handleRequest import', null, 'getXmlNodeContent', 'function'),
    (0, 'article', 0, 'module', '', 'index', '', 'import', 'from webcrawl.work import', null, 'index', 'function'),
    (0, 'article', 0, 'module', '', 'initflow', '', 'import', 'from webcrawl.work import', null, 'initflow', 'function'),
    (0, 'article', 0, 'module', '', 'mongo', '', 'import', 'from task.config.db.mongo import', null, '_DBCONN', 'dict'),
    (0, 'article', 0, 'module', '', 'mysql', '', 'import', 'from task.config.db.mysql import', null, '_DBCONN', 'dict'),
    (0, 'article', 0, 'module', '', 'next', '', 'import', 'from webcrawl.work import', null, 'next', 'function'),
    (0, 'article', 0, 'module', '', 'parturl', '', 'import', 'from webcrawl.handleRequest import', null, 'parturl', 'function'),
    (0, 'article', 0, 'module', '', 'requGet', '', 'import', 'from webcrawl.handleRequest import', null, 'requGet', 'function'),
    (0, 'article', 0, 'module', '', 'requPost', '', 'import', 'from webcrawl.handleRequest import', null, 'requPost', 'function'),
    (0, 'article', 0, 'module', '', 'retry', '', 'import', 'from webcrawl.work import', null, 'retry', 'function'),
    (0, 'article', 0, 'module', '', 'store', '', 'import', 'from webcrawl.work import', null, 'store', 'function'),
    (0, 'article', 0, 'module', '', 'timedelta', '', 'import', 'from datetime import', null, 'timedelta', 'function'),
    (0, 'article', 0, 'module', '', 'timelimit', '', 'import', 'from webcrawl.work import', null, 'timelimit', 'function'),
    (0, 'article', 0, 'module', '', 'TIMEOUT', '', 'import', 'from task.config.web.hotel import', null, 'TIMEOUT', 'int'),
    (0, 'article', 0, 'module', '', 'withMongo', '', 'import', 'from datakit.mongo.suit import', null, 'withMongo', 'function'),
    (0, 'article', 0, 'module', '', 'withMysql', '', 'import', 'from datakit.mysql.suit import', null, 'withMysql', 'function'),
    (0, 'unit', 0, 'module', '', 'SpiderOrigin', '', 'import', 'from webcrawl.spider import', null, 'SpiderOrigin', 'class');
""",
"""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
    (0, 'unit', {{cid}}, 'class', '', 'queuetype', '', 'params', null, 'P', null, 'str'),
    (0, 'unit', {{cid}}, 'class', '', 'timeout', '', 'params', null, '-1', null, 'int'),
    (0, 'unit', {{cid}}, 'class', '', 'worknum', '', 'params', null, '6', null, 'int'),
    (0, 'unit', {{cid}}, 'class', '', 'worktype', '', 'params', null, 'COROUTINE', null, 'str');
"""
]

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
  ({{uid}}, 'unit', {{cid}}, 'class', '{{bcid}}', 'SpiderOrigin', '', 'params', null, null, null, 'class'),
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
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
    ({{sid}}, 'section', {{fid}}, 'function', '', 'next', '', '@', null, null, null, 'function'),
    ({{sid}}, 'section', {{fid}}, 'function', '', 'initflow', '', '@', null, {{flow}}, null, 'str'),
    ({{sid}}, 'section', {{fid}}, 'function', '', 'index', '', '@', null, {{index}}, null, 'str'),
    ({{sid}}, 'section', {{fid}}, 'function', '', 'retry', '', '@', null, {{retry}}, null, 'int'),
    ({{sid}}, 'section', {{fid}}, 'function', '', 'timelimit', '', '@', null, {{timelimit}}, null, 'int'),
    ({{sid}}, 'section', {{fid}}, 'function', '{{store}}', 'store', '', '@', null, null, null, '%s');
""",
"""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
    ({{sid}}, 'section', {{fid}}, 'function', '', 'url', '', 'params', null, null, null, 'str');
"""
,
"""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
    ({{sid}}, 'section', {{fid}}, 'function', '{{mid}}', '%s', '', '=', null, null, null, 'execute');
"""
,
"""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
    ({{sid}}, 'section', '{{peid}}', 'execute', '{{puid}}', 'url', '', 'params', null, 'url', null, 'object');

"""
,
"""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
    ({{sid}}, 'section', {{prid}}, 'execute', '', 'timeout', '', 'params', null, '%s', null, 'int'),
    ({{sid}}, 'section', {{prid}}, 'execute', '', 'format', '', 'params', null, '%s', null, 'str'),
    ({{sid}}, 'section', {{prid}}, 'execute', '{{puid}}', 'url', '', 'params', null, null, null, 'str');
""",
"""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
    ({{sid}}, 'section', {{fid}}, 'function', '{{prid}}', '%s', '', '%s', '%s', null, null, 'list');
"""
,
"""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
    ({{sid}}, 'section', {{plid}}, 'list', '{{plid}}', 'one', '', 'in', null, null, null, 'object');
""",
"""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
    ({{sid}}, 'section', {{boid}}, '%s', '{{poid}}', '%s', '', '%s', %s, null, '%s', 'str');
""",
"""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
    ({{sid}}, 'section', {{boid}}, '%s', '{{trid}}', '%s', '', 'yield', null, null, null, '%s');
""",

"""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
    ({{sid}}, 'section', {{poid}}, 'object', '{{esid}}', '%s', '', '=', null, null, null, 'execute');
""",
"""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
    ({{sid}}, 'section', {{trid}}, 'execute', '{{puid}}', 'refurl', '', 'params', null, '%s', null, 'object'),
    ({{sid}}, 'section', {{trid}}, 'execute', '{{pdid}}', 'objurl', '', 'params', null, '%s', null, 'object');
""",
"""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
    ({{sid}}, 'section', {{boid}}, '%s', '{{poid}}', '%s', '', '%s', %s, %s, null, '%s');
""",
"""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
    ({{sid}}, 'section', {{fid}}, 'function', '{{ptid}}', 'rqp', '', '=', null, null, null, 'execute');
""",
"""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
    ({{sid}}, 'section', {{fdb1}}, 'function', '{{fdb2}}', '', '', 'params', '["use"]["wdb"]', null, null, 'execute');
""",
"""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
    ({{sid}}, 'section', {{fsid}}, 'execute', '', 'method', '', 'params', null, 'MANY', null, 'str'),
    ({{sid}}, 'section', {{fsid}}, 'execute', '', 'update', '', 'params', null, 'True', null, 'bool'),
    ({{sid}}, 'section', {{fsid}}, 'execute', '{{mcid}}', 'way', '', 'params', '.insert', null, null, 'method'),
    ({{sid}}, 'section', {{fsid}}, 'execute', '{{dbid}}', 'db', '', 'params', null, null, null, 'execute');
"""
]

@withMysql(WDB, resutype='DICT', autocommit=True)
def init():
    try:
        dbpc.handler.insert(initsqls[0])
    except:
        pass
    cid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = 0 and btype='unit' and `name` = 'SpiderOrigin'; """)['id']
    try:
        dbpc.handler.insert(initsqls[1].replace('{{cid}}', str(cid)))
    except:
        pass

init()

@withMysql(WDB, resutype='DICT', autocommit=True)
def seeunit(uid):
    unit = dbpc.handler.queryOne(""" select * from grab_unit where id = %s """, (uid,))
    try:
        dbpc.handler.insert(units[0].replace('{{uid}}', str(uid)) % unit['filepath'].replace('.py', ''))
    except:
        raise
    mid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='unit' and sid = 0 """, (uid,))['id']
    try:
        dbpc.handler.insert(units[1].replace('{{uid}}', str(uid)).replace('{{mid}}', str(mid)) % (unit['name'].capitalize(), unit['name'].capitalize()))
    except:
        raise
    bcid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = 0 and btype='unit' and `name` = 'SpiderOrigin'; """)['id']
    cid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='unit' and `name` = %s """, (uid, 'Spider%sOrigin' % unit['name'].capitalize()))['id']
    try:
        dbpc.handler.insert(units[2].replace('{{uid}}', str(uid)).replace('{{cid}}', str(cid)).replace('{{bcid}}', str(bcid)))
    except:
        raise
    fid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='unit' and `sid` = %s and `name` = '__init__' """, (uid, cid))['id']
    did = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='unit' and `sid` = %s and `name` = 'initDB' """, (uid, mid))['id']
    try:
        dbpc.handler.insert(units[3].replace('{{uid}}', str(uid)).replace('{{fid}}', str(fid)) % (did))
    except:
        raise

@withMysql(WDB, resutype='DICT', autocommit=True)
def seearticle(uid, aid):
    unit = dbpc.handler.queryOne(""" select * from grab_unit where id = %s """, (uid,))
    article = dbpc.handler.queryOne(""" select * from grab_article where id = %s """, (aid,))
    try:
        dbpc.handler.insert(articles[0].replace('{{aid}}', str(aid)) % article['filepath'].replace('.py', ''))
    except:
        raise
    mid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and sid = 0 """, (aid,))['id']
    try:
        dbpc.handler.insert(articles[1].replace('{{aid}}', str(aid)).replace('{{mid}}', str(mid)) % (unit['filepath'].replace('.py', ''), 'Spider%s' % article['name'].capitalize(), 'Spider%sOrigin' % unit['name'].capitalize(), unit['filepath'].replace('.py', ''), 'Spider%sOrigin' % unit['name'].capitalize()))
    except:
        raise
    pcid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and `pid`='' and `name` = %s """, (aid, 'Spider%sOrigin' % unit['name'].capitalize()))['id']
    try:
        dbpc.handler.insert(articles[2].replace('{{aid}}', str(aid)).replace('{{pcid}}', str(pcid)))
    except:
        raise
    cid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and `name` = %s """, (aid, 'Spider%s' % article['name'].capitalize()))['id']
    try:
        dbpc.handler.insert(articles[3].replace('{{aid}}', str(aid)).replace('{{cid}}', str(cid)) % (pcid, 'Spider%sOrigin' % unit['name'].capitalize()))
    except:
        raise
    fid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and `sid` = %s and `name` = '__init__' """, (aid, cid))['id']
    try:
        dbpc.handler.insert(articles[4].replace('{{aid}}', str(aid)).replace('{{fid}}', str(fid)))
    except:
        raise

@withMysql(WDB, resutype='DICT', autocommit=True)
def seesection(uid, aid, sid):
    unit = dbpc.handler.queryOne(""" select * from grab_unit where id = %s """, (uid,))
    article = dbpc.handler.queryOne(""" select * from grab_article where id = %s """, (aid,))
    section = dbpc.handler.queryOne(""" select * from grab_section where id = %s """, (sid,))
    source = dbpc.handler.queryAll(""" select * from grab_datasource where sid = %s """, (sid,))
    extract = dbpc.handler.queryAll(""" select * from grab_dataextract where sid = %s """, (sid,))
    print """ select * from grab_datapath where bid = %s and btype='article' and `name` = %s """ % (aid, 'Spider%s' % article['name'].capitalize())
    cid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and `name` = %s """, (aid, 'Spider%s' % article['name'].capitalize()))['id']
    try:
        print sections[0].replace('{{sid}}', str(sid)).replace('{{cid}}', str(cid)) % ('fetch%s%s' % (section['flow'].upper(), section['name'].capitalize()))
        dbpc.handler.insert(sections[0].replace('{{sid}}', str(sid)).replace('{{cid}}', str(cid)) % ('fetch%s%s' % (section['flow'].upper(), section['name'].capitalize())))
    except:
        raise
    fid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='section' and `name` = %s """, (sid, 'fetch%s%s' % (section['flow'].upper(), section['name'].capitalize())))['id']
    try:
        presection = dbpc.handler.queryOne(""" select * from grab_section where aid = %s and next_id = %s """, (section['aid'], section['id']))
        if section['store']:
            section['store'] = dbpc.handler.queryOne(""" select * from grab_datapath where bid = 0 and btype='article' and `name` = 'store' """)['id']
        else:
            section['store'] = None
        if presection is not None:
            section['flow'] = None
            dbpc.handler.update(""" update grab_datapath set pid = '%d' where bid = %d and btype='section' and `name`='next' and pid = '' """ % (fid, presection['id']))
        #     puname = dbpc.handler.queryOne(""" select * from grab_dataextract where sid = %s and parameter = 1 """ % (presection['id']))['name']
        # else:
        #     puname = 'url'
        sql = sections[1].replace('{{sid}}', str(sid)).replace('{{fid}}', str(fid))
        sql = sql.replace('{{flow}}', section['flow'] and "'%s'" % section['flow'] or 'null')
        sql = sql.replace('{{index}}', section['index'] and "'%s'" % section['index'] or 'null')
        sql = sql.replace('{{retry}}', section['retry'] and "'%s'" % section['retry'] or 'null')
        sql = sql.replace('{{timelimit}}', section['timelimit'] and "'%s'" % section['timelimit'] or 'null')
        sql = sql.replace('{{store}}', section['store'] and "%s" % section['store'] or '')
        sql = sql % (section['store'] and 'execute' or 'None')
        print sql
        dbpc.handler.insert(sql)
    except:
        raise
    try:
        print sections[2].replace('{{sid}}', str(sid)).replace('{{fid}}', str(fid))
        dbpc.handler.insert(sections[2].replace('{{sid}}', str(sid)).replace('{{fid}}', str(fid)))
    except:
        raise
    print """select * from grab_datapath where method='params' and sid = %s and `name` = 'url' """, (fid, )
    puid = dbpc.handler.queryOne(""" select * from grab_datapath where method='params' and sid = %s and `name` = 'url' """, (fid, ))['id']
    print '>>>>', puid
    prid = None
    for s in source:
        if s['method'] == 'parameter' and s['format'] == 'PARAMETER':
            ptid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = 0 and `btype` = 'article' and `name` = 'parturl'; """)['id']
            try:
                dbpc.handler.insert(sections[13].replace('{{sid}}', str(sid)).replace('{{fid}}', str(fid)).replace('{{ptid}}', str(ptid)))
            except:
                raise
            peid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and `btype` = 'section' and `sid` = %s and `name` = 'rqp'; """, (sid, fid))['id']
            try:
                print sections[4].replace('{{sid}}', str(sid)).replace('{{peid}}', str(peid)).replace('{{puid}}', str(puid))
                dbpc.handler.insert(sections[4].replace('{{sid}}', str(sid)).replace('{{peid}}', str(peid)).replace('{{puid}}', str(puid)))
            except:
                raise
        else:
            print """ select * from grab_datapath where bid = 0 and btype='article' and `name` = %s """, ('requ%s' % s['method'].capitalize(), )
            mid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = 0 and btype='article' and `name` = %s """, ('requ%s' % s['method'].capitalize(), ))['id']
            try:
                print sections[3].replace('{{sid}}', str(sid)).replace('{{fid}}', str(fid)).replace('{{mid}}', str(mid)) % s['name']
                dbpc.handler.insert(sections[3].replace('{{sid}}', str(sid)).replace('{{fid}}', str(fid)).replace('{{mid}}', str(mid)) % s['name'])
            except:
                raise
            prid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype = 'section' and sid = %s and stype = 'function' and `name` = %s; """, (sid, fid, s['name']))['id']
            try:
                print sections[5].replace('{{sid}}', str(sid)).replace('{{fid}}', str(fid)).replace('{{prid}}', str(prid)).replace('{{puid}}', str(puid)) % (str(s['timeout']), s['format'])
                dbpc.handler.insert(sections[5].replace('{{sid}}', str(sid)).replace('{{fid}}', str(fid)).replace('{{prid}}', str(prid)).replace('{{puid}}', str(puid)) % (str(s['timeout']), s['format']))
            except:
                raise
    for e in extract:
        if e['method'] == '.findall':
            try:
                s = dbpc.handler.queryOne(""" select * from grab_datasource where id = %s """, (e['dsid'],))
                prid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype = 'section' and sid = %s and stype = 'function' and `name` = %s; """, (sid, fid, s['name']))['id']
                print sections[6].replace('{{sid}}', str(sid)).replace('{{fid}}', str(fid)).replace('{{prid}}', str(prid)) % (e['name'], '%s' % e['method'], e['path'].replace("'", '"'))
                dbpc.handler.insert(sections[6].replace('{{sid}}', str(sid)).replace('{{fid}}', str(fid)).replace('{{prid}}', str(prid)) % (e['name'], '%s' % e['method'], e['path'].replace("'", '"')))
            except:
                raise
            try:
                plid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype = 'section' and sid = %s and stype = 'function' and `pid` = %s; """, (sid, fid, prid))['id']
                print sections[7].replace('{{sid}}', str(sid)).replace('{{plid}}', str(plid))
                dbpc.handler.insert(sections[7].replace('{{sid}}', str(sid)).replace('{{plid}}', str(plid)))
            except:
                raise
        elif e['method'] == '.find':
            boid = None
            if e['pdeid'] > 0:
                pe = dbpc.handler.queryOne(""" select * from grab_dataextract where id = %s """, (e['pdeid'],))
                ps = dbpc.handler.queryOne(""" select * from grab_datasource where id = %s """, (pe['dsid'],))
                if pe['method'] == '.findall':
                    prid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype = 'section' and sid = %s and stype = 'function' and `name` = %s; """, (sid, fid, ps['name']))['id']
                    plid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype = 'section' and sid = %s and stype = 'function' and `pid` = %s; """, (sid, fid, prid))['id']
                    poid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype = 'section' and sid = %s and stype = 'list' and `pid` = %s; """, (sid, plid, plid))['id']
                    boid = poid
                    btype = 'object'
                else:
                    poid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype = 'section' and sid = %s and stype = 'function' and `name` = %s; """, (sid, fid, ps['name']))['id']
            else:
                ps = dbpc.handler.queryOne(""" select * from grab_datasource where id = %s """, (e['dsid'],))
                poid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype = 'section' and sid = %s and stype = 'function' and `name` = %s; """, (sid, fid, ps['name']))['id']
            if boid is None:
                if e['store'] == 1:
                    bo = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='section' and `method`='yield' """, (sid,))
                    mcid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and `name`='Data' """, (aid,))['id']
                    if bo is None:
                        try:
                            print sections[9].replace('{{sid}}', str(sid)).replace('{{boid}}', str(fid)).replace('{{trid}}', str(mcid)) % ('function', '', 'object')
                            dbpc.handler.insert(sections[9].replace('{{sid}}', str(sid)).replace('{{boid}}', str(fid)).replace('{{trid}}', str(mcid)) % ('function', '', 'object'))
                        except:
                            raise
                    boid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='section' and `method`='yield' """, (sid,))['id']
                    fsid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='section' and `name`='store' and `method` = '@' """, (sid,))['id']
                    fdb1 = dbpc.handler.queryOne(""" select * from grab_datapath where bid = 0 and btype='article' and `name`='withMysql' """)['id']
                    fdb2 = dbpc.handler.queryOne(""" select * from grab_datapath where bid = 0 and btype='article' and `name`='mysql' """)['id']
                    # fdb3 = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and `name`='Data' """, (aid))['id']
                    try:
                        print sections[14].replace('{{sid}}', str(sid)).replace('{{fdb1}}', str(fdb1)).replace('{{fdb2}}', str(fdb2))
                        dbpc.handler.insert(sections[14].replace('{{sid}}', str(sid)).replace('{{fdb1}}', str(fdb1)).replace('{{fdb2}}', str(fdb2)))
                    except:
                        pass
                    dbid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='section' and `xpath` = '["use"]["wdb"]'; """, (sid, ))['id']
                    try:
                        print sections[15].replace('{{sid}}', str(sid)).replace('{{fsid}}', str(fsid)).replace('{{mcid}}', str(mcid)).replace('{{dbid}}', str(dbid))
                        dbpc.handler.insert(sections[15].replace('{{sid}}', str(sid)).replace('{{fsid}}', str(fsid)).replace('{{mcid}}', str(mcid)).replace('{{dbid}}', str(dbid)))
                    except:
                        pass
                    btype = 'object'
                else:
                    boid = fid
                    btype = 'function'
            try:
                print sections[8].replace('{{sid}}', str(sid)).replace('{{boid}}', str(boid)).replace('{{poid}}', str(poid)) % (btype, e['name'], '%s' % e['method'], e['path'] == '.' and 'null' or "'%s'" % e['path'].replace("'", '"'), e['content'].replace("'", '"'))
                dbpc.handler.insert(sections[8].replace('{{sid}}', str(sid)).replace('{{boid}}', str(boid)).replace('{{poid}}', str(poid)) % (btype, e['name'], '%s' % e['method'], e['path'] == '.' and 'null' or "'%s'" % e['path'].replace("'", '"'), e['content'].replace("'", '"')))
            except:
                raise
            if e['parameter'] == 1:
                print '________'
                try:
                    esid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = 0 and btype = 'article' and `name` = 'ensureurl'; """)['id']
                    print sections[10].replace('{{sid}}', str(sid)).replace('{{poid}}', str(poid)).replace('{{esid}}', str(esid)) % e['name']
                    dbpc.handler.insert(sections[10].replace('{{sid}}', str(sid)).replace('{{poid}}', str(poid)).replace('{{esid}}', str(esid)) % e['name'])
                except:
                    raise
                trid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype = 'section' and `sid` = %s and pid = %s; """, (sid, poid, esid))['id']
                try:
                    pdid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype = 'section' and `sid` = %s and `pid` = %s; """, (sid, poid, poid))['id']
                    print sections[11].replace('{{sid}}', str(sid)).replace('{{trid}}', str(trid)).replace('{{puid}}', str(puid)).replace('{{pdid}}', str(pdid)) % ('url', e['name'])
                    dbpc.handler.insert(sections[11].replace('{{sid}}', str(sid)).replace('{{trid}}', str(trid)).replace('{{puid}}', str(puid)).replace('{{pdid}}', str(pdid)) % ('url', e['name']))
                except:
                    raise
                try:
                    print sections[9].replace('{{sid}}', str(sid)).replace('{{boid}}', str(boid)).replace('{{trid}}', str(trid)) % (btype, e['name'], 'str')
                    dbpc.handler.insert(sections[9].replace('{{sid}}', str(sid)).replace('{{boid}}', str(boid)).replace('{{trid}}', str(trid)) % (btype, e['name'], 'str'))
                except:
                    raise
        else:
            if e['store'] == 1:
                bo = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='section' and `method`='yield' """, (sid,))
                mcid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and `name`='Data' """, (aid,))['id']
                if bo is None:
                    print '>>>>>>>>>'
                    try:
                        print sections[9].replace('{{sid}}', str(sid)).replace('{{boid}}', str(fid)).replace('{{trid}}', str(mcid)) % ('function', '', 'object')
                        dbpc.handler.insert(sections[9].replace('{{sid}}', str(sid)).replace('{{boid}}', str(fid)).replace('{{trid}}', str(mcid)) % ('function', '', 'object'))
                    except:
                        raise
                boid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='section' and `method`='yield' """, (sid,))['id']
                fsid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='section' and `name`='store' and `method` = '@' """, (sid,))['id']
                fdb1 = dbpc.handler.queryOne(""" select * from grab_datapath where bid = 0 and btype='article' and `name`='withMysql' """)['id']
                fdb2 = dbpc.handler.queryOne(""" select * from grab_datapath where bid = 0 and btype='article' and `name`='mysql' """)['id']
                # fdb3 = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and `name`='Data' """, (aid))['id']
                try:
                    print sections[14].replace('{{sid}}', str(sid)).replace('{{fdb1}}', str(fdb1)).replace('{{fdb2}}', str(fdb2))
                    dbpc.handler.insert(sections[14].replace('{{sid}}', str(sid)).replace('{{fdb1}}', str(fdb1)).replace('{{fdb2}}', str(fdb2)))
                except:
                    pass
                dbid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='section' and `xpath` = '["use"]["wdb"]'; """, (sid, ))['id']
                try:
                    print sections[15].replace('{{sid}}', str(sid)).replace('{{fsid}}', str(fsid)).replace('{{mcid}}', str(mcid)).replace('{{dbid}}', str(dbid))
                    dbpc.handler.insert(sections[15].replace('{{sid}}', str(sid)).replace('{{fsid}}', str(fsid)).replace('{{mcid}}', str(mcid)).replace('{{dbid}}', str(dbid)))
                except:
                    pass
                btype = 'object'
            else:
                boid = fid
                btype = 'function'
            if e['path'] == 'self.tid':
                poid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and `default`='tid' """, (aid,))['id']
                xpath = 'null'
                default = 'null'
            elif e['dsid'] > 0:
                s = dbpc.handler.queryOne(""" select * from grab_datasource where sid = %s and `id` = %s """, (sid, e['dsid']))
                if s['format'] == 'PARAMETER':
                    poid = dbpc.handler.queryOne(""" select * from grab_datapath where bid = %s and `btype` = 'section' and `sid` = %s and `name` = 'rqp'; """, (sid, fid))['id']
                else:
                    poid = ''
                xpath = "'%s'" % e['path']
                default = 'null'
            else:
                poid = ''
                xpath = 'null'
                default = "'%s'" % e['path']
            try:
                print sections[12].replace('{{sid}}', str(sid)).replace('{{boid}}', str(boid)).replace('{{poid}}', str(poid)) % (btype, e['name'], e['method'], xpath, default, e['content'])
                dbpc.handler.insert(sections[12].replace('{{sid}}', str(sid)).replace('{{boid}}', str(boid)).replace('{{poid}}', str(poid)) % (btype, e['name'], e['method'], xpath, default, e['content']))
            except:
                raise

if __name__ == '__main__':
    seeunit(1)
    seearticle(1, 1)
    seesection(1, 1, 1)
    seesection(1, 1, 2)
    seesection(1, 1, 3)
    print 'dddd'
