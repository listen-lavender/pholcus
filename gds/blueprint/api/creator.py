#!/usr/bin/env python
# coding=utf8
import os, types, datetime, uuid, random, hashlib, json
from flask import Blueprint, request, Response, render_template, redirect, make_response, session, g
from model.setting import withBase, basecfg
from model.base import Creator
from rest import api

@api.route('/login', methods=['POST'])
@withBase(basecfg.W, resutype='DICT', autocommit=True)
def login():
    username = request.form.get('username')
    secret = request.form.get('secret')
    
    result = {"appname":g.appname, "user":{}, "msg":""}
    user = Creator.queryOne({}, {'username':username, 'secret':secret, 'status':{'$ne':0}})
    if user is None:
        result['msg'] = '未找到用户，是否未注册？'
    else:
        user = {'name':user['username'], '_id':str(user['_id']), 'status':user['status'], 'group':user['group'], 'api':True}
        sid = str(uuid.uuid4())
        session[sid] = user
    result['user'] = user
    
    response = Response(json.dumps({'code':1, 'res':result, 'msg':''}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8'), mimetype='application/json')
    if sid is not None:
        response.set_cookie('sid', sid)
    return response

