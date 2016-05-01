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

user = Blueprint('user', __name__, template_folder='template')
user.send_static_file  = types.MethodType(send_static_file, user)


@user.route('/login', methods=['GET', 'POST'])
@withBase(basecfg.W, resutype='DICT', autocommit=True)
def login():
    username = request.form.get('username')
    password = request.form.get('password', '')
    user = request.user
    m = hashlib.md5()
    m.update(password)
    password = m.hexdigest()
    if user is not None:
        return redirect('/gds/m/task/list')
    user = Creator.queryOne({}, {'username':username, 'password':password, 'status':{'$ne':0}})
    if user is not None:
        user = {'name':user['username'], '_id':str(user['_id']), 'status':user['status'], 'group':user['group']}
        if user['group'] == 'developer':
            response = make_response(redirect('/gds/m/task/activity'))
        else:
            response = make_response(redirect('/gds/m/task/list'))
        sid = str(uuid.uuid4())
        session[sid] = user
        response.set_cookie('sid', sid)
        return response
    else:
        return render_template('login.html', appname=g.appname, status=0, user=None)


@user.route('/logout', methods=['GET'])
def logout():
    sid = request.sid
    if sid is not None:
        del session[sid]
    return redirect('/gds/a/login')


@user.route('/register', methods=['GET', 'POST'])
@withBase(basecfg.W, resutype='DICT', autocommit=True)
def register():
    if request.method == 'GET':
        return render_template('register.html', appname=g.appname, user=None)
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        m = hashlib.md5()
        m.update(password)
        password = m.hexdigest()
        contact = '{}'
        notify = '{}'
        m = hashlib.md5()
        origin = ''
        for k in range(random.choice(LENGTH)):
            origin += random.choice(C).upper()  if random.choice(UL) else random.choice(C)
        m.update(origin)
        secret = m.hexdigest()
        status = 2
        creator = Creator.queryOne({'username':'root'}, {'_id':1})['_id']
        updator = creator
        create_time = datetime.datetime.now()
        user = Creator(username=username, password=password, contact=contact, notify=notify, secret=secret, status=status, creator=creator, updator=updator, create_time=create_time)
        user['_id'] = Creator.insert({}, user)
        user = {'name':user['username'], '_id':user['_id'], 'status':user['status'], 'group':''}
        response = make_response(redirect('/gds/a/info'))
        sid = str(uuid.uuid4())
        session[sid] = user
        response.set_cookie('sid', sid)
        return response


@user.route('/user/verify', methods=['GET', 'POST'])
@withBase(basecfg.W, resutype='DICT', autocommit=True)
def verify():
    user = request.user
    if request.method == 'POST':
        _id = request.form.get('_id')
        vtype = request.form.get('type')
        value = request.form.get('value')

        if vtype == 'status':
            Creator.update(user, {'_id':_id}, {'status':int(value)})
        else:
            create_time = datetime.datetime.now()
            for one in ['Creator', 'Article', 'Section', 'Task']:
                authority = PRIORITY.get(value).get(one).get('authority')
                desc = PRIORITY.get(value).get(one).get('desc')
                permit = Permit(cid=_id, otype=one, authority=authority, desc=desc, status=1, creator=user['_id'], updator=user['_id'], create_time=create_time)
                Permit.insert(permit)
            Creator.update(user, {'_id':_id}, {'group':value})
        return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')


@user.route('/user/list', methods=['GET', 'POST'])
@withBase(basecfg.W, resutype='DICT', autocommit=True)
def user_list():
    user = request.user
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = int(request.args.get('total', 0))
    if total == 0:
        total = Creator.count(user, {})
    count = (total - 1)/pagetotal + 1
    if request.method == 'GET':
        creators = Creator.queryAll(user, {}, projection={'username':1, 'group':1, 'create_time':1}, sort=[('update_time', -1)], skip=(page-1)*pagetotal, limit=pagetotal)
        return render_template('user/list.html', appname=g.appname, user=user, creators=creators, pagetotal=pagetotal, page=page, total=total, count=count)
    else:
        creators = Creator.queryAll(user, {}, projection={'username':1}, sort=[('update_time', -1)])
        for index, one in enumerate(creators):
            creators[index]['_id'] = str(one['_id'])
        return json.dumps({'stat':1, 'desc':'success', 'data':creators}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')


@user.route('/user/detail/<cid>', methods=['GET'])
@withBase(basecfg.W, resutype='DICT', autocommit=True)
def userdetail(cid=None):
    user = request.user
    cid = cid or user['_id']
    creator = Creator.queryOne(user, {'_id':cid})
    creator['current'] = str(cid) == user['_id']
    creator['secret'] = creator['secret'] if creator['current'] else ''
    creator['status_desc'] = STATUS.get(creator['status'])
    return render_template('user/detail.html', appname=g.appname, user=user, creator=creator)


@user.route('/user/avatar', methods=['POST'])
@withBase(basecfg.W, resutype='DICT', autocommit=True)
def useravatar():
    user = request.user
    avatar = request.files['avatar']
    name = str(ObjectId())
    path = os.path.join(os.path.abspath('.'), STATIC, 'img/user/', name)
    avatar.save(path)
    Creator.update(user, {'_id':user['_id']}, {'avatar':'/gds/static/img/user/%s' % name})
    return json.dumps({'stat':1, 'desc':'success', 'data':'/gds/static/img/user/%s' % name}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')


@user.route('/user/password', methods=['GET', 'POST'])
@withBase(basecfg.W, resutype='DICT', autocommit=True)
def userpassword():
    user = request.user
    if request.method == 'GET':
        return render_template('user/password.html', appname=g.appname, user=user)
    else:
        oldpassword = request.form.get('oldpassword')
        m = hashlib.md5()
        m.update(oldpassword)
        oldpassword = m.hexdigest()
        newpassword = request.form.get('newpassword', '123456')
        m = hashlib.md5()
        m.update(newpassword)
        newpassword = m.hexdigest()

        if oldpassword == newpassword:
            data = '更新成功.'
        elif Creator.queryOne({}, {'_id':user['_id'], 'password':oldpassword, 'status':{'$ne':0}}) is None:
            data = '请输入正确的旧密码.'
        else:
            Creator.update(user, {'_id':user['_id']}, {'password':newpassword})
            data = '更新成功.'
        return json.dumps({'stat':1, 'desc':'success', 'data':data}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
