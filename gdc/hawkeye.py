#!/usr/bin/python
# coding=utf-8
import time, datetime
import os
from optparse import OptionParser
from datakit.mysql.suit import withMysql, dbpc
from godhand import cook
import task

LIMIT = 20
WDB = 'local'
RDB = 'local'
_DBCONN = {"host": "127.0.0.1",
                "port": 3306,
                "user": "root",
                "passwd": "",
                "db": "pholcus",
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

models = ["""#!/usr/bin/python
# coding=utf-8

from datakit.mysql.orm import Model, Field
from datakit.mysql.suit import dbpc
from task.config.db.mysql import RDB, WDB, LIMIT, _DBCONN, USE

def initDB():
    dbpc.addDB(RDB, LIMIT, host=_DBCONN[USE]['host'],
                port=_DBCONN[USE]['port'],
                user=_DBCONN[USE]['user'],
                passwd=_DBCONN[USE]['passwd'],
                db=_DBCONN[USE]['db'],
                charset=_DBCONN[USE]['charset'],
                use_unicode=_DBCONN[USE]['use_unicode'],
                override=False)
    dbpc.addDB(WDB, LIMIT, host=_DBCONN[USE]['host'],
                port=_DBCONN[USE]['port'],
                user=_DBCONN[USE]['user'],
                passwd=_DBCONN[USE]['passwd'],
                db=_DBCONN[USE]['db'],
                charset=_DBCONN[USE]['charset'],
                use_unicode=_DBCONN[USE]['use_unicode'],
                override=False)
""",
"""
class Hotel(Model):
    __table__ = 'hotelinfo'
    hotel_id = Field(ddl='varchar(20)', unique='uq_official')
    hotel_type = Field(ddl='varchar(10)', unique='uq_official')
    hotel_name = Field(ddl='varchar(50)')

    address = Field(ddl='varchar(256)')
    lat = Field(ddl='varchar(50)')
    lnt = Field(ddl='varchar(50)')

    tel = Field(ddl='varchar(100)')
    logo = Field(ddl='varchar(256)')
    status = Field(ddl='tinyint(1)')

    create_time = Field(ddl='datetime')
    update_time = Field(ddl='timestamp')
    tid = Field(ddl='int(11)')
"""
]

config = """#!/usr/bin/python
# coding=utf-8

LIMIT = 20
USE = 'local'
WDB = 'local'
RDB = 'local'
_DBCONN = {"local":{"host": "127.0.0.1",
                "port": 3306,
                "user": "root",
                "passwd": "",
                "db": "dandan-jiang",
                "charset": "utf8",
                "use_unicode":False,},
            "use":{
                "rdb":"local",
                "wdb":"local"}
            }

"""

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
def getUnit(uid):
    dirfile = dbpc.handler.queryOne(""" select gu.dmid, gu.name, concat(gc.val, gu.dirpath, gu.filepath) as filepath from grab_unit gu join grab_config gc on gc.type='ROOT' and gc.key ='dir' where gu.id = %s; """, (uid,))
    material = {}
    print """ select gd.* from grab_datapath gd where gd.btype='unit' and (gd.bid = %s or gd.bid=0); """, (uid, )
    for one in dbpc.handler.queryAll(""" select gd.* from grab_datapath gd where gd.btype='unit' and (gd.bid = %s or gd.bid=0); """, (uid, )):
        material[str(one['id'])] = one
    fi = open(ensure(dirfile['filepath']), 'w')
    fi.write(cook(material))
    fi.close()

@withMysql(WDB, resutype='DICT')
def getArticle(aid, flow):
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
    for u in dbpc.handler.queryAll(""" select * from grab_unit where distribute = 'SC'; """):
        getUnit(u['id'])
        for a in dbpc.handler.queryAll(""" select * from grab_article where uid = %s and distribute = 'SC'; """, (u['id'])):
            for f in dbpc.handler.queryAll(""" select distinct flow from grab_section where aid = %s and distribute = 'SC'; """, a['id']):
                getArticle(a['id'], f['flow'])

def initConfig():
    fi = open('task/config/db/mysql.py', 'w')
    fi.write(config)
    fi.close()

def initModel():
    fi = open('task/model/mysql.py', 'w')
    fi.write('\n'.join(models))
    fi.close()

@withMysql(WDB, resutype='DICT', autocommit=True)
def setModel(filepath):
    print filepath
    fi = open(filepath, 'r')
    data = fi.read()
    fi.close()
    for txt in data.split('@'):
        if 'comment(' in txt:
            comment = None
            model = None
            for line in txt.split('\n'):
                if 'comment' in line:
                    info = line.replace('(', '').replace(')', '').split("'")
                    comment = info[1]
                if 'class' in line:
                    info = line.replace('(', ' ').replace(')', '').replace(',', '').split(' ')
                    model = info[1].lower()
                    break
            if model is not None:
                if dbpc.handler.queryOne(""" select * from grab_datamodel where name = %s """, (model,)):
                    continue
                dbpc.handler.insert("""insert into grab_datamodel(`name`, `table`, `comment`, `autocreate`, `iscreated`, `status`, `extra`, `creator`, `updator`, `create_time`)
                                                           values(    %s,      %s,        %s,           1,      1,   1, null, 0, 0, now()) """, (model, model, comment))

@withMysql(WDB, resutype='DICT', autocommit=True)
def setUnit(filepath, comment):
    name = filepath[filepath.rindex('/')+1:].replace('spider.py', '')
    u = dbpc.handler.queryOne(""" select * from grab_unit where `name` = %s """, (name, ))
    if u is None:
        dmid = None
        fi = open(filepath, 'r')
        for one in fi.readlines():
            if 'as Data' in one:
                model = one.replace('as Data', '').split('import')[-1].strip().lower()
                dmid = dbpc.handler.queryOne(""" select id from grab_datamodel where name = %s """, (model,)).get('id')
                break
        fi.close()
        dirpath = name + '/'
        filepath = filepath[filepath.rindex('/')+1:]
        extra = comment
        create_time = datetime.datetime.now()
        dbpc.handler.insert(""" insert into grab_unit(`dmid`, `name`, `dirpath`, `filepath`, `extra`, `creator`, `updator`, `create_time`) values(%s, %s, %s, %s, %s, 0, 0, now()) """, (dmid, name, dirpath, filepath, extra))
        print 'Unit is set successfully.'
    else:
        print 'Unit has been set.'

@withMysql(WDB, resutype='DICT', autocommit=True)
def setArticle(filepath, pinyin, host):
    u = None
    for one in os.listdir(os.path.dirname(filepath)):
        if one.endswith('spider.py'):
            u = dbpc.handler.queryOne(""" select * from grab_unit where `name` = %s """, (one.replace('spider.py', ''), ))
            break
    if u is None:
        print 'Please set unit firstly.'
    else:
        name = host.split('.')
        if len(name) > 2:
            name = name[1]
        else:
            name = name[0]
        article = dbpc.handler.queryOne(""" select * from grab_article where `name` = %s and uid = %s """, (name, u['id']))
        sections = []
        flows = []
        fi = open(filepath, 'r')
        flag = False
        for line in fi.readlines():
            if '@' in line and not 'find' in line and not 'findall' in line:
                sections.append(line.replace('\n', '').replace('  ', ''))
                flag = True
            if 'def ' in line and flag:
                sections.append(line.replace('\n', '').replace('  ', ''))
                flag = False
            if 'initflow' in line and not 'import' in line:
                flows.append(line.replace('\n', '').replace('  ', '').replace('@initflow(', '').replace(')', '').replace('"', '').replace("'", ''))
        fi.close()
        if article is None:
            create_time = datetime.datetime.now()
            dbpc.handler.insert(""" insert into grab_article(`uid`, `name`, `pinyin`, `host`, `filepath`, `create_time`) values(%s, %s, %s, %s, %s, %s) """, (u['id'], name, pinyin, host, filepath[filepath.rindex('/')+1:], create_time))
            article = dbpc.handler.queryOne(""" select * from grab_article where `name` = %s and uid = %s """, (name, u['id']))
            section = {}
            flow = ''
            for index, one in enumerate(sections):
                if 'next' in one:
                    if flows[0] in one.lower():
                        flow = flows[0]
                        flows.remove(flows[0])
                    section['next_id'] = dbpc.handler.queryOne(""" select id from grab_section where `name` = %s and aid = %s """, (one.replace('@next(', '').replace(')', ''), article['id']))['id']
                if 'index' in one:
                    section['index'] = one.replace('@index(', '').replace(')', '')
                if 'retry' in one:
                    section['retry'] = one.replace('@retry(', '').replace(')', '')
                if 'timelimit' in one:
                    section['timelimit'] = one.replace('@timelimit(', '').replace(')', '')
                if 'store' in one:
                    section['store'] = 1
                if 'def ' in one:
                    if flows and flows[0] in one.lower():
                        flow = flows[0]
                        flows.remove(flows[0])
                    section_name = one.replace('def ', '').split('(')[0]
                    step = len(sections) - index
                    dbpc.handler.insert(""" insert into grab_section(`aid`,`next_id`,`name`,`flow`,`step`,`index`,`retry`,`timelimit`,`store`,`distribute`,`creator`,`updator`,`create_time`)
                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """, (article['id'], section.get('next_id'), section_name, flow, step, section.get('index'), section.get('retry', 0), section.get('timelimit', 30), section.get('store', 0), 'SN', 0, 0, datetime.datetime.now()))
                    section = {}
            print 'Article is set successfully.'
        else:
            section = {}
            flow = ''
            for index, one in enumerate(sections):
                if 'next' in one:
                    if flows and flows[0] in one.lower():
                        flow = flows[0]
                        flows.remove(flows[0])
                    section['next_id'] = dbpc.handler.queryOne(""" select id from grab_section where `name` = %s and aid = %s and flow = %s limit 1 """, (one.replace('@next(', '').replace(')', ''), article['id'], flow))['id']
                if 'index' in one:
                    section['index'] = one.replace('@index(', '').replace(')', '')
                if 'retry' in one:
                    section['retry'] = one.replace('@retry(', '').replace(')', '')
                if 'timelimit' in one:
                    section['timelimit'] = one.replace('@timelimit(', '').replace(')', '')
                if 'store' in one:
                    section['store'] = 1
                if 'def ' in one:
                    if flows and flows[0] in one.lower():
                        flow = flows[0]
                        flows.remove(flows[0])
                    section_name = one.replace('def ', '').split('(')[0]
                    step = len(sections) - index
                    if dbpc.handler.queryOne(""" select * from grab_section where `name` = %s and aid = %s and flow = %s limit 1 """, (section_name, article['id'], flow)) is None:
                        dbpc.handler.insert(""" insert into grab_section(`aid`,`next_id`,`name`,`flow`,`step`,`index`,`retry`,`timelimit`,`store`,`distribute`,`creator`,`updator`,`create_time`)
                        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """, (article['id'], section.get('next_id'), section_name, flow, step, section.get('index'), section.get('retry', 0), section.get('timelimit', 30), section.get('store', 0), 'SN', 0, 0, datetime.datetime.now()))
                    section = {}
            print 'Article has been set.'

if __name__ == '__main__':
    getUnit(1)
    getArticle(1, 'www')