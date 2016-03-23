#!/usr/bin/env python
# coding=utf8
import os
STATIC = os.path.join(os.path.abspath('.'), 'static', 'exe')

ALLOWED_EXTENSIONS = set(['py'])

def allowed(filename):
    return '.' in filename and filename.rsplit('.')[-1] in ALLOWED_EXTENSIONS

def getpath(filename):
    filepath = os.path.join(STATIC, filename)
    filedir = os.path.dirname(filepath)
    if not os.path.exists(filedir):
        os.makedirs(filedir)
    return filepath