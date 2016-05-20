#!/usr/bin/env python
# coding=utf8
import os, types, datetime, uuid, random, hashlib, json
from flask import Blueprint, request, Response, render_template, redirect, make_response, session, g
from model.setting import withBase, basecfg
from flask.helpers import send_from_directory
from bson import ObjectId
from model.base import Creator, Permit
from setting import STATIC


LENGTH = [5, 7, 13]
UL = [True, True, False, True, False, False]
C = ['a', '1', 'b', 'c', '2', 'd', '3', 'e', 'f', 'g', '4', '5', 'h', 'i', '7', 'j', 'k', '6', 'l', 'm', 'n', 'o', 'p', '9', 'q', 'r', '8', 's', 't', 'u', 'v', 'w', 'x', '0', 'y', 'z']
PRIORITY = {'administrator':{
        'Creator':{'authority':9, 'desc':'a--q'},
        'Article':{'authority':1, 'desc':'---q'},
        'Section':{'authority':1, 'desc':'---q'},
        'Task':{'authority':1, 'desc':'---q'},
    },
    'developer':{
        'Creator':{'authority':1, 'desc':'---q'},
        'Article':{'authority':9, 'desc':'a--q'},
        'Section':{'authority':9, 'desc':'a--q'},
        'Task':{'authority':9, 'desc':'a--q'},
    },
    'operator':{
        'Creator':{'authority':1, 'desc':'---q'},
        'Article':{'authority':1, 'desc':'---q'},
        'Section':{'authority':1, 'desc':'---q'},
        'Task':{'authority':9, 'desc':'a--q'},
    },
}
STATUS = {1:'有效', 0:'无效', 2:'待审核'}


def send_static_file(self, filename):
    """Function used internally to send static files from the static
    folder to the browser.

    .. versionadded:: 0.5
    """
    if not self.has_static_folder:
        raise RuntimeError('No static folder for this object')
    # Ensure get_send_file_max_age is called in all cases.
    # Here, we ensure get_send_file_max_age is called for Blueprints.
    cache_timeout = self.get_send_file_max_age(filename)
    return send_from_directory(self.static_folder, filename,
                               cache_timeout=1)

creator = Blueprint('creator', __name__, template_folder='template')
creator.send_static_file  = types.MethodType(send_static_file, creator)
    
@creator.route('/list', methods=['GET'])
@withBase(basecfg.R, resutype='DICT', autocommit=True)
def user_list():
    user = request.user
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = int(request.args.get('total', 0))
    if total == 0:
        total = Creator.count(user, {})
    count = (total - 1)/pagetotal + 1
    creators = Creator.queryAll(user, {}, projection={'username':1, 'group':1, 'create_time':1}, sort=[('update_time', -1)], skip=(page-1)*pagetotal, limit=pagetotal)
    result = {"appname":g.appname, "user":user, "creator":creators, "pagetotal":pagetotal, "page":page, "total":total, "count":count}
    return json.dumps({'code':1, 'desc':'success', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')


@creator.route('/login', methods=['POST', 'GET'])
@withBase(basecfg.W, resutype='DICT', autocommit=True)
def login():
    # username = request.form.get('username')
    # password = request.form.get('password')
    username = 'root'
    password = '123456'
    user = request.user
    m = hashlib.md5()
    m.update(password)
    password = m.hexdigest()
    
    result = {"appname":g.appname, "user":user, "msg":""}
    sid = None
    if user is None:
        user = Creator.queryOne({}, {'username':username, 'password':password, 'status':{'$ne':0}})
        if user is None:
            result['msg'] = '未找到用户，是否未注册？'
        else:
            user = {'name':user['username'], '_id':str(user['_id']), 'status':user['status'], 'group':user['group']}
            sid = str(uuid.uuid4())
            session[sid] = user
    else:
        user = Creator.queryOne({}, {'_id':user['_id']})
    result['user'] = user
    
    response = Response(json.dumps({'code':1, 'res':result, 'msg':''}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8'), mimetype='application/json')
    if sid is not None:
        response.set_cookie('sid', sid)
    return response

@creator.route('/logout', methods=['GET'])
def logout():
    pass

