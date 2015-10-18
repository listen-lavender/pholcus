#!/usr/bin/python
# coding=utf-8
from godhand import cook
from datakit.mysql.suit import withMysql, dbpc

WDB = 'local'
RDB = 'local'
_DBCONN = {"host": "127.0.0.1",
                "port": 3306,
                "user": "root",
                "passwd": "",
                "db": "kuaijie",
                "charset": "utf8",
                "use_unicode":False
            }

def initDB():
    dbpc.addDB(RDB, LIMIT, host=_DBCONN['host'],
                port=_DBCONN['port'],
                user=_DBCONN['user'],
                passwd=_DBCONN['passwd'],
                db=_DBCONN['db'],
                charset=_DBCONN['charset'],
                use_unicode=_DBCONN['use_unicode'],
                override=False)
    dbpc.addDB(WDB, LIMIT, host=_DBCONN['host'],
                port=_DBCONN['port'],
                user=_DBCONN['user'],
                passwd=_DBCONN['passwd'],
                db=_DBCONN['db'],
                charset=_DBCONN['charset'],
                use_unicode=_DBCONN['use_unicode'],
                override=False)

initDB()

def ensure(filepath):
    if filepath.startswith('/'):
        if not os.path.exists(os.path.split(filepath)[0]):
            os.mkdir(os.path.split(filepath)[0])
    else:
        filepath = os.path.join(os.path.split(os.path.abspath(__file__))[0], filepath)
        if not os.path.exists(os.path.split(filepath)[0]):
            os.mkdir(os.path.split(filepath)[0])
    return filepath

@withMysql(WDB, resutype='DICT')
def makeunit(uid):
    dirfile = dbpc.handler.queryOne(""" select gu.dmid, gu.name, concat(gc.val, gu.dirpath, gu.filepath) as filepath from grab_unit gu join grab_config gc on gc.type='ROOT' and gc.key ='dir' where gu.id = %s; """, (uid,))
    material = {}
    print """ select gd.* from grab_datapath gd where gd.btype='unit' and (gd.bid = %s or gd.bid=0); """, (uid, )
    for one in dbpc.handler.queryAll(""" select gd.* from grab_datapath gd where gd.btype='unit' and (gd.bid = %s or gd.bid=0); """, (uid, )):
        material[str(one['id'])] = one
    fi = open(ensure(dirfile['filepath']), 'w')
    fi.write(cook(material))
    fi.close()

@withMysql(WDB, resutype='DICT')
def makearticle(aid, flow):
    dirfile = dbpc.handler.queryOne(""" select gu.dmid, gu.name, concat(gc.val, gu.dirpath, ga.filepath) as filepath from grab_unit gu join grab_config gc join grab_article ga on gc.type='ROOT' and gc.key ='dir' and ga.uid =gu.id where ga.id = %s; """, (aid,))
    material = {}
    sids = ','.join([str(one['id']) for one in dbpc.handler.queryAll(""" select * from grab_section where aid = %s and flow = %s """, (aid, flow))])
    print """ select * from grab_datapath where (btype = 'article' and (bid=0 or bid = %s)) or (btype='section' and bid in (%s)); """ % (str(aid), sids)
    for one in dbpc.handler.queryAll(""" select * from grab_datapath where (btype = 'article' and (bid=0 or bid = %s)) or (btype='section' and bid in (%s)); """ % (str(aid), sids)):
        material[str(one['id'])] = one
    fi = open(ensure(dirfile['filepath']), 'w')
    fi.write(cook(material))
    fi.close()

@withMysql(WDB, resutype='DICT')
def initScript():
    for u in dbpc.handler.queryAll(""" select * from grab_unit; """):
        makeunit(u['id'])
        for a in dbpc.handler.queryAll(""" select * from grab_article where uid = %s; """, (u['id'])):
            for f in dbpc.handler.queryAll(""" select distinct flow from grab_section where aid = %s; """, a['id']):
                makearticle(a['id'], f['flow'])

if __name__ == '__main__':
    print 'start'
    makeunit(1)
    makearticle(1, 'www')
    print 'end'