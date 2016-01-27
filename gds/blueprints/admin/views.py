#!/usr/bin/python
# coding=utf8
from flask import Blueprint, request, Response, render_template, redirect, make_response, session
from datakit.mysql.suit import withMysql, dbpc, RDB, WDB
from flask.helpers import send_from_directory
import types, datetime, uuid


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

admin = Blueprint('admin', __name__, template_folder='templates')
admin.send_static_file  = types.MethodType(send_static_file, admin)

@admin.route('/login', methods=['GET', 'POST'])
@withMysql(WDB, resutype='DICT', autocommit=True)
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
    # dbpc.handler.insert(sql, (username, password, contact, notify, status, creator, updator, create_time))
    user = request.user
    if user is not None:
        return redirect('/gds/m/task/list')
    user = dbpc.handler.queryOne(""" select * from grab_creator where username = %s and password = %s """, (username, password))
    if user is not None:
        user = {'name':user['username'], 'id':user['id']}
        response = make_response(redirect('/gds/m/task/list'))
        sid = str(uuid.uuid4())
        session[sid] = user
        response.set_cookie('sid', sid)
        return response
    else:
        return render_template('login.html')

@admin.route('/logout', methods=['GET'])
def logout():
    sid = request.sid
    if sid is not None:
        del session[sid]
    return redirect('/gds/a/login')

@admin.route('/register', methods=['POST'])
def register():
    pass

@admin.route('/config/list', methods=['GET'])
def configlist():
    pass

@admin.route('/config/detail/<cid>', methods=['GET', 'POST'])
def configdetail(cid):
    render_template('')
