#!/usr/bin/env python
# coding=utf8
import json
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from util.encrypt import rsa, randomKey, encrypt_crypto

api = Blueprint('api', __name__)

def format_datetime(one):
    if 'create_time' in one:
        one['create_time'] = one['create_time'].strftime('%Y-%m-%d %H:%M:%S')
    if 'update_time' in one:
        one['update_time'] = one['update_time'].strftime('%Y-%m-%d %H:%M:%S')
    return one

from datamodel import *
from unit import *
from article import *
from section import *
from task import *

@api.route('/test', methods=['GET'])
def test_encrypt():
    txt = {'a':'hao', 'b':'kuan'}
    result = json.dumps({'stat':1, 'desc':'将军', 'result':txt}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    key = randomKey()
    result = encrypt_crypto(result, key)
    key = rsa.encrypt(key)
    return json.dumps({'key':key, 'result':result})
    