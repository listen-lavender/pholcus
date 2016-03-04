#!/usr/bin/env python
# coding=utf-8


USER = 'root'
SECRET = '900150983cd24fb0d6963f7d28e17f72'

DQ = {
    'redis':{
        'host':'localhost',
        'port':6379,
        'db':0,
        'tube':'pholcus-task',
        'log':{
            'host':'localhost',
            'port':6379,
            'db':0,
            'tube':'pholcus-log',
            'worker':10
        }
    },
    'beanstalkd':{
        'host':'localhost',
        'port':11300,
        'tube':'pholcus-task',
    }
}
