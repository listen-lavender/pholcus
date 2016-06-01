#!/usr/bin/env python
# coding=utf8
import json, urllib, datetime
from webcrawl.character import unicode2utf8
from model.setting import withBase, basecfg, baseorm
from model.base import Article, Creator, Section
from flask import Blueprint, request, Response, render_template, g
from views import script
from model.base import Section, Permit
from model.setting import baseorm

@script.route('/step/list', methods=['GET', 'DELETE'])
@withBase(basecfg.W, resutype='DICT', autocommit=True)
def sectionlist():
    """
    select gs.id, gs.aid, gs.name, gs.flow, gs.index, gs.retry, gs.timelimit, gs.store, gsp.id, gsp.aid, gsp.name, gsp.flow, gsp.index, gsp.retry, gsp.timelimit, gsp.store
    from grab_section gs join grab_section gsp
    on gs.next_id = gsp.id
     where gs.flow = 'www';
    """
    user = request.user
    if request.method == 'GET':
        weight = {}
        fid = request.args.get('flow_id')
        fid = baseorm.IdField.verify(fid)
        sections = []
        projection = {'_id':1, 'aid':1, 'name':1, 'flow':1, 'index':1, 'retry':1, 'timelimit':1, 'store':1, 'next_id':1}
        for section in Section.queryAll(user, {'fid':fid}, projection=projection):
            section['_id'] = str(section['_id'])
            weight[section['_id']] = weight.get(section['_id'], 0) + 1
            next = Section.queryOne(user, {'_id':section['next_id']}, projection=projection)
            if next:
                section['pid'] = str(next['_id'])
                weight[section['pid']] = weight.get(section['pid'], 0) + weight.get(section['_id'], 1)
            sections.append({'_id':section['_id'], 'aid':section['aid'], 'name':section['name'], 'flow':section['flow'], 'index':section['index'], 'retry':section['retry'], 'timelimit':section['timelimit'], 'store':section['store']})
        sections.sort(key=lambda one:weight[one['_id']])
        result = {"appname":g.appname, "user":user, "step":sections}
        result = json.dumps({'code':1, 'msg':'', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
        return result
    elif request.method == 'DELETE':
        fid = request.args.get('flow_id')
        fid = baseorm.IdField.verify(fid)
        return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        pass

@script.route('/step/detail/<sid>', methods=['GET', 'POST'])
@withBase(basecfg.W, resutype='DICT', autocommit=True)
def sectiondetail(sid=None):
    user = request.user
    sid = baseorm.IdField.verify(sid)
    if request.method == 'GET':
        projection = {'_id':1, 'aid':1, 'next_id':1, 'name':1, 'desc':1, 'flow':1, 'index':1, 'retry':1, 'timelimit':1, 'store':1, 'additions':1, 'creator':1}
        section = Section.queryOne(user, {'_id':sid}, projection=projection)
        next = Section.queryOne(user, {'_id':section['next_id']}, projection=projection)
        if next is None:
            section['next'] = ''
        else:
            section['next'] = next['name']
        section['current'] = str(section['creator']) == user['_id']
        del section['creator']
        author = {}
        for one in Permit.queryAll({'otype':'Section', 'oid':sid}, projection={'cid':1, '_id':0}):
            author[str(one['cid'])] = ''
        section['author'] = urllib.quote(json.dumps(author).encode('utf8'))
        result = {"appname":g.appname, "user":user, "step":section}
        result = json.dumps({'code':1, 'msg':'', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
        return result
    elif request.method == 'POST':
        desc = request.form.get('desc')
        retry = request.form.get('retry')
        timelimit = request.form.get('timelimit')
        store = request.form.get('store')
        additions = request.form.get('additions')
        addcid = request.form.get('addcid', '').split(',')
        delcid = request.form.get('delcid', '').split(',')

        Section.update(user, {'_id':sid}, {'desc':desc, 'retry':retry, 'timelimit':timelimit, 'store':store, 'additions':additions})
        for cid in addcid:
            if cid == '':
                continue
            # cid = baseorm.IdField.verify(cid)
            # if Permit.queryOne({'cid':cid, 'otype':'Section', 'oid':sid}) is None:
            #     permit = Permit(cid=cid, otype='Section', oid=baseorm.IdField.verify(sid), authority=1, desc='---q', status=1, creator=user['_id'], updator=user['_id'], create_time=datetime.datetime.now())
            #     Permit.insert(permit)
        for cid in delcid:
            if cid == '':
                continue
            # Permit.delete({'cid':cid, 'otype':'Section', 'oid':sid})
        result = {"appname":g.appname, "user":user, "step":{}}
        result = json.dumps({'code':1, 'msg':'', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
        return result
    else:
        pass
        