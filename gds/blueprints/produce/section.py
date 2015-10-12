#!/usr/bin/python
# coding=utf8
import json
from datakit.mysql.suit import withMysql, dbpc, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template
from views import produce

# @produce.route('/section/list', methods=['GET'])
# @produce.route('/section/list/<aid>', methods=['GET'])
# @withMysql(RDB, resutype='DICT')
# def sectionlist(aid):
#     pagetotal = int(request.args.get('pagetotal', 10))
#     page = int(request.args.get('page', 1))
#     total = int(request.args.get('total', 0))
#     if total == 0:
#         total = dbpc.handler.queryOne(""" select count(id) as total from grab_section where aid = %s or '' = %s; """, (aid, aid))['total']
#     count = (total - 1)/pagetotal + 1
#     sections = dbpc.handler.queryAll(""" select `id`, `name` from grab_section where aid = %s or ''=%s; """, (aid, aid))
#     return render_template('sectionlist.html', aid=aid, sections=sections, pagetotal=pagetotal, page=page, total=total, count=count)

@produce.route('/section/list/<aid>', methods=['GET', 'POST', 'DELETE'])
@withMysql(RDB, resutype='DICT')
def sectionlist(aid):
    """
    select gs.id, gs.aid, gs.name, gs.flow, gs.index, gs.retry, gs.timelimit, gs.store, gsp.id, gsp.aid, gsp.name, gsp.flow, gsp.index, gsp.retry, gsp.timelimit, gsp.store
    from grab_section gs join grab_section gsp
    on gs.next_id = gsp.id
     where gs.flow = 'www';
    """
    if request.method == 'GET':
        flows = dbpc.handler.queryAll(""" select distinct flow from grab_section where aid = %s; """, (aid, ))
        sections = {}
        for flow in flows:
            sections[flow['flow']] = []
            for section in dbpc.handler.queryAll(""" select gs.id, gs.aid, gs.name, gs.flow, gs.index, gs.retry, gs.timelimit, gs.store, gsp.id as pid, gsp.aid as paid, gsp.name as pname, gsp.flow as pflow, gsp.index as pindex, gsp.retry as pretry, gsp.timelimit as ptimelimit, gsp.store as pstore
                                        from grab_section gs join grab_section gsp
                                            on gs.next_id = gsp.id
                                         where gs.aid = %s and gs.flow = %s; """, (aid, flow['flow'])):
                dataextract = dbpc.handler.queryAll(""" select * from grab_dataextract where sid = %s """, (section['id'], ))
                datasource = dbpc.handler.queryAll(""" select * from grab_datasource where sid = %s """, (section['id'], ))
                sections[flow['flow']].append({'id':section['id'], 'aid':section['aid'], 'name':section['name'], 'flow':section['flow'], 'index':section['index'], 'retry':section['retry'], 'timelimit':section['timelimit'], 'store':section['store'], 'dataextract':dataextract, 'datasource':datasource})
            dataextract = dbpc.handler.queryAll(""" select * from grab_dataextract where sid = %s """, (section['pid'], ))
            datasource = dbpc.handler.queryAll(""" select * from grab_datasource where sid = %s """, (section['pid'], ))
            sections[flow['flow']].append({'id':section['pid'], 'aid':section['paid'], 'name':section['pname'], 'flow':section['pflow'], 'index':section['pindex'], 'retry':section['pretry'], 'timelimit':section['ptimelimit'], 'store':section['pstore'], 'dataextract':dataextract, 'datasource':datasource})
        return render_template('sectionlist.html', aid=aid, flows=flows, sections=sections)
    elif request.method == 'POST':
        flow = request.form.get('flow', '')
        sections = json.loads(request.form.get('sections', '[]'))
        for section in sections:
            if section['id']:
                print 'update'
            else:
                print 'insert'
        return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    elif request.method == 'DELETE':
        sid = request.form.get('id', '')
        print 'section id ', sid
        return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        pass

@produce.route('/section/detail', methods=['GET', 'POST', 'DELETE'])
@produce.route('/section/detail/<sid>', methods=['GET', 'POST', 'DELETE'])
@withMysql(WDB, resutype='DICT', autocommit=True)
def sectiondetail(sid=None):
    aid = int(request.args.get('aid', 0))
    if request.method == 'GET':
        if sid is None:
            section = {'id':'', 'aid':'', 'next_id':'', 'name':'', 'flow':'', 'index':'', 'retry':'', 'timelimit':'', 'store':'', 'datasource':[], 'dataextract':[]}
        else:
            section = dbpc.handler.queryOne(""" select `id`, `aid`,`next_id`,`name`,`flow`,`index`,`retry`,`timelimit`,`store` from grab_section where id = %s; """, sid)
            next = dbpc.handler.queryOne(""" select `id`, `aid`,`next_id`,`name`,`flow`,`index`,`retry`,`timelimit`,`store` from grab_section where id = %s; """, (section['next_id'],))
            if next is None:
                section['next'] = ''
            else:
                section['next'] = next['name']
            datasource = dbpc.handler.queryAll(""" select * from grab_datasource where sid = %s """, (sid, ))
            dataextract = dbpc.handler.queryAll(""" select * from grab_dataextract where sid = %s """, (sid, ))
            section['datasource'] = datasource
            section['dataextract'] = dataextract
        return render_template('sectiondetail.html', aid=aid, section=section)
    elif request.method == 'POST':
        section_name = request.form.get('section_name')
        next_id = request.form.get('next_id')
        flow = request.form.get('flow')
        index = request.form.get('index')
        retry = request.form.get('retry')
        timelimit = request.form.get('timelimit')
        store = request.form.get('store')
        if aid is None:
            dbpc.handler.insert(""" insert into `grab_section` (`aid`, `name`, `next_id`, `flow`, `index`, `retry`, `timelimit`, `store`, `creator`, `updator`, `create_time`, `update_time`)values(%s, %s, %s, %s, %s, %s, %s, %s, 1, null, 0, 0, now(), now()); """, (aid, section_name, next_id, flow, index, retry, timelimit, store))
        else:
            dbpc.handler.update(""" update `grab_section` set `name` = %s, `next_id` = %s, `flow` = %s, `index` = %s, `retry` = %s, `timelimit` = %s, `store` = %s, update_time=now() where `id` = %s """, (section_name, next_id, flow, index, retry, timelimit, store, sid))
        return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    elif request.method == 'DELETE':
        iid = request.form.get('id', '')
        iname = request.form.get('name', '')
        itype = request.form.get('type', '')
        print 'i id ', iid
        print 'i name ', iname
        print 'i type ', itype
        return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        pass
