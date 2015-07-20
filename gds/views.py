#!/usr/bin/python
# coding=utf8
import json
from settings import staticfilepath, useport, CACHE_TIMEOUT, _DBCONN_R, _DBCONN_W, LIMIT
from dbm.mysql.suit import withMysql, dbpc, RDB, WDB
from flask import Flask, g, request, Response
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.contrib.cache import SimpleCache
from blueprints.admin.views import admin
from blueprints.monitor.views import monitor
from blueprints.produce.views import produce
from werkzeug.routing import BaseConverter

dbpc.addDB(RDB, LIMIT, host=_DBCONN_R['host'],
                    port=_DBCONN_R['port'],
                    user=_DBCONN_R['user'],
                    passwd=_DBCONN_R['passwd'],
                    db=_DBCONN_R['db'],
                    charset=_DBCONN_R['charset'],
                    use_unicode=_DBCONN_R['use_unicode'],
                    override=False)

dbpc.addDB(WDB, LIMIT, host=_DBCONN_W['host'],
                    port=_DBCONN_W['port'],
                    user=_DBCONN_W['user'],
                    passwd=_DBCONN_W['passwd'],
                    db=_DBCONN_W['db'],
                    charset=_DBCONN_W['charset'],
                    use_unicode=_DBCONN_W['use_unicode'],
                    override=False)

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

app = Flask(__name__, static_folder='static', static_path='/gds/static', template_folder='templates')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hotel2:hotel0115@58.83.130.112:3306/hotel20'
# db = SQLAlchemy(app)
# g['db'] = db
app.register_blueprint(admin, url_prefix='/gds/admin')
app.register_blueprint(monitor, url_prefix='/gds/monitor')
app.register_blueprint(produce, url_prefix='/gds/produce')

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

def after_this_request(f):
    if not hasattr(g, 'after_request_callbacks'):
        g.after_request_callbacks = []
    g.after_request_callbacks.append(f)
    return f

# @app.before_request
# def docrypt():
#     pass
#     @after_this_request
#     def encrypt(response):
#         pass

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
