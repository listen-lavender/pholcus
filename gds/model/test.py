#!/usr/bin/env python
# coding=utf8
import ConfigParser 

config=ConfigParser.ConfigParser()
config.read('../pholcus.cfg')

def parse(items):
    return dict(items)

print parse(config.items("base"))