#!/usr/bin/python
# coding=utf8
from datakit.mysql.suit import withMysql, dbpc
from flask import Blueprint, request, Response, render_template

monitor = Blueprint('monitor', __name__, template_folder='templates')
