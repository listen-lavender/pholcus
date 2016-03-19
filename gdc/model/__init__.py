#!/usr/bin/env python
# coding=utf-8

def initDB():
    from setting import dataconn, datacfg
    dataconn.addDB(datacfg.R, datacfg.LIMIT, **datacfg.SETTING)
    dataconn.addDB(datacfg.W, datacfg.LIMIT, **datacfg.SETTING)

initDB()