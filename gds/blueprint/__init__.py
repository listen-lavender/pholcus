#!/usr/bin/env python
# coding=utf8
import datetime
from model.base import baseorm, Permit

def select(options, otype, oid, uid, authtype='update'):
    if not type(options) == list:
        options = options.split(',') if ',' in options else []
    authority = 1
    desc = (3, 'q')
    if authtype == 'update':
        authority = 2
        desc = (2, 'u')
    for _id in options:
        _id = baseorm.IdField.verify(_id)
        permit = Permit.queryOne({'cid':_id, 'otype':otype, 'oid':oid})
        if permit and not desc[1] in permit['desc']:
            permit['authority'] = permit['authority'] + authority
            permit['desc'] = permit['desc'][0:desc[0]] + desc[1] + permit['desc'][desc[0]+1:]
            Permit.update({'_id':permit['_id'], 'creator':uid}, {'$set':{'authority':permit['authority'], 'desc':permit['desc']}})
        else:
            authority = 3
            desc = '--uq'
            Permit.insert(Permit(**{'cid':_id, 'otype':otype, 'oid':oid, 'creator':uid, 'authority':authority, 'desc':desc, 'creator':uid, 'updator':uid, 'create_time':datetime.datetime.now()}))

def unselect(options, otype, oid, uid):
    if not type(options) == list:
        options = options.split(',') if ',' in options else []
    for _id in options:
        _id = baseorm.IdField.verify(_id)
        Permit.update({'cid':_id, 'otype':otype, 'oid':oid}, {'$set':{'authority':0, 'desc':'----', 'updator':uid}})

