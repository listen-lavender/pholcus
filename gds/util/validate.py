#!/usr/bin/env python
# coding=utf-8

#-*- coding:utf-8 -*-

import time, urllib
import urlparse, hashlib

APPKEY = '48cHeUnimNMjn5D6BnQehEwaA1Pa'
APPSECRET = '3JHrP69s4otAGd9ksRaCxc2A6cRh'

def md5encode(paras, appKey=APPKEY, appSecret=APPSECRET):
    m = hashlib.md5()
    origin = ''
    if not 'appkey' in ','.join(paras.keys()).lower():
        paras['appKey'] = appKey
    if not 'appSecret' in ','.join(paras.keys()).lower():
        paras['appSecret'] = appSecret
    for one in sorted(paras.items(), key=lambda x: x[0]):
        if one[0] == 'sign':
            continue
        if one[0] == 'redirect':
            origin += urllib.unquote(one[-1])
        else:
            origin += one[-1]
    m.update(origin)
    sign = m.hexdigest()
    return sign

def autologin(uid, credits, redirect, appKey=APPKEY, appSecret=APPSECRET):
    ts = str(int(time.time() * 1000))
    url = 'http://www.duiba.com.cn/autoLogin/autologin?uid=%s&credits=%s&appKey=%s&timestamp=%s&redirect=%s&appSecret=%s' % (uid, credits, appKey, ts, redirect, appSecret)
    paras = dict(urlparse.parse_qsl(urlparse.urlparse(url).query))
    paras['sign'] = md5encode(paras, appKey=appKey, appSecret=appSecret)
    loginurl = 'http://www.duiba.com.cn/autoLogin/autologin?' + '&'.join('%s=%s' % (one[0], urllib.quote(one[-1]) if one[0] == 'redirect' else one[-1]) for one in sorted(paras.items(), key=lambda x: x[0]) if not one[0] == 'appSecret')
    return loginurl

def checksign(url, appKey=APPKEY, appSecret=APPSECRET):
    if 'sign=' in url:
        paras = dict(urlparse.parse_qsl(urlparse.urlparse(url).query))
        return paras['sign'] == md5encode(paras, appKey=appKey, appSecret=appSecret)
    else:
        return False

if __name__ == '__main__':
    pass
