#!/usr/bin/env python
# coding=utf8
import json
from model.setting import withBase, basecfg
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g

task = Blueprint('task', __name__, template_folder='template')

@produce.route('/list', methods=['GET'])
def task_list():
    return 