#!/usr/bin/python
# coding=utf8
import json, sys, os
sys.path.append('../')
from settings import staticfilepath, useport, CACHE_TIMEOUT
from flask import Flask, g, request, Response, session, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.contrib.cache import SimpleCache
from werkzeug.routing import BaseConverter
from util.session import Session

from blueprint.admin.views import admin
from blueprint.monitor.views import monitor
from blueprint.produce.views import produce

cache = SimpleCache()
def cached(func):
    def decorator(*args, **kwargs):
        key = request.path + '&'.join(['%s=%s'%(k,v.encode('utf8')) for k,v in
                                      request.args.items()])
        response = cache.get(key)
        if response is None:
            print 'call func:', key
            response = func(*args, **kwargs)
            cache.set(key, response, CACHE_TIMEOUT)
        return response
    return decorator

app = Flask(__name__, static_folder='static', static_path='/gds/static', template_folder='template')
app.config.from_object(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = True
Session(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hotel2:hotel0115@58.83.130.112:3306/hotel20'
# db = SQLAlchemy(app)
# g['db'] = db
app.register_blueprint(admin, url_prefix='/gds/a')
app.register_blueprint(monitor, url_prefix='/gds/m')
app.register_blueprint(produce, url_prefix='/gds/p')

# @app.context_processor
# def override_url_for():
#     return dict(url_for=static_url_for)

# def static_url_for(endpoint, **values):
#     if endpoint == 'static':
#         filename = values.get('filename', None)
#         if filename:
#             file_path = STATIC_URL_ROOT + filename
#             return file_path
#     else:
#         return url_for(endpoint, **values)

class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]
app.url_map.converters['regex'] = RegexConverter

# def after_this_request(f):
#     if not hasattr(g, 'after_request_callbacks'):
#         g.after_request_callbacks = []
#     g.after_request_callbacks.append(f)
#     return f

@app.before_request
def is_login():
    sid = request.cookies.get('sid')
    user = session.get(sid, None)
    g.appname = 'pholcus'
    flag = '/static/' in request.url or '/login' in request.url or '/register' in request.url
    request.sid = sid
    request.user = user
    if flag:
        pass
    elif user is None:
        return redirect('/gds/a/login')
    elif not user.get('status') == 1:
        return redirect('/gds/a/info')
    else:
        pass


# @app.after_request
# def call_after_request_callbacks(response):
#     pass

if __name__ == "__main__":
    import logging
    from werkzeug.serving import run_simple

    app.logger.setLevel(logging.DEBUG)
    logging.getLogger().setLevel(logging.DEBUG)
    logging.info("Launching server at port %d" % useport)

    run_simple('0.0.0.0', useport, app, use_reloader=True,
        passthrough_errors=True, threaded=True)

    logging.info("Server sucessfully terminated")
