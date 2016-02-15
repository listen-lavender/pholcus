#!/usr/bin/python
# coding=utf8
import types, datetime, uuid, random, hashlib
from flask import Blueprint, request, Response, render_template, redirect, make_response, session, g
from model.settings import withBase, withData, base, data, _BASE_R, _BASE_W, RDB, WDB
from flask.helpers import send_from_directory
from model.base import Creator, Permit

LENGTH = [5, 7, 13]
UL = [True, True, False, True, False, False]
C = ['a', '1', 'b', 'c', '2', 'd', '3', 'e', 'f', 'g', '4', '5', 'h', 'i', '7', 'j', 'k', '6', 'l', 'm', 'n', 'o', 'p', '9', 'q', 'r', '8', 's', 't', 'u', 'v', 'w', 'x', '0', 'y', 'z']


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

admin = Blueprint('admin', __name__, template_folder='template')
admin.send_static_file  = types.MethodType(send_static_file, admin)


@admin.route('/login', methods=['GET', 'POST'])
@withBase(WDB, resutype='DICT', autocommit=True)
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    # contact = '{}'
    # notify = '{}'
    # status = 1
    # creator = 0
    # updator = 0
    # create_time = datetime.datetime.now()
    # sql = """insert ignore into grab_creator(`username`,`password`,`contact`,`notify`,`status`,`creator`,`updator`,`create_time`)
    #                            values(%s        ,        %s,       %s,      %s,      %s,       %s,       %s,           %s);
    # """
    # baseConn.handler.insert(sql, (username, password, contact, notify, status, creator, updator, create_time))
    user = request.user
    if user is not None:
        return redirect('/gds/m/task/list')
    user = Creator.queryOne(None, {'username':username, 'password':password, 'status':{'$ne':0}})
    if user is not None:
        user = {'name':user['username'], '_id':user['_id'], 'status':user['status']}
        response = make_response(redirect('/gds/m/task/list'))
        sid = str(uuid.uuid4())
        session[sid] = user
        response.set_cookie('sid', sid)
        return response
    else:
        return render_template('login.html', appname=g.appname, status=0, logined=False)


@admin.route('/logout', methods=['GET'])
def logout():
    sid = request.sid
    if sid is not None:
        del session[sid]
    return redirect('/gds/a/login')


@admin.route('/register', methods=['GET', 'POST'])
@withBase(WDB, resutype='DICT', autocommit=True)
def register():
    if request.method == 'GET':
        return render_template('register.html', appname=g.appname, logined=False)
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        contact = '{}'
        notify = '{}'
        m = hashlib.md5()
        origin = ''
        for k in range(random.choice(LENGTH)):
            origin += random.choice(C).upper()  if random.choice(UL) else random.choice(C)
        m.update(origin)
        secret = m.hexdigest()
        status = 2
        creator = 0
        updator = 0
        create_time = datetime.datetime.now()
        user = Creator(username=username, password=password, contact=contact, notify=notify, secret=secret, status=status, creator=creator, updator=updator, create_time=create_time)
        user['_id'] = Creator.insert(user)
        user = {'name':user['username'], '_id':user['_id']}
        response = make_response(redirect('/gds/a/info'))
        sid = str(uuid.uuid4())
        session[sid] = user
        response.set_cookie('sid', sid)
        return response


@admin.route('/verify', methods=['GET', 'POST'])
@withBase(WDB, resutype='DICT', autocommit=True)
def verify():
    user = request.user
    if request.method == 'GET':
        return render_template('verify.html', appname=g.appname, logined=False)
    else:
        _id = request.form.get('_id')
        group = request.form.get('group')
        Creator.update({'_id':_id}, {'group':group, 'status':1})
        permit = Permit(cid=_id, otype='grab_unit', authority=15, desc='aduq', status=1, creator=user['uid'], updator=user['uid'])
        Permit.insert(permit)
        permit = Permit(cid=_id, otype='grab_article', authority=15, desc='aduq', status=1, creator=user['uid'], updator=user['uid'])
        Permit.insert(permit)
        permit = Permit(cid=_id, otype='grab_section', authority=15, desc='aduq', status=1, creator=user['uid'], updator=user['uid'])
        Permit.insert(permit)
        permit = Permit(cid=_id, otype='grab_task', authority=15, desc='aduq', status=1, creator=user['uid'], updator=user['uid'])
        Permit.insert(permit)
        permit = Permit(cid=_id, otype='grab_config', authority=15, desc='aduq', status=1, creator=user['uid'], updator=user['uid'])
        Permit.insert(permit)
        return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')


@admin.route('/info', methods=['GET'])
@withBase(WDB, resutype='DICT', autocommit=True)
def info():
    user = request.user
    user = Creator.queryOne(user['_id'], {'_id':user['_id']})
    return render_template('info.html', appname=g.appname, logined=True, user=user)
