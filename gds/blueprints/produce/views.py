#!/usr/bin/python
# coding=utf8
import json
from datakit.mysql.suit import withMysql, dbpc, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template

produce = Blueprint('produce', __name__, template_folder='templates')

model = {}

@produce.route('/datamodel/list', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def modellist():
    datamodels = dbpc.handler.queryAll(""" select * from grab_datamodel; """)
    return render_template('datamodellist.html', datamodels=datamodels)

@produce.route('/datamodel/detail/<dmid>', methods=['GET', 'POST'])
@withMysql(WDB, resutype='DICT', autocommit=True)
def modeldetail(dmid=None):
    rows = ['id', 'name', 'autocreate', 'iscreated', 'status', 'extra', 'creator', 'updator', 'create_time', 'update_time']
    cols = ['id', 'dmid', 'name', 'default', 'nullable', 'unique']
    # rows = ['id', 'name', 'comment', 'autocreate', 'iscreated', 'status', 'extra', 'creator', 'updator', 'create_time', 'update_time']
    # cols = ['id', 'dmid', 'name', 'comment', 'default', 'nullable', 'unique']
    adds = ['ditype','ddl']
    rowvals = dbpc.handler.queryOne(""" select {{s}} from grab_datamodel where id = %s """.replace("{{s}}", ','.join(''.join(('`', one, '`')) for one in rows)), (dmid or '', )) or dict(zip(rows, ['' for one in rows]))
    colvals = dbpc.handler.queryAll(""" select {{s}} from grab_dataitem where dmid = %s; """.replace("{{s}}", ','.join(''.join(('`', one, '`')) for one in cols)), (rowvals['id'], ))
    for col in colvals:
        # colvals[col]['datatypes'] = dbpc.handler.queryAll(""" select %s from grab_datatype where diid = %s; """, (','.join(''.join(('`', one, '`')) for one in adds), colvals[col]['id']))
        del col['dmid']
    cols.remove('dmid')
    cols.remove('id')
    rows.remove('id')
    return render_template('datamodeldetail.html', rows=rows, cols=cols, rowvals=unicode2utf8(rowvals), colvals=unicode2utf8(colvals), colspan=len(cols)-1)

@produce.route('/unit/list', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def unitlist():
    units = dbpc.handler.queryAll(""" select gu.id, gu.name as unit_name, gdm.name as datamodel_name from grab_unit gu join grab_datamodel gdm on gu.dmid = gdm.id; """)
    return render_template('unitlist.html', units=units)

@produce.route('/unit/detail/<uid>', methods=['GET', 'POST'])
@withMysql(WDB, resutype='DICT', autocommit=True)
def unitdetail(uid=None):
    unit = dbpc.handler.queryOne(""" select * from grab_unit where id = %s; """, uid)
    return render_template('unitdetail.html', unit=unit)

@produce.route('/article/list', methods=['GET'])
@produce.route('/article/list/<uid>', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def articlelist(uid=None):
    uid = uid or ''
    articles = dbpc.handler.queryAll(""" select `id`, `name`, `filepath` from grab_article where uid = %s or '' = %s; """, (uid, uid))
    return render_template('articlelist.html', articles=articles)

@produce.route('/article/detail/<aid>', methods=['GET', 'POST'])
@withMysql(WDB, resutype='DICT', autocommit=True)
def articledetail(aid=None):
    article = dbpc.handler.queryOne(""" select * from grab_article where id = %s; """, aid)
    return render_template('articledetail.html', article=article)

@produce.route('/section/list', methods=['GET'])
@produce.route('/section/list/<aid>', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def sectionlist(aid=None):
    aid = aid or None
    sections = dbpc.handler.queryAll(""" select `id`, `name` from grab_section where aid = %s or ''=%s; """, (aid, aid))
    return render_template('sectionlist.html', sections=sections)

@produce.route('/section/detail/<sid>', methods=['GET', 'POST'])
@withMysql(WDB, resutype='DICT', autocommit=True)
def sectiondetail(sid=None):
    if request.method == 'GET':
        section = dbpc.handler.queryOne(""" select * from grab_section where id = %s; """, sid)
        return render_template('sectiondetail.html', section=section)
    elif request.method == 'POST':
        rt = request.args.get('rf', '/section/list')
        return redirect(rt)
    elif request.method == 'DELETE':
        rt = request.args.get('rf', '/section/list')
        return redirect(rt)
    else:
        pass

@produce.route('/task/list', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def tasklist():
    tasks = dbpc.handler.queryAll(""" select * from grab_task; """)
    return render_template('tasklist.html', tasks=tasks)

@produce.route('/task/detail/<tid>', methods=['GET', 'POST', 'DELETE'])
@withMysql(WDB, resutype='DICT', autocommit=True)
def taskdetail(tid=None):
    if request.method == 'GET':
        task = dbpc.handler.queryOne(""" select * from grab_task where id = %s; """, tid)
        return render_template('taskdetail.html', task=task)
    elif request.method == 'POST':
        rt = request.args.get('rf', '/task/list')
        return redirect(rt)
    elif request.method == 'DELETE':
        rt = request.args.get('rf', '/task/list')
        return redirect(rt)
    else:
        pass
    
@produce.route('/db/list', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def dblist():
    # info = {'status':1, 'desc':'成功', 'result':[]}
    dbs = dbpc.handler.queryAll(""" select distinct gc1.name, concat(gc2.val, gc1.filepath) "filepath", gc1.extra from grab_config gc1 join grab_config gc2 on gc1.type = gc2.name where gc1.type= 'db' and gc2.type='CONFIG' and gc2.key='dir' order by gc1.name; """)
    for i in dbs:
        i['dbl'] = []
        for j in dbpc.handler.queryAll(""" select gc1.id, gc1.key, gc1.val from grab_config gc1 join grab_config gc2 on gc1.type = gc2.name where gc1.type= 'db' and gc2.type='CONFIG' and gc2.key='dir' and gc1.name = %s order by gc1.name; """, (i['name'],)):
            if j['key'] == 'use':
                use = json.loads(j['val'])
                use['id'] = j['id']
                i.update(use)
            else:
                i['dbl'].append({'id':j['id'], 'key':j['key']})
    # info['result'] = dbs
    # return json.dumps(info, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return render_template('dblist.html', dbs=dbs)

@produce.route('/db/detail/<dbid>', methods=['GET', 'POST', 'DELETE'])
@withMysql(WDB, resutype='DICT', autocommit=True)
def dbdetail(dbid=None):
    if request.method == 'GET':
        db = dbpc.handler.queryOne(""" select gc1.id, gc1.name, gc1.key, concat(gc2.val, gc1.filepath) "filepath", gc1.extra, gc1.val from grab_config gc1 join grab_config gc2 on gc1.type = gc2.name where gc1.type= 'db' and gc2.type='CONFIG' and gc2.key='dir' and gc1.id = %s order by gc1.name; """, (dbid,))
        print db['val']
        db.update(json.loads(db['val']))
        del db['val']
        print db
        return render_template('dbdetail.html', db=db)
    elif request.method == 'POST':
        rt = request.args.get('rf', '/task/list')
        return redirect(rt)
    elif request.method == 'DELETE':
        rt = request.args.get('rf', '/task/list')
        return redirect(rt)
    else:
        pass
    