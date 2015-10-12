#!/usr/bin/python
# coding=utf8
from flask import Blueprint, request, Response, render_template
from flask.helpers import send_from_directory
import types
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
                               cache_timeout=1200000)

admin = Blueprint('admin', __name__, template_folder='templates')
admin.send_static_file  = types.MethodType(send_static_file, admin)

@admin.route('/login', methods=['POST'])
def login():
    return render_template('login.html')

@admin.route('/register', methods=['POST'])
def register():
    pass

@admin.route('/config/list', methods=['GET'])
def configlist():
    pass

@admin.route('/config/detail/<cid>', methods=['GET', 'POST'])
def configdetail(cid):
    render_template('')