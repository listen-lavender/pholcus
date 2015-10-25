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
    return render_template('mtasklist.html', tasks=tasks, pagetotal=pagetotal, page=page, total=total, count=count)

@monitor.route('/task/detail/<tid>', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def taskdetail(tid):
    end = request.args.get('end', datetime.datetime.now())
    begin = request.args.get('begin', datetime.datetime.now() -
                             datetime.timedelta(seconds=48*600))

    sql = '''select substr(create_time, 1, 16) as time, elapse as value
        from grab_statistics where tid = %s and create_time between %s and %s
            order by time
    '''
    print sql, tid, begin.strftime('%Y-%m-%d %H:%M:%S'), end.strftime('%Y-%m-%d %H:%M:%S')
    stats = dbpc.handler.queryAll(sql, (tid, begin, end))
    for log in stats:
        # log['time'] = parser.parse(log['time']+'0')
        log['time'] = time.mktime(time.strptime(log['time']+ ':00', '%Y-%m-%d %H:%M:%S')) * 1000
        log['value']  = float(log['value'])

    chart = dict(
        title='a',
        subtitle='b',
        ytitle='c',
    )
    print stats
    dataset=[
        {'name':u'elapse state', 'stats':stats, 'color':'#229933'},
        # {'name':u'exception requests', 'stats':stats, 'color':'#007788'},
    ]
    return render_template("mtaskdetail.html", dataset=dataset, request=request, chart=chart, unit='s', begin=begin, end=end)

@monitor.route('/task/change/<tid>', methods=['POST'])
@withMysql(WDB, resutype='DICT', autocommit=True)
def taskchange(tid):
    status = request.form.get('status', 1)
    sql = '''
        update grab_task set status = %s where id = %s
    '''
    dataset = dbpc.handler.update(sql, (status, tid))
    return json.dumps({'stat':1, 'desc':'success', 'data':{}}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')

@monitor.route('/time-detail/<gsid>', methods=['GET'])
@withMysql(RDB, resutype='DICT')
def time_detail():
    html = request.args.get('html', '0')
    stime = request.args.get('time', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    end = begin + datetime.timedelta(seconds=600)
    sql = '''
        select * from grab_log where gsid = %s and timestamp between %s and %s
    '''
    dataset = dbpc.handler.queryAll(sql, (gsid, begin, end))
    if html == "0":
        return simplejson.dumps(dataset)
    else:
        return render_template("time_detail.html", title="Cada", dataset=dataset, request=request, begin=begin, end=end)