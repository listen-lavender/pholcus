#!/usr/bin/python
# coding=utf-8
import time
from webcrawl.godhand import cook
from datakit.mysql.suit import withMysql, dbpc
from task.config.db.mysql import RDB, WDB
from task.model.mysql import initDB

initDB()
    
@withMysql(WDB, resutype='DICT')
def u():
    dirfile = dbpc.handler.queryOne(""" select gu.dmid, gu.name, concat(gc.val, gu.dirpath, gu.filepath) as filepath from grab_unit gu join grab_config gc on gc.type='ROOT' and gc.key ='dir' where gu.name = 'hotel'; """)
    material = {}
    for one in dbpc.handler.queryAll(""" select gd.* from grab_datapath gd where (gd.btype='unit' and (gd.bid = 1 or gd.bid=0)) or gd.sid in (select gd.id from grab_datapath gd where gd.btype='unit' and gd.bid = 1) order by gd.pid asc, gd.id asc; """):
        material[str(one['id'])] = one
    fi = open(dirfile['filepath'], 'w')
    fi.write(cook(material))
    fi.close()

@withMysql(WDB, resutype='DICT')
def a():
    dirfile = dbpc.handler.queryOne(""" select gu.dmid, gu.name, concat(gc.val, gu.dirpath, ga.filepath) as filepath from grab_unit gu join grab_config gc join grab_article ga on gc.type='ROOT' and gc.key ='dir' and ga.uid =gu.id where gu.name = 'hotel' and ga.name = 'homeinns'; """)
    material = {}
    for one in dbpc.handler.queryAll(""" select gd.* from grab_datapath gd where gd.id > 16; """):
        material[str(one['id'])] = one
    fi = open(dirfile['filepath'], 'w')
    fi.write(cook(material))
    fi.close()

if __name__ == '__main__':
    print 'start'
    # u()
    a()
    print 'end'