#!/usr/bin/env python
# coding=utf-8

def initDB():
    from setting import dataconn, datacfg
    print datacfg.R()
    dataconn.addDB(datacfg.R(), datacfg._LIMIT, **datacfg._SETTING)
    dataconn.addDB(datacfg.W(), datacfg._LIMIT, **datacfg._SETTING)

initDB()