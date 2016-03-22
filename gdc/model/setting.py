#!/usr/bin/env python
# coding=utf8
import ConfigParser 
from dbskit import parse, extract
from dbskit.mysql import CFG as mysql_cfg, orm as mysql_orm
from dbskit.mongo import CFG as mongo_cfg, orm as mongo_orm
from dbskit.mysql.suit import withMysql, withMysqlQuery, withMysqlCount, dbpc as mysql_dbpc
from dbskit.mongo.suit import withMongo, withMongoQuery, withMongoCount, dbpc as mongo_dbpc

config=ConfigParser.ConfigParser()
config.read('../pholcus.cfg')

base = parse(config.items("base"))

if base['type'] == 'mysql':
    baseorm = mysql_orm
else:
    baseorm = mongo_orm

data = parse(config.items("data"))
if data['type'] == 'mysql':
    datacfg = mysql_cfg
    dataconn = mysql_dbpc
    dataorm = mysql_orm
    withData = withMysql
    withDataQuery = withMysqlQuery
    withDataCount = withMysqlCount
else:
    datacfg = mongo_cfg
    dataconn = mongo_dbpc
    dataorm = mongo_orm
    withData = withMongo
    withDataQuery = withMongoQuery
    withDataCount = withMongoCount
datacfg.R = datacfg.W = data['name']
datacfg._LIMIT = data['limit']
datacfg._BUFFER = data['buffer']
datacfg._SETTING = extract(data)

WORKNUM = config.getint("work", "worknum")
WORKQUEUE = parse(config.items("work-queue"))
LOGNUM = config.getint("log", "worknum")
LOGSTATUS = config.getint("log", "status")
LOGQUEUE = parse(config.items("log-queue"))
