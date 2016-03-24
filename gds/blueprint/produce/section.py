#!/usr/bin/env python
# coding=utf8
import json, urllib, datetime
from model.setting import withBase, basecfg
from webcrawl.character import unicode2utf8
from hawkeye import seesection
from flask import Blueprint, request, Response, render_template, g
from views import produce
from model.base import Section, Dataextract, Datasource, Permit
from model.setting import baseorm

@produce.route('/section/list/<aid>', methods=['GET', 'POST', 'DELETE'])
@withBase(basecfg.W, resutype='DICT', autocommit=True)
def sectionlist(aid):
    """
    select gs.id, gs.aid, gs.name, gs.flow, gs.index, gs.retry, gs.timelimit, gs.store, gsp.id, gsp.aid, gsp.name, gsp.flow, gsp.index, gsp.retry, gsp.timelimit, gsp.store
    from grab_section gs join grab_section gsp
    on gs.next_id = gsp.id
     where gs.flow = 'www';
    """
    user = request.user
    if request.method == 'GET':
        weight = {}
        flow = request.args.get('flow', 0)
        sections = []
        projection = {'_id':1, 'aid':1, 'name':1, 'flow':1, 'index':1, 'retry':1, 'timelimit':1, 'store':1, 'next_id':1}
        for section in Section.queryAll(user, {'aid':aid, 'flow':flow}, projection=projection):
            section['_id'] = str(section['_id'])
            section['aid'] = str(section['aid'])
            weight[section['_id']] = weight.get(section['_id'], 0) + 1
            next = Section.queryOne(user, {'_id':section['next_id']}, projection=projection)
            if next:
                section['pid'] = str(next['_id'])
                section['paid'] = str(next['aid'])
                weight[section['pid']] = weight.get(section['pid'], 0) + weight.get(section['_id'], 1)
                section['pname'] = next['name']
                section['pflow'] = next['flow']
                section['pindex'] = next['index']
                section['pretry'] = next['retry']
                section['ptimelimit'] = next['timelimit']
                section['pstore'] = next['store']
            dataextract = Dataextract.queryAll({'sid':section['_id']})
            datasource = Datasource.queryAll({'sid':section['_id']})
            sections.append({'_id':section['_id'], 'aid':section['aid'], 'name':section['name'], 'flow':section['flow'], 'index':section['index'], 'retry':section['retry'], 'timelimit':section['timelimit'], 'store':section['store'], 'dataextract':dataextract, 'datasource':datasource})
        # dataextract = Dataextract.queryAll({'sid':section['pid']})
        # datasource = Datasource.queryAll({'sid':section['pid']})
        # sections.append({'_id':section['pid'], 'aid':section['paid'], 'name':section['pname'], 'flow':section['pflow'], 'index':section['pindex'], 'retry':section['pretry'], 'timelimit':section['ptimelimit'], 'store':section['pstore'], 'dataextract':dataextract, 'datasource':datasource})
        sections.sort(key=lambda one:weight[one['_id']])
        return render_template('section/list.html', appname=g.appname, user=user, aid=aid, flow=flow, sections=sections)
    elif request.method == 'POST':
        flow = request.form.get('flow', '')
        sections = json.loads(request.form.get('sections', '[]'))
        for section in sections:
            if section['_id']:
                print 'update'
            else:
                print 'insert'
        return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    elif request.method == 'DELETE':
        sid = request.form.get('_id', '')
        return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        pass

@produce.route('/section/detail', methods=['GET', 'POST', 'DELETE'])
@produce.route('/section/detail/<sid>', methods=['GET', 'POST', 'DELETE'])
@withBase(basecfg.W, resutype='DICT', autocommit=True)
def sectiondetail(sid=None):
    user = request.user
    aid = int(request.args.get('aid', 0))
    if request.method == 'GET':
        if sid is None:
            section = {'_id':'', 'aid':'', 'next_id':'', 'next':'', 'name':'', 'desc':'', 'flow':'', 'index':'', 'retry':'', 'timelimit':'', 'store':'', 'additions':'', 'datasource':[], 'dataextract':[], 'current':True}
        else:
            projection = {'_id':1, 'aid':1, 'next_id':1, 'name':1, 'desc':1, 'flow':1, 'index':1, 'retry':1, 'timelimit':1, 'store':1, 'additions':1, 'creator':1}
            section = Section.queryOne(user, {'_id':sid}, projection=projection)
            next = Section.queryOne(user, {'_id':section['next_id']}, projection=projection)
            if next is None:
                section['next'] = ''
            else:
                section['next'] = next['name']
            dataextract = Dataextract.queryAll({'sid':sid})
            datasource = Datasource.queryAll({'sid':sid})
            section['datasource'] = datasource
            section['dataextract'] = dataextract
            section['current'] = str(section['creator']) == user['_id']
            del section['creator']
        author = {}
        for one in Permit.queryAll({'otype':'Section', 'oid':sid}, projection={'cid':1, '_id':0}):
            author[str(one['cid'])] = ''
        section['author'] = urllib.quote(json.dumps(author).encode('utf8'))
        return render_template('section/detail.html', appname=g.appname, user=user, aid=aid, sid=sid, section=section)
    elif request.method == 'POST':
        sid = request.form.get('_id')
        section_name = request.form.get('name')
        desc = request.form.get('desc')
        next = request.form.get('next')
        flow = request.form.get('flow')
        index = request.form.get('index')
        retry = request.form.get('retry')
        timelimit = request.form.get('timelimit')
        store = request.form.get('store')
        additions = request.form.get('additions')
        addcid = request.form.get('addcid', '').split(',')
        delcid = request.form.get('delcid', '').split(',')
        if sid:
            sid = baseorm.IdField.verify(sid)
            Section.update(user, {'_id':sid}, {'desc':desc, 'index':index, 'retry':retry, 'timelimit':timelimit, 'store':store, 'additions':additions})
        else:
            section = Section(aid=baseorm.IdField.verify(aid), next_id=next, name=section_name, desc=desc, flow=flow, step=0, index=index, retry=retry, timelimit=timelimit, store=store, additions=additions, create_time=datetime.datetime.now())
            sid = Section.insert(user, section)
        for cid in addcid:
            if cid == '':
                continue
            cid = baseorm.IdField.verify(cid)
            if Permit.queryOne({'cid':cid, 'otype':'Article', 'oid':aid}) is None:
                permit = Permit(cid=cid, otype='Article', oid=baseorm.IdField.verify(aid), authority=1, desc='---q', status=1, creator=user['_id'], updator=user['_id'], create_time=datetime.datetime.now())
                Permit.insert(permit)
            if Permit.queryOne({'cid':cid, 'otype':'Section', 'oid':sid}) is None:
                permit = Permit(cid=cid, otype='Section', oid=baseorm.IdField.verify(sid), authority=1, desc='---q', status=1, creator=user['_id'], updator=user['_id'], create_time=datetime.datetime.now())
                Permit.insert(permit)
        for cid in delcid:
            if cid == '':
                continue
            Permit.delete({'cid':cid, 'otype':'Section', 'oid':sid})
        return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    elif request.method == 'DELETE':
        iid = request.form.get('_id', '')
        iname = request.form.get('name', '')
        itype = request.form.get('type', '')
        print 'i id ', iid
        print 'i name ', iname
        print 'i type ', itype
        return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        pass
