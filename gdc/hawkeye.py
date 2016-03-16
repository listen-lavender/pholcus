#!/usr/bin/env python
# coding=utf-8
import time, datetime
import os, sys
from webcrawl.handleRequest import requGet, requPost
sys.path.append('../')
from optparse import OptionParser
from godhand import cook
from model.setting import baseorm, withBase, WDB, RDB
from model.base import Section, Article, Unit, Config, Datamodel
from setting import USER, SECRET
import task

LIMIT = 20

# def ensure(filepath):
#     if filepath.startswith('/'):
#         if not os.path.exists(os.path.split(filepath)[0]):
#             os.mkdir(os.path.split(filepath)[0])
#     else:
#         filepath = os.path.join(os.path.split(os.path.abspath(__file__))[0], filepath)
#         if not os.path.exists(os.path.split(filepath)[0]):
#             os.mkdir(os.path.split(filepath)[0])
#     return filepath


# @withBase(WDB, resutype='DICT')
# def getUnit(uid):
#     config = Config.queryOne({'key':'task'}, projection={'val':1})
#     unit = Unit.queryOne({'_id':uid}, projection={'dmid':1, 'name':1, 'filepath':1})
#     dirfile = ''.join([config['val'], unit['filepath']])
#     material = {}
#     for one in Datapath.queryAll({'btype':'unit', '$or':[{'bid':uid}, {'bid':0}]}):
#         material[str(one['_id'])] = one
#     fi = open(ensure(dirfile), 'w')
#     fi.write(cook(material))
#     fi.close()


# @withBase(WDB, resutype='DICT')
# def getArticle(aid, flow):
#     config = Config.queryOne({'type':'ROOT', 'key':'dir'}, projection={'val':1})
#     article = Article.queryOne({'username':USER, 'secret':SECRET}, {'_id':aid}, projection={'filepath':1, 'uid':1})
#     unit = Unit.queryOne({'_id':article['uid']}, projection={'dmid':1, 'name':1})
#     dirfile = ''.join([config['val'], article['filepath']])
#     material = {}
#     sids = [str(one['_id']) for one in Section.queryAll({'username':USER, 'secret':SECRET}, {'aid':aid, 'flow':flow}, projection={'_id':1})]
#     for one in Datapath.queryAll({'$or':[{'btype':'article', '$or':[{'bid':baseorm.IdField.verify(aid)}, {'bid':0}]}, {'btype':'section', 'bid':{'$in':sids}}]}):
#         material[str(one['_id'])] = one
#     fi = open(ensure(dirfile), 'w')
#     fi.write(cook(material))
#     fi.close()


# @withBase(WDB, resutype='DICT')
# def initScript():
#     for unit in Unit.queryAll():
#         getUnit(unit['_id'])
#         for article in Article.queryAll({'username':USER, 'secret':SECRET}, {'uid':unit['_id']}):
#             for flow in set([section['flow'] for section in Section.queryAll({'username':USER, 'secret':SECRET}, {'aid':article['aid']}, projection={'flow':1})]):
#                 getArticle(article['_id'], flow)

def setModel(filepath):
    fi = open(filepath, 'r')
    data = fi.read()
    fi.close()
    for txt in data.split('@'):
        if 'comment(' in txt:
            comment = None
            model = None
            for line in txt.split('\n'):
                if 'comment' in line:
                    info = line.replace('(', '').replace(')', '').split("'")
                    comment = info[1]
                if 'class' in line:
                    info = line.replace('(', ' ').replace(')', '').replace(',', '').split(' ')
                    model = info[1].lower()
                    break
            if model is not None:
                datamodel = requGet('http://localhost/api/datamodel?name=%s' % model)
                datamodel = datamodel['datamodel']
                if datamodel:
                    continue
                data = {
                    "name"=model,
                    "table"=model,
                    "comment"=comment,
                }
                print requPost('http://localhost/api/datamodel', data, format='JSON')
                # datamodel = Datamodel(name=model, table=model, comment=comment, autocreate=1, iscreated=1, status=1, create_time=datetime.datetime.now())
                # Datamodel.insert(datamodel)


def setUnit(filepath, comment):
    name = filepath[filepath.rindex('/')+1:].replace('spider.py', '')
    unit = requGet('http://localhost/api/unit?name=%s' % name)
    unit = unit['unit']
    if not unit:
        dmid = None
        fi = open(filepath, 'r')
        for one in fi.readlines():
            if 'as Data' in one:
                model = one.replace('as Data', '').split('import')[-1].strip().lower()
                datamodel = requGet('http://localhost/api/datamodel?name=%s' % model)
                datamodel = datamodel['datamodel']
                dmid = datamodel[0]['_id']
                break
        fi.close()
        filepath = '%s/%s' % (name, filepath[filepath.rindex('/')+1:])
        extra = comment
        create_time = datetime.datetime.now()
        data = {
            "dmid":dmid,
            "name":name,
            "filepath":filepath,
            "extra":comment,
        }
        print requPost('http://localhost/api/unit', data, format='JSON')
        # unit = Unit(dmid=dmid, name=name, filepath=filepath, status=1, extra=comment, create_time=datetime.datetime.now())
        # Unit.insert(unit)
        # print 'Unit %s is set successfully.' % name
    else:
        print 'Unit %s has been set.' % name


def setArticle(filepath, pinyin, host):
    unit = None
    for one in os.listdir(os.path.dirname(filepath)):
        if one.endswith('spider.py'):
            unit = requGet('http://localhost/api/unit?name=%s' % one.replace('spider.py', ''))
            break
    if not unit['unit']:
        print 'Please set unit firstly.'
        return
    unit = unit[0]
    name = host.split('.')
    if len(name) > 2:
        name = name[1]
    else:
        name = name[0]
    name = name.replace('-', '')
    article = requGet('http://localhost/api/article?name=%s&uid=%s' % (name, str(unit['_id'])))
    article = article['article']
    lines = []
    flows = []
    fi = open(filepath, 'r')
    flag = False
    for line in fi.readlines():
        if '@' in line and not 'find' in line and not 'findall' in line:
            lines.append(line.replace('\n', '').replace('  ', ''))
            flag = True
        if 'def ' in line and flag:
            lines.append(line.replace('\n', '').replace('  ', ''))
            flag = False
        if 'initflow' in line and not 'import' in line:
            lines.append(line.replace('\n', '').replace('  ', ''))
            flows.append(line.replace('\n', '').replace('  ', '').replace('@initflow(', '').replace(')', '').replace('"', '').replace("'", ''))
    fi.close()
    sections = {}
    section = {}
    for index, one in enumerate(lines):
        if 'next' in one:
            section['next'] = one.replace('@next(', '').replace(')', '')
        if 'index' in one:
            section['index'] = one.replace('@index(', '').replace(')', '').replace('"', '').replace("'", "")
        if 'retry' in one:
            section['retry'] = one.replace('@retry(', '').replace(')', '')
        if 'timelimit' in one:
            section['timelimit'] = one.replace('@timelimit(', '').replace(')', '')
        if 'store' in one:
            section['store'] = 1
        if 'initflow' in one and not 'import' in one:
            section['flow'] = one.replace('\n', '').replace('  ', '').replace('@initflow(', '').replace(')', '').replace('"', '').replace("'", '')
        if 'def ' in one:
            section['name'] = one.replace('def ', '').split('(')[0]
            sections[section['name']]=section
            section = {}
    if not article:
        # article = Article(uid=unit['_id'], name=name, pinyin=pinyin, host=host, filepath=filepath[filepath.rindex('/')+1:], create_time=datetime.datetime.now())
        # article['_id'] = Article.insert({'username':USER, 'secret':SECRET}, article)
        # print 'Article %s is set successfully.' % name
        data = {
            "uid":unit['_id'],
            "name":name,
            "pinyin":pinyin,
            "host":host,
            "filepath":filepath[filepath.rindex('/')+1:],
        }
        print requPost('http://localhost/api/article', data, format='JSON')
    else:
        print 'Article %s has been set.' % name
    for section_name, section in sections.items():
        if section.get('flow') is None:
            continue
        flow_section = section
        step = 1
        setSection(section['flow'], step, section['name'], sections, article['_id'])


def setSection(flow, step, section_name, sections, article_id):
    data = sections.get(section_name)
    next = data.get('next')
    if next is not None:
        data['next_id'] = setSection(flow, step+1, next, sections, article_id)
    section = requGet('http://localhost/api/section?name=%s&aid=%s&flow=%s' % (name, str(article['_id']), flow))
    section = section['section']
    if not section:
        data = {
            "aid":article_id,
            "next_id":data.get('next_id'),
            "name":section_name,
            "flow":flow,
            "step":step,
            "index":data.get('index'),
            "retry":data.get('retry', 0),
            "timelimit":data.get('timelimit', 30),
            "store":data.get('store', 0)
        }
        section = requPost('http://localhost/api/section', data, format='JSON')
        return section['sid']
        # section = Section(aid=article_id, next_id=section.get('next_id'), name=section_name, flow=flow, step=step, index=section.get('index'), retry=section.get('retry', 0), timelimit=section.get('timelimit', 30), store=section.get('store', 0), create_time=datetime.datetime.now())
        # print 'Section %s %s is set successfully.' % (flow, section_name)
        # return Section.insert({'username':USER, 'secret':SECRET}, section)
    else:
        print 'Section %s %s has been set.' % (flow, section_name)
        return section[0]['_id']


if __name__ == '__main__':
    pass
