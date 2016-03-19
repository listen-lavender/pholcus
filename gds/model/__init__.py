#!/usr/bin/env python
# coding=utf-8

def initDB():
    from setting import baseconn, dataconn, basecfg, datacfg
    baseconn.addDB(basecfg.R, basecfg.LIMIT, **basecfg.SETTING)
    baseconn.addDB(basecfg.W, basecfg.LIMIT, **basecfg.SETTING)
    dataconn.addDB(datacfg.R, datacfg.LIMIT, **datacfg.SETTING)
    dataconn.addDB(datacfg.W, datacfg.LIMIT, **datacfg.SETTING)
    
initDB()