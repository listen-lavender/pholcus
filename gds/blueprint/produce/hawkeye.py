#!/usr/bin/env python
# coding=utf-8

initsqls = ["""
insert into `grab_datapath` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`, `method`, `xpath`, `default`, `content`, `datatype`)
values
    (0, 'article', 0, 'module', '', 'datetime', '', 'import', 'from datetime import', null, 'datetime', 'datetime'),
    (0, 'article', 0, 'module', '', 'ensureurl', '', 'import', 'from webcrawl.request import', null, 'ensureurl', 'function'),
    (0, 'article', 0, 'module', '', 'getHtmlNodeContent', '', 'import', 'from webcrawl.request import', null, 'getHtmlNodeContent', 'function'),
    (0, 'article', 0, 'module', '', 'getJsonNodeContent', '', 'import', 'from webcrawl.request import', null, 'getJsonNodeContent', 'function'),
    (0, 'article', 0, 'module', '', 'getXmlNodeContent', '', 'import', 'from webcrawl.request import', null, 'getXmlNodeContent', 'function'),
    (0, 'article', 0, 'module', '', 'index', '', 'import', 'from webcrawl.task import', null, 'index', 'function'),
    (0, 'article', 0, 'module', '', 'initflow', '', 'import', 'from webcrawl.task import', null, 'initflow', 'function'),
    (0, 'article', 0, 'module', '', 'mongo', '', 'import', 'from task.config.db.mongo import', null, '_DBCONN', 'dict'),
    (0, 'article', 0, 'module', '', 'mysql', '', 'import', 'from task.config.db.mysql import', null, '_DBCONN', 'dict'),
    (0, 'article', 0, 'module', '', 'next', '', 'import', 'from webcrawl.task import', null, 'next', 'function'),
    (0, 'article', 0, 'module', '', 'parturl', '', 'import', 'from webcrawl.request import', null, 'parturl', 'function'),
    (0, 'article', 0, 'module', '', 'get', '', 'import', 'from webcrawl.request import', null, 'get', 'function'),
    (0, 'article', 0, 'module', '', 'post', '', 'import', 'from webcrawl.request import', null, 'post', 'function'),
    (0, 'article', 0, 'module', '', 'retry', '', 'import', 'from webcrawl.task import', null, 'retry', 'function'),
    (0, 'article', 0, 'module', '', 'store', '', 'import', 'from webcrawl.task import', null, 'store', 'function'),
    (0, 'article', 0, 'module', '', 'timedelta', '', 'import', 'from datetime import', null, 'timedelta', 'function'),
    (0, 'article', 0, 'module', '', 'timelimit', '', 'import', 'from webcrawl.task import', null, 'timelimit', 'function'),
    (0, 'article', 0, 'module', '', 'TIMEOUT', '', 'import', 'from task.config.web.hotel import', null, 'TIMEOUT', 'int'),
    (0, 'article', 0, 'module', '', 'withMongo', '', 'import', 'from dbskit.mongo.suit import', null, 'withMongo', 'function'),
    (0, 'article', 0, 'module', '', 'withMysql', '', 'import', 'from dbskit.mysql.suit import', null, 'withMysql', 'function'),
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
  ({{uid}}, 'unit', {{mid}}, 'module', '', 'withDB', '', 'import', 'from dbskit.mysql.suit import', null, 'withMysql', 'decorator'),
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

def init(baseConn):
    try:
        baseConn.handler.insert(initsqls[0]);
    except:
        pass
    cid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = 0 and btype='unit' and `name` = 'SpiderOrigin'; """)['_id']
    try:
        baseConn.handler.insert(initsqls[1].replace('{{cid}}', str(cid)))
    except:
        pass

def seeunit(baseConn, uid):
    unit = baseConn.handler.queryOne(""" select * from grab_unit where id = %s """, (uid,))
    try:
        baseConn.handler.insert(units[0].replace('{{uid}}', str(uid)) % unit['filepath'].replace('.py', ''))
    except:
        raise
    mid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='unit' and sid = 0 """, (uid,))['_id']
    try:
        baseConn.handler.insert(units[1].replace('{{uid}}', str(uid)).replace('{{mid}}', str(mid)) % (unit['name'].capitalize(), unit['name'].capitalize()))
    except:
        raise
    bcid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = 0 and btype='unit' and `name` = 'SpiderOrigin'; """)['_id']
    cid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='unit' and `name` = %s """, (uid, 'Spider%sOrigin' % unit['name'].capitalize()))['_id']
    try:
        baseConn.handler.insert(units[2].replace('{{uid}}', str(uid)).replace('{{cid}}', str(cid)).replace('{{bcid}}', str(bcid)))
    except:
        raise
    fid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='unit' and `sid` = %s and `name` = '__init__' """, (uid, cid))['_id']
    did = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='unit' and `sid` = %s and `name` = 'initDB' """, (uid, mid))['_id']
    try:
        baseConn.handler.insert(units[3].replace('{{uid}}', str(uid)).replace('{{fid}}', str(fid)) % (did))
    except:
        raise

def seearticle(baseConn, uid, aid):
    unit = baseConn.handler.queryOne(""" select * from grab_unit where id = %s """, (uid,))
    article = baseConn.handler.queryOne(""" select * from grab_article where id = %s """, (aid,))
    try:
        baseConn.handler.insert(articles[0].replace('{{aid}}', str(aid)) % article['filepath'].replace('.py', ''))
    except:
        raise
    mid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and sid = 0 """, (aid,))['_id']
    try:
        baseConn.handler.insert(articles[1].replace('{{aid}}', str(aid)).replace('{{mid}}', str(mid)) % (unit['filepath'].replace('.py', ''), 'Spider%s' % article['name'].capitalize(), 'Spider%sOrigin' % unit['name'].capitalize(), unit['filepath'].replace('.py', ''), 'Spider%sOrigin' % unit['name'].capitalize()))
    except:
        raise
    pcid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and `pid`='' and `name` = %s """, (aid, 'Spider%sOrigin' % unit['name'].capitalize()))['_id']
    try:
        baseConn.handler.insert(articles[2].replace('{{aid}}', str(aid)).replace('{{pcid}}', str(pcid)))
    except:
        raise
    cid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and `name` = %s """, (aid, 'Spider%s' % article['name'].capitalize()))['_id']
    try:
        baseConn.handler.insert(articles[3].replace('{{aid}}', str(aid)).replace('{{cid}}', str(cid)) % (pcid, 'Spider%sOrigin' % unit['name'].capitalize()))
    except:
        raise
    fid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and `sid` = %s and `name` = '__init__' """, (aid, cid))['_id']
    try:
        baseConn.handler.insert(articles[4].replace('{{aid}}', str(aid)).replace('{{fid}}', str(fid)))
    except:
        raise

def clearsection(baseConn, sid):
    baseConn.handler.queryOne(""" delete from grab_datapath where btype='section' and bid = %d; """ % int(sid))

def seesection(baseConn, aid, sid):
    clearsection(baseConn, sid)
    article = baseConn.handler.queryOne(""" select * from grab_article where id = %s """, (aid,))
    section = baseConn.handler.queryOne(""" select * from grab_section where id = %s """, (sid,))
    source = baseConn.handler.queryAll(""" select * from grab_datasource where sid = %s """, (sid,))
    extract = baseConn.handler.queryAll(""" select * from grab_dataextract where sid = %s """, (sid,))
    print """ select * from grab_datapath where bid = %s and btype='article' and `name` = %s """ % (aid, 'Spider%s' % article['name'].capitalize())
    cid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and `name` = %s """, (aid, 'Spider%s' % article['name'].capitalize()))['_id']
    try:
        print sections[0].replace('{{sid}}', str(sid)).replace('{{cid}}', str(cid)) % ('fetch%s%s' % (section['flow'].upper(), section['name'].capitalize()))
        baseConn.handler.insert(sections[0].replace('{{sid}}', str(sid)).replace('{{cid}}', str(cid)) % ('fetch%s%s' % (section['flow'].upper(), section['name'].capitalize())))
    except:
        raise
    fid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='section' and `name` = %s """, (sid, 'fetch%s%s' % (section['flow'].upper(), section['name'].capitalize())))['_id']
    try:
        presection = baseConn.handler.queryOne(""" select * from grab_section where aid = %s and next_id = %s """, (section['aid'], section['_id']))
        if section['store']:
            section['store'] = baseConn.handler.queryOne(""" select * from grab_datapath where bid = 0 and btype='article' and `name` = 'store' """)['_id']
        else:
            section['store'] = None
        if presection is not None:
            section['flow'] = None
            baseConn.handler.update(""" update grab_datapath set pid = '%d' where bid = %d and btype='section' and `name`='next' and pid = '' """ % (fid, presection['_id']))
        #     puname = baseConn.handler.queryOne(""" select * from grab_dataextract where sid = %s and parameter = 1 """ % (presection['_id']))['name']
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
        baseConn.handler.insert(sql)
    except:
        raise
    try:
        print sections[2].replace('{{sid}}', str(sid)).replace('{{fid}}', str(fid))
        baseConn.handler.insert(sections[2].replace('{{sid}}', str(sid)).replace('{{fid}}', str(fid)))
    except:
        raise
    print """select * from grab_datapath where method='params' and sid = %s and `name` = 'url' """, (fid, )
    puid = baseConn.handler.queryOne(""" select * from grab_datapath where method='params' and sid = %s and `name` = 'url' """, (fid, ))['_id']
    print '>>>>', puid
    prid = None
    for s in source:
        if s['method'] == 'parameter' and s['format'] == 'PARAMETER':
            ptid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = 0 and `btype` = 'article' and `name` = 'parturl'; """)['_id']
            try:
                baseConn.handler.insert(sections[13].replace('{{sid}}', str(sid)).replace('{{fid}}', str(fid)).replace('{{ptid}}', str(ptid)))
            except:
                raise
            peid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and `btype` = 'section' and `sid` = %s and `name` = 'rqp'; """, (sid, fid))['_id']
            try:
                print sections[4].replace('{{sid}}', str(sid)).replace('{{peid}}', str(peid)).replace('{{puid}}', str(puid))
                baseConn.handler.insert(sections[4].replace('{{sid}}', str(sid)).replace('{{peid}}', str(peid)).replace('{{puid}}', str(puid)))
            except:
                raise
        else:
            print """ select * from grab_datapath where bid = 0 and btype='article' and `name` = %s """, ('requ%s' % s['method'].capitalize(), )
            mid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = 0 and btype='article' and `name` = %s """, ('requ%s' % s['method'].capitalize(), ))['_id']
            try:
                print sections[3].replace('{{sid}}', str(sid)).replace('{{fid}}', str(fid)).replace('{{mid}}', str(mid)) % s['name']
                baseConn.handler.insert(sections[3].replace('{{sid}}', str(sid)).replace('{{fid}}', str(fid)).replace('{{mid}}', str(mid)) % s['name'])
            except:
                raise
            prid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype = 'section' and sid = %s and stype = 'function' and `name` = %s; """, (sid, fid, s['name']))['_id']
            try:
                print sections[5].replace('{{sid}}', str(sid)).replace('{{fid}}', str(fid)).replace('{{prid}}', str(prid)).replace('{{puid}}', str(puid)) % (str(s['timeout']), s['format'])
                baseConn.handler.insert(sections[5].replace('{{sid}}', str(sid)).replace('{{fid}}', str(fid)).replace('{{prid}}', str(prid)).replace('{{puid}}', str(puid)) % (str(s['timeout']), s['format']))
            except:
                raise
    for e in extract:
        if e['method'] == '.findall':
            try:
                s = baseConn.handler.queryOne(""" select * from grab_datasource where id = %s """, (e['dsid'],))
                prid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype = 'section' and sid = %s and stype = 'function' and `name` = %s; """, (sid, fid, s['name']))['_id']
                print sections[6].replace('{{sid}}', str(sid)).replace('{{fid}}', str(fid)).replace('{{prid}}', str(prid)) % (e['name'], '%s' % e['method'], e['path'].replace("'", '"'))
                baseConn.handler.insert(sections[6].replace('{{sid}}', str(sid)).replace('{{fid}}', str(fid)).replace('{{prid}}', str(prid)) % (e['name'], '%s' % e['method'], e['path'].replace("'", '"')))
            except:
                raise
            try:
                plid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype = 'section' and sid = %s and stype = 'function' and `pid` = %s; """, (sid, fid, prid))['_id']
                print sections[7].replace('{{sid}}', str(sid)).replace('{{plid}}', str(plid))
                baseConn.handler.insert(sections[7].replace('{{sid}}', str(sid)).replace('{{plid}}', str(plid)))
            except:
                raise
        elif e['method'] == '.find':
            boid = None
            if e['pdeid'] > 0:
                pe = baseConn.handler.queryOne(""" select * from grab_dataextract where id = %s """, (e['pdeid'],))
                ps = baseConn.handler.queryOne(""" select * from grab_datasource where id = %s """, (pe['dsid'],))
                if pe['method'] == '.findall':
                    prid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype = 'section' and sid = %s and stype = 'function' and `name` = %s; """, (sid, fid, ps['name']))['_id']
                    plid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype = 'section' and sid = %s and stype = 'function' and `pid` = %s; """, (sid, fid, prid))['_id']
                    poid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype = 'section' and sid = %s and stype = 'list' and `pid` = %s; """, (sid, plid, plid))['_id']
                    boid = poid
                    btype = 'object'
                else:
                    poid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype = 'section' and sid = %s and stype = 'function' and `name` = %s; """, (sid, fid, ps['name']))['_id']
            else:
                ps = baseConn.handler.queryOne(""" select * from grab_datasource where id = %s """, (e['dsid'],))
                poid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype = 'section' and sid = %s and stype = 'function' and `name` = %s; """, (sid, fid, ps['name']))['_id']
            if boid is None:
                if e['store'] == 1:
                    bo = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='section' and `method`='yield' """, (sid,))
                    mcid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and `name`='Data' """, (aid,))['_id']
                    if bo is None:
                        try:
                            print sections[9].replace('{{sid}}', str(sid)).replace('{{boid}}', str(fid)).replace('{{trid}}', str(mcid)) % ('function', '', 'object')
                            baseConn.handler.insert(sections[9].replace('{{sid}}', str(sid)).replace('{{boid}}', str(fid)).replace('{{trid}}', str(mcid)) % ('function', '', 'object'))
                        except:
                            raise
                    boid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='section' and `method`='yield' """, (sid,))['_id']
                    fsid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='section' and `name`='store' and `method` = '@' """, (sid,))['_id']
                    fdb1 = baseConn.handler.queryOne(""" select * from grab_datapath where bid = 0 and btype='article' and `name`='withMysql' """)['_id']
                    fdb2 = baseConn.handler.queryOne(""" select * from grab_datapath where bid = 0 and btype='article' and `name`='mysql' """)['_id']
                    # fdb3 = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and `name`='Data' """, (aid))['_id']
                    try:
                        print sections[14].replace('{{sid}}', str(sid)).replace('{{fdb1}}', str(fdb1)).replace('{{fdb2}}', str(fdb2))
                        baseConn.handler.insert(sections[14].replace('{{sid}}', str(sid)).replace('{{fdb1}}', str(fdb1)).replace('{{fdb2}}', str(fdb2)))
                    except:
                        pass
                    dbid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='section' and `xpath` = '["use"]["wdb"]'; """, (sid, ))['_id']
                    try:
                        print sections[15].replace('{{sid}}', str(sid)).replace('{{fsid}}', str(fsid)).replace('{{mcid}}', str(mcid)).replace('{{dbid}}', str(dbid))
                        baseConn.handler.insert(sections[15].replace('{{sid}}', str(sid)).replace('{{fsid}}', str(fsid)).replace('{{mcid}}', str(mcid)).replace('{{dbid}}', str(dbid)))
                    except:
                        pass
                    btype = 'object'
                else:
                    boid = fid
                    btype = 'function'
            try:
                print sections[8].replace('{{sid}}', str(sid)).replace('{{boid}}', str(boid)).replace('{{poid}}', str(poid)) % (btype, e['name'], '%s' % e['method'], e['path'] == '.' and 'null' or "'%s'" % e['path'].replace("'", '"'), e['content'].replace("'", '"'))
                baseConn.handler.insert(sections[8].replace('{{sid}}', str(sid)).replace('{{boid}}', str(boid)).replace('{{poid}}', str(poid)) % (btype, e['name'], '%s' % e['method'], e['path'] == '.' and 'null' or "'%s'" % e['path'].replace("'", '"'), e['content'].replace("'", '"')))
            except:
                raise
            if e['parameter'] == 1:
                print '________'
                try:
                    esid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = 0 and btype = 'article' and `name` = 'ensureurl'; """)['_id']
                    print sections[10].replace('{{sid}}', str(sid)).replace('{{poid}}', str(poid)).replace('{{esid}}', str(esid)) % e['name']
                    baseConn.handler.insert(sections[10].replace('{{sid}}', str(sid)).replace('{{poid}}', str(poid)).replace('{{esid}}', str(esid)) % e['name'])
                except:
                    raise
                trid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype = 'section' and `sid` = %s and pid = %s; """, (sid, poid, esid))['_id']
                try:
                    pdid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype = 'section' and `sid` = %s and `pid` = %s; """, (sid, poid, poid))['_id']
                    print sections[11].replace('{{sid}}', str(sid)).replace('{{trid}}', str(trid)).replace('{{puid}}', str(puid)).replace('{{pdid}}', str(pdid)) % ('url', e['name'])
                    baseConn.handler.insert(sections[11].replace('{{sid}}', str(sid)).replace('{{trid}}', str(trid)).replace('{{puid}}', str(puid)).replace('{{pdid}}', str(pdid)) % ('url', e['name']))
                except:
                    raise
                try:
                    print sections[9].replace('{{sid}}', str(sid)).replace('{{boid}}', str(boid)).replace('{{trid}}', str(trid)) % (btype, e['name'], 'str')
                    baseConn.handler.insert(sections[9].replace('{{sid}}', str(sid)).replace('{{boid}}', str(boid)).replace('{{trid}}', str(trid)) % (btype, e['name'], 'str'))
                except:
                    raise
        else:
            if e['store'] == 1:
                bo = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='section' and `method`='yield' """, (sid,))
                mcid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and `name`='Data' """, (aid,))['_id']
                if bo is None:
                    print '>>>>>>>>>'
                    try:
                        print sections[9].replace('{{sid}}', str(sid)).replace('{{boid}}', str(fid)).replace('{{trid}}', str(mcid)) % ('function', '', 'object')
                        baseConn.handler.insert(sections[9].replace('{{sid}}', str(sid)).replace('{{boid}}', str(fid)).replace('{{trid}}', str(mcid)) % ('function', '', 'object'))
                    except:
                        raise
                boid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='section' and `method`='yield' """, (sid,))['_id']
                fsid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='section' and `name`='store' and `method` = '@' """, (sid,))['_id']
                fdb1 = baseConn.handler.queryOne(""" select * from grab_datapath where bid = 0 and btype='article' and `name`='withMysql' """)['_id']
                fdb2 = baseConn.handler.queryOne(""" select * from grab_datapath where bid = 0 and btype='article' and `name`='mysql' """)['_id']
                # fdb3 = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and `name`='Data' """, (aid))['_id']
                try:
                    print sections[14].replace('{{sid}}', str(sid)).replace('{{fdb1}}', str(fdb1)).replace('{{fdb2}}', str(fdb2))
                    baseConn.handler.insert(sections[14].replace('{{sid}}', str(sid)).replace('{{fdb1}}', str(fdb1)).replace('{{fdb2}}', str(fdb2)))
                except:
                    pass
                dbid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='section' and `xpath` = '["use"]["wdb"]'; """, (sid, ))['_id']
                try:
                    print sections[15].replace('{{sid}}', str(sid)).replace('{{fsid}}', str(fsid)).replace('{{mcid}}', str(mcid)).replace('{{dbid}}', str(dbid))
                    baseConn.handler.insert(sections[15].replace('{{sid}}', str(sid)).replace('{{fsid}}', str(fsid)).replace('{{mcid}}', str(mcid)).replace('{{dbid}}', str(dbid)))
                except:
                    pass
                btype = 'object'
            else:
                boid = fid
                btype = 'function'
            if e['path'] == 'self.tid':
                poid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and btype='article' and `default`='tid' """, (aid,))['_id']
                xpath = 'null'
                default = 'null'
            elif e['dsid'] > 0:
                s = baseConn.handler.queryOne(""" select * from grab_datasource where sid = %s and `id` = %s """, (sid, e['dsid']))
                if s['format'] == 'PARAMETER':
                    poid = baseConn.handler.queryOne(""" select * from grab_datapath where bid = %s and `btype` = 'section' and `sid` = %s and `name` = 'rqp'; """, (sid, fid))['_id']
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
                baseConn.handler.insert(sections[12].replace('{{sid}}', str(sid)).replace('{{boid}}', str(boid)).replace('{{poid}}', str(poid)) % (btype, e['name'], e['method'], xpath, default, e['content']))
            except:
                raise

if __name__ == '__main__':
    print 'start...'
    # seeunit(1)
    # seearticle(1, 1)
    # seesection(1, 1, 1)
    # seesection(1, 1, 2)
    # seesection(1, 1, 3)
    print 'end...'
