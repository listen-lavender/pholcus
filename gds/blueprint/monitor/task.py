#!/usr/bin/python
# coding=utf8
import json
import time, datetime
from model.setting import withBase, withData, base, data, _BASE_R, _BASE_W, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from views import monitor
from model.base import Task
from model.log import Statistics

STATDESC = {0:'stopped', 1:'started', 2:'running', 3:'error'}

@monitor.route('/task/list', methods=['GET'])
@withBase(RDB, resutype='DICT')
@withData(RDB, resutype='DICT')
def tasklist():
    user = request.user
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = int(request.args.get('total', 0))
    if total == 0:
        total = Task.count(user, {})
    count = (total - 1)/pagetotal + 1
    tasks = Task.queryAll(user, {}, sort=[('update_time', -1)], skip=(page-1)*pagetotal, limit=pagetotal)
    for one in tasks:
        one['change'] = (one['status'] in (0, 1, 2) and one['type'] == 'FOREVER') or (one['status'] in (0, 1) and one['type'] == 'ONCE')
        one['status_desc'] = STATDESC.get(one['status'], '')
        one['max'] = (Statistics.queryOne({'tid':one['_id']}, projection={'succ':1}, sort=[('succ', -1)]) or {'succ':0})['succ']
    return render_template('task/list.html', appname=g.appname, user=user, tasks=tasks, pagetotal=pagetotal, page=page, total=total, count=count)

@monitor.route('/task/time/detail/<tid>', methods=['GET'])
@withBase(RDB, resutype='DICT')
def tasktimedetail(tid):
    title = '任务耗时统计'
    end = request.args.get('end')
    begin = request.args.get('begin')

    if end is None:
        end = (Statistics.queryOne({'tid':tid}, projection={'create_time':1}, sort=[('_id', -1)]) or {'create_time':datetime.datetime.now()})['create_time']
    else:
        end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    begin = end - datetime.timedelta(seconds=48*600)

    sql = '''select substr(create_time, 1, 16) as time, elapse as value
        from grab_statistics where tid = %s and create_time between %s and %s
            order by time
    '''

    print sql, tid, begin, end
    stats = Statistics.queryAll({'tid':tid, '$and':[{'create_time':{'$get':begin}}, {'create_time':{'$let':end}}]}, projection={'time':1, 'elapse':1})
    for log in stats:
        log['time'] = log['time'].strftime('%Y-%m-%d %H:%M')
        log['time'] = time.mktime(time.strptime(log['time']+ ':00', '%Y-%m-%d %H:%M:%S')) * 1000
        log['value'] = float(log['elapse'])
        del log['elapse']

    chart = dict(
        title=title,
        subtitle='',
        ytitle='',
    )
    dataset=[
        {'name':'elapse state', 'stats':stats, 'color':'#229933'},
    ]
    return render_template("task/detail.html", appname=g.appname, user=user, title=title, dataset=dataset, request=request, chart=chart, unit='s', begin=begin, end=end)

@monitor.route('/task/count/detail/<tid>', methods=['GET'])
@withBase(RDB, resutype='DICT')
def taskcountdetail(tid):
    title = '任务数量统计'
    end = request.args.get('end')
    begin = request.args.get('begin')

    if end is None:
        end = (Statistics.queryOne({'tid':tid}, projection={'create_time':1}, sort=[('_id', -1)]) or {'create_time':datetime.datetime.now()})['create_time']
    else:
        end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    begin = end - datetime.timedelta(seconds=48*600)

    sql = '''select substr(create_time, 1, 16) as time, succ as value
        from grab_statistics where tid = %s and create_time between %s and %s
            order by time
    '''

    print sql, tid, begin, end
    succ_stats = Statistics.queryAll({'tid':tid, '$and':[{'create_time':{'$get':begin}}, {'create_time':{'$let':end}}]}, projection={'time':1, 'succ':1})
    for log in succ_stats:
        log['time'] = log['time'].strftime('%Y-%m-%d %H:%M')
        log['time'] = time.mktime(time.strptime(log['time']+ ':00', '%Y-%m-%d %H:%M:%S')) * 1000
        log['value'] = float(log['succ'])
        del log['succ']

    sql = '''select substr(create_time, 1, 16) as time, fail as value
        from grab_statistics where tid = %s and create_time between %s and %s
            order by time
    '''
    print sql, tid, begin, end
    fail_stats = Statistics.queryAll({'tid':tid, '$and':[{'create_time':{'$get':begin}}, {'create_time':{'$let':end}}]}, projection={'time':1, 'fail':1})
    for log in fail_stats:
        log['time'] = log['time'].strftime('%Y-%m-%d %H:%M')
        log['time'] = time.mktime(time.strptime(log['time']+ ':00', '%Y-%m-%d %H:%M:%S')) * 1000
        log['value'] = float(log['fail'])
        del log['fail']

    sql = '''select substr(create_time, 1, 16) as time, timeout as value
        from grab_statistics where tid = %s and create_time between %s and %s
            order by time
    '''
    print sql, tid, begin, end
    timeout_stats = Statistics.queryAll({'tid':tid, '$and':[{'create_time':{'$get':begin}}, {'create_time':{'$let':end}}]}, projection={'time':1, 'timeout':1})
    for log in timeout_stats:
        log['time'] = log['time'].strftime('%Y-%m-%d %H:%M')
        log['time'] = time.mktime(time.strptime(log['time']+ ':00', '%Y-%m-%d %H:%M:%S')) * 1000
        log['value'] = float(log['timeout'])
        del log['timeout']

    chart = dict(
        title=title,
        subtitle='',
        ytitle='',
    )
    dataset=[
        {'name':'succ', 'stats':succ_stats, 'color':'green'},
        {'name':'fail', 'stats':fail_stats, 'color':'blue'},
        {'name':'timeout', 'stats':timeout_stats, 'color':'red'},
    ]
    return render_template("task/detail.html", appname=g.appname, user=user, title=title, dataset=dataset, request=request, chart=chart, unit='', begin=begin, end=end)


@monitor.route('/task/change/<tid>', methods=['POST'])
@withBase(WDB, resutype='DICT', autocommit=True)
def taskchange(tid):
    user = request.user
    status = request.form.get('status', 1)
    Task.update(user, {'_id':tid}, {'status':status})
    return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')

