#!/usr/bin/env python
# coding=utf8
import json, sys, os, functools

from datetime import datetime, date, timedelta
from bson import ObjectId
from setting import USEPORT, CACHE_TIMEOUT, APPNAME
from flask import Flask, g, request, Response, session, redirect, render_template
from flask.templating import DispatchingJinjaLoader
from flask.globals import _request_ctx_stack
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.contrib.cache import SimpleCache
from werkzeug.routing import BaseConverter
from util.session import Session

from blueprint.task.views import task
from blueprint.script.views import script
from blueprint.creator.views import creator
from blueprint.api.rest import api

class SpecialEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif type(obj) == list:
            return ','.join(obj)
        elif type(obj) == dict:
            return ','.join(obj.keys())
        else:
            return json.JSONEncoder.default(self, obj)

class Utf8Decoder(json.JSONDecoder):
    def __init__(self):
        super(Utf8Decoder, self).__init__(object_hook=None)

json.dumps = functools.partial(json.dumps, cls=SpecialEncoder)
# json.loads = functools.partial(json.loads, cls=Utf8Decoder)

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


class LeafinlineLoader(DispatchingJinjaLoader):
    def _iter_loaders(self, template):
        bp = _request_ctx_stack.top.request.blueprint
        if bp is not None and bp in self.app.blueprints:
            loader = self.app.blueprints[bp].jinja_loader
            if loader is not None:
                yield loader, template

        loader = self.app.jinja_loader
        if loader is not None:
            yield loader, template


app = Flask(__name__, static_folder='static', static_path='/static', template_folder='template')
app.config.from_object(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
# app.config['SESSION_COOKIE_HTTPONLY'] = False
app.permanent_session_lifetime = timedelta(days=1)
Session(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hotel2:hotel0115@58.83.130.112:3306/hotel20'
# db = SQLAlchemy(app)
# g['db'] = db

app.jinja_options = Flask.jinja_options.copy() 
app.jinja_options['loader'] = LeafinlineLoader(app)

app.register_blueprint(task, url_prefix='/gds/api/task')
app.register_blueprint(script, url_prefix='/gds/api/script')
app.register_blueprint(creator, url_prefix='/gds/api/creator')
app.register_blueprint(api, url_prefix='/gdc/api')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', appname=g.appname)

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
    g.appname = APPNAME
    sid = request.cookies.get('sid')
    user = session.get(sid, None)
    print request.url
    
    flag = request.url == request.url_root or '/task/data/' in request.url or '/static/' in request.url or '/login' in request.url or '/register' in request.url
    request.sid = sid
    request.user = user
    if '/logout' in request.url:
        session[sid] = None
        response = Response(json.dumps({'code':0, 'res':{'user':None}, 'msg':''}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8'), mimetype='application/json')
        return response
    elif flag or user:
        pass
    else:
        response = Response(json.dumps({'code':1, 'res':{'user':None}, 'msg':''}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8'), mimetype='application/json')
        return response

# @app.after_request
# def call_after_request_callbacks(response):
#     pass

@app.after_request
def allow_cross_domain(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.errorhandler(Exception)
def exception_handler(error):
    response = Response(json.dumps({'code':0, 'res':{'user':None}, 'msg':str(error)}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8'), mimetype='application/json')
    return response

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    print("Launching server at port %d" % USEPORT)

    run_simple('0.0.0.0', USEPORT, app, use_reloader=True,
        passthrough_errors=True, threaded=True)

    print("Server sucessfully terminated")
