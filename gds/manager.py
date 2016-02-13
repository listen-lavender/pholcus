#!/usr/bin/python
# coding=utf8

from flask.ext.script import Manager, Server
from views import app
from settings import useport
from werkzeug.contrib.fixers import ProxyFix
from dbskit.mysql.suit import baseConn, withMysql, DBPoolCollector

@withMysql('wdb')
def buildbase():
    pass

app.wsgi_app = ProxyFix(app.wsgi_app)

manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0',
    port = useport)
)

@manager.command
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)
    
    for line in sorted(output):
        print line

if __name__ == "__main__":
    manager.run()

