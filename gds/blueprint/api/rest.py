#!/usr/bin/env python
# coding=utf8
import json
from model.setting import withBase, withData, base, data, _BASE_R, _BASE_W, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g

api = Blueprint('api', __name__)

from datamodel import *
from unit import *
from article import *
from section import *
from task import *
from config import *
