#!/usr/bin/env python
# coding=utf-8

def initDB():
    from setting import baseconn, dataconn, basecfg, datacfg
    baseconn.addDB(basecfg.R(), basecfg._LIMIT, **basecfg._SETTING)
    baseconn.addDB(basecfg.W(), basecfg._LIMIT, **basecfg._SETTING)
    dataconn.addDB(datacfg.R(), datacfg._LIMIT, **datacfg._SETTING)
    dataconn.addDB(datacfg.W(), datacfg._LIMIT, **datacfg._SETTING)
    
initDB()