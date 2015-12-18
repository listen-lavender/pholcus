#!/usr/bin/python
# coding=utf8
import json
import time, datetime
from datakit.mysql.suit import withMysql, dbpc, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template
from views import monitor

STATDESC = {0:'stopped', 1:'started', 2:'running', 3:'error'}

@monitor.route('/task/list', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def tasklist():
    pagetotal = int(request.args.get('pagetotal', 10))
    page = int(request.args.get('page', 1))
    total = int(request.args.get('total', 0))
    if total == 0:
        total = dbpc.handler.queryOne(""" select count(gt.id) as total from grab_task gt; """)['total']
    count = (total - 1)/pagetotal + 1
    tasks = dbpc.handler.queryAll(""" select gt.id, gt.name as task_name, gt.status from grab_task gt order by gt.update_time desc limit %s, %s; """, ((page-1)*pagetotal, pagetotal))
    for one in tasks:
        one['status_desc'] = STATDESC.get(one['status'], '')
        one['max'] = (dbpc.handler.queryOne(""" select max(succ) as succ from grab_statistics where tid = %s; """, (one['id'], )) or {'succ':0})['succ']
    return render_template('mtasklist.html', tasks=tasks, pagetotal=pagetotal, page=page, total=total, count=count)

@monitor.route('/task/time/detail/<tid>', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def tasktimedetail(tid):
    title = '耗时统计'
    end = request.args.get('end')
    begin = request.args.get('begin')

    if end is None:
        end = (dbpc.handler.queryOne(''' select create_time from grab_statistics where tid = %s order by id desc limit 1; ''', (tid, )) or {'create_time':datetime.datetime.now()})['create_time']
    else:
        end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    begin = end - datetime.timedelta(seconds=48*600)

    sql = '''select substr(create_time, 1, 16) as time, elapse as value
        from grab_statistics where tid = %s and create_time between %s and %s
            order by time
    '''

    print sql, tid, begin, end
    stats = dbpc.handler.queryAll(sql, (tid, begin, end))
    for log in stats:
        # log['time'] = parser.parse(log['time']+'0')
        log['time'] = time.mktime(time.strptime(log['time']+ ':00', '%Y-%m-%d %H:%M:%S')) * 1000
        log['value'] = float(log['value'])

    chart = dict(
        title=title,
        subtitle='',
        ytitle='',
    )
    dataset=[
        {'name':'elapse state', 'stats':stats, 'color':'#229933'},
    ]
    title = '耗时统计'
    return render_template("mtaskdetail.html", title=title, dataset=dataset, request=request, chart=chart, unit='s', begin=begin, end=end)

@monitor.route('/task/count/detail/<tid>', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def taskcountdetail(tid):
    title = '数量统计'
    end = request.args.get('end')
    begin = request.args.get('begin')

    if end is None:
        end = (dbpc.handler.queryOne(''' select create_time from grab_statistics where tid = %s order by id desc limit 1; ''', (tid, )) or {'create_time':datetime.datetime.now()})['create_time']
    else:
        end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    begin = end - datetime.timedelta(seconds=48*600)

    sql = '''select substr(create_time, 1, 16) as time, succ as value
        from grab_statistics where tid = %s and create_time between %s and %s
            order by time
    '''

    print sql, tid, begin, end
    succ_stats = dbpc.handler.queryAll(sql, (tid, begin, end))
    for log in succ_stats:
        # log['time'] = parser.parse(log['time']+'0')
        log['time'] = time.mktime(time.strptime(log['time']+ ':00', '%Y-%m-%d %H:%M:%S')) * 1000
        log['value'] = float(log['value'])

    sql = '''select substr(create_time, 1, 16) as time, fail as value
        from grab_statistics where tid = %s and create_time between %s and %s
            order by time
    '''
    print sql, tid, begin, end
    fail_stats = dbpc.handler.queryAll(sql, (tid, begin, end))
    for log in fail_stats:
        # log['time'] = parser.parse(log['time']+'0')
        log['time'] = time.mktime(time.strptime(log['time']+ ':00', '%Y-%m-%d %H:%M:%S')) * 1000
        log['value'] = float(log['value'])

    sql = '''select substr(create_time, 1, 16) as time, timeout as value
        from grab_statistics where tid = %s and create_time between %s and %s
            order by time
    '''
    print sql, tid, begin, end
    timeout_stats = dbpc.handler.queryAll(sql, (tid, begin, end))
    for log in timeout_stats:
        # log['time'] = parser.parse(log['time']+'0')
        log['time'] = time.mktime(time.strptime(log['time']+ ':00', '%Y-%m-%d %H:%M:%S')) * 1000
        log['value'] = float(log['value'])

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
    
    return render_template("mtaskdetail.html", title=title, dataset=dataset, request=request, chart=chart, unit='', begin=begin, end=end)

@monitor.route('/task/change/<tid>', methods=['POST'])
@withMysql(WDB, resutype='DICT', autocommit=True)
def taskchange(tid):
    status = request.form.get('status', 1)
    sql = '''
        update grab_task set status = %s where id = %s
    '''
    dataset = dbpc.handler.update(sql, (status, tid))
    return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')

