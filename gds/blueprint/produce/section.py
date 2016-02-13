#!/usr/bin/python
# coding=utf8
import json
from settings import withBase, withData, baseConn, dataConn, _BASE_R, _BASE_W
from webcrawl.character import unicode2utf8
from hawkeye import seesection
from flask import Blueprint, request, Response, render_template, g
from views import produce
from model.base import Section, Dataextract, Datasource

@produce.route('/section/list/<aid>', methods=['GET', 'POST', 'DELETE'])
@withMysql(WDB, resutype='DICT', autocommit=True)
def sectionlist(aid):
    """
    select gs.id, gs.aid, gs.name, gs.flow, gs.index, gs.retry, gs.timelimit, gs.store, gsp.id, gsp.aid, gsp.name, gsp.flow, gsp.index, gsp.retry, gsp.timelimit, gsp.store
    from grab_section gs join grab_section gsp
    on gs.next_id = gsp.id
     where gs.flow = 'www';
    """
    if request.method == 'GET':
        flows = Section.queryAll({'aid':aid}, projection={'flow':1})
        flows = set(one['flow'] for one in flows)
        sections = {}
        projection = {'id':1, 'aid':1, 'name':1, 'flow':1, 'index':1, 'retry':1, 'timelimit':1, 'store':1, 'next_id':1}
        for flow in flows:
            sections[flow] = []
            currs = Section.queryAll({'aid':aid, 'flow':flow}, projection=projection)
            for section in currs:
                next = Section.queryOne({'id':section['next_id']}, projection=projection)
                if next:
                    section['pid'] = next['id']
                    section['paid'] = next['aid']
                    section['pname'] = next['name']
                    section['pflow'] = next['flow']
                    section['pindex'] = next['index']
                    section['pretry'] = next['retry']
                    section['ptimelimit'] = next['timelimit']
                    section['pstore'] = next['store']
                dataextract = Dataextract.queryAll({'sid':section['id']})
                datasource = Datasource.queryAll({'sid':section['id']})
                sections[flow].append({'id':section['id'], 'aid':section['aid'], 'name':section['name'], 'flow':section['flow'], 'index':section['index'], 'retry':section['retry'], 'timelimit':section['timelimit'], 'store':section['store'], 'dataextract':dataextract, 'datasource':datasource})
            dataextract = Dataextract.queryAll({'sid':section['pid']})
            datasource = Datasource.queryAll({'sid':section['pid']})
            sections[flow].append({'id':section['pid'], 'aid':section['paid'], 'name':section['pname'], 'flow':section['pflow'], 'index':section['pindex'], 'retry':section['pretry'], 'timelimit':section['ptimelimit'], 'store':section['pstore'], 'dataextract':dataextract, 'datasource':datasource})
        return render_template('psectionlist.html', appname=g.appname, logined=True, aid=aid, flows=flows, sections=sections)
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
            projection = {'id':1 ,'aid':1 ,'next_id':1 ,'name':1 ,'flow':1 ,'index':1 ,'retry':1 ,'timelimit':1 ,'store':1}
            section = Section.queryOne({'id':sid}, projection=projection)
            next = Section.queryOne({'id':section['next_id']}, projection=projection)
            if next is None:
                section['next'] = ''
            else:
                section['next'] = next['name']
            dataextract = Dataextract.queryAll({'sid':sid})
            datasource = Datasource.queryAll({'sid':sid})
            section['datasource'] = datasource
            section['dataextract'] = dataextract
        return render_template('psectiondetail.html', appname=g.appname, logined=True, aid=aid, sid=sid, section=section)
    elif request.method == 'POST':
        if request.form.get('type') == 'source':
            sid = request.form.get('sid')
            datasource_name = request.form.get('name')
        elif request.form.get('type') == 'extract':
            sid = request.form.get('sid')
            dataextract_name = request.form.get('name')
        else:
            sid = request.form.get('id')
            section_name = request.form.get('name')
            next = request.form.get('next')
            flow = request.form.get('flow')
            index = request.form.get('index')
            retry = request.form.get('retry')
            timelimit = request.form.get('timelimit')
            store = request.form.get('store')
        # seesection(baseConn, aid, sid)
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
