#!/usr/bin/env python
# coding=utf-8
import time
import hashlib

def checksign(paras, appSecret):
    m = hashlib.md5()
    origin = ''
    if not 'appKey' in paras:
        raise Exception('No appKey.')
    if not 'appSecret' in paras:
        paras['appSecret'] = appSecret
    for one in sorted(paras.items(), key=lambda x: x[0]):
        if one[0] == 'sign':
            continue
        origin += one[-1]
    m.update(origin)
    sign = m.hexdigest()
    return sign == paras['sign']


if __name__ == '__main__':
    pass
