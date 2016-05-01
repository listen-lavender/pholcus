#!/usr/bin/env python
# coding=utf8
import json, sys, os, datetime

from setting import useport, CACHE_TIMEOUT
from flask import Flask, g, request, Response, session, redirect, render_template
from flask.templating import DispatchingJinjaLoader
from flask.globals import _request_ctx_stack
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.contrib.cache import SimpleCache
from werkzeug.routing import BaseConverter
from util.session import Session

from blueprint.task.views import task
from blueprint.script.views import script
from blueprint.user.views import user

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
app.permanent_session_lifetime = datetime.timedelta(days=1)
Session(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hotel2:hotel0115@58.83.130.112:3306/hotel20'
# db = SQLAlchemy(app)
# g['db'] = db

app.jinja_options = Flask.jinja_options.copy() 
app.jinja_options['loader'] = LeafinlineLoader(app)

app.register_blueprint(admin, url_prefix='/api/task')
app.register_blueprint(script, url_prefix='/api/script')
app.register_blueprint(user, url_prefix='/api/user')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', appname=g.appname)


def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = fun(*args, **kwargs)
        if type(rst) == str:
            rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        return rst
    return wrapper_fun

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
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
    # sid = request.cookies.get('sid')
    # user = session.get(sid, None)
    g.appname = 'pholcus'
    # flag = request.url == request.url_root or '/task/data/' in request.url or '/static/' in request.url or '/login' in request.url or '/register' in request.url
    # if '/api/' in request.url and user is None:
    #     user = {'status': 1, '_id': '7', 'group': 'developer', 'name': 'root'}
    # request.sid = sid
    # request.user = user
    # if flag:
    #     pass
    # elif user is None:
    #     return redirect('/api/a/login')
    # elif not user.get('status') == 1:
    #     return redirect('/api/a/info')
    # else:
    #     pass
    request.user = {'status': 1, '_id': '7', 'group': 'developer', 'name': 'root'}


# @app.after_request
# def call_after_request_callbacks(response):
#     pass

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    print("Launching server at port %d" % useport)

    run_simple('0.0.0.0', useport, app, use_reloader=True,
        passthrough_errors=True, threaded=True)

    print("Server sucessfully terminated")
