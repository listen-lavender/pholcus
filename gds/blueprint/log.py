#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
import pickle
from model.setting import withBase, withDataQuery, withDataCount, baseorm, basecfg
from flask import Blueprint, request, Response, render_template, g
from webcrawl.queue.mongo import Queue
from model.setting import WORKQUEUE
from model.log import Log
from views import running

q = Queue(host=WORKQUEUE['host'], port=WORKQUEUE['port'], db=WORKQUEUE['db'], tube=WORKQUEUE['tube'], init=False)
q = q.mc[q.tube]

from views import running

@running.route('/log/<ssid>', methods=['GET'])
def log(ssid):
    user = request.user
    snapshot = q.find_one({'_id':ssid}) or {'args':'', 'kwargs':''}
    log = withDataQuery(Log.__table__, {'_id':ssid}, qt='one') or {'desc':''}
    txt = snapshot['txt'].encode('utf-8')
    txt = pickle.loads(txt)
    args = str(txt['args'])
    kwargs = json.dumps(txt['kwargs'], ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    result = {"appname":g.appname, "user":user, "log":{'args':args, 'kwargs':kwargs, 'exception':log['desc'], 'tid':snapshot['tid']}}
    return json.dumps({'code':1, 'desc':'success', 'res':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
