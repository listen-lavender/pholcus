#!/usr/bin/env python
# coding=utf8
import json
from flask import Blueprint, request, Response, render_template, g
from util.encrypt import rsa, randomKey, encrypt_crypto

api = Blueprint('api', __name__)

from datamodel import *
from unit import *
from article import *
from flow import *
from section import *
from task import *
from creator import *

@api.route('/test', methods=['GET'])
def test_encrypt():
    txt = {'a':'hao', 'b':'kuan'}
    result = json.dumps({'stat':1, 'desc':'将军', 'result':txt}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    key = randomKey()
    result = encrypt_crypto(result, key)
    key = rsa.encrypt(key)
    return json.dumps({'key':key, 'result':result})
    