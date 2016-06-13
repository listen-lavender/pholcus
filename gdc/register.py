#!/usr/bin/env python
# coding=utf-8
import time, datetime
import os, sys, json
import hashlib
from webcrawl import request
from setting import USER, SECRET, HOST
from version import Store
import task

LIMIT = 20

def persist(filepath, content):
    if filepath.startswith('/'):
        fi = open(filepath, 'w')
    else:
        fi = open(os.path.join(CURRPATH, filepath), 'w')
    fi.write(content)
    fi.close()


def getSection(sid):
    projection = {'step':1, 'index':1, 'additions':1}
    section = request.post('%sgdc/api/section/%s' % (HOST, str(sid)), {'projection':json.dumps(projection), 'limit':'one'}, format='JSON')
    section = section['section']
    return section


def getArticle(aid):
    projection = {'uid':1, 'name':1, 'clsname':1, 'filepath':1, 'digest':1}
    article = request.post('%sgdc/api/article/%s' % (HOST, str(aid)), {'projection':json.dumps(projection), 'limit':'one'}, format='JSON')
    article = article['article']
    filepath = article['filepath']
    if filepath in Store and article['digest'] == Store[filepath]:
        return article
    result = request.get('%sgds/static/exe/%s' % (HOST, filepath), format='TEXT')
    persist(filepath, result)
    Store[filepath] = article['digest']
    return article


def getUnit(uid):
    projection = {'name':1, 'filepath':1, 'digest':1, 'dmid':1}
    unit = request.post('%sgdc/api/unit/%s' % (HOST, str(uid)), {'projection':json.dumps(projection), 'limit':'one'}, format='JSON')
    unit = unit['unit']
    filepath = unit['filepath']
    if filepath in Store and article['digest'] == Store[filepath]:
        return
    result = request.get('%sgds/static/exe/%s' % (HOST, filepath), format='TEXT')
    persist(filepath, result)
    Store[filepath] = unit['digest']

    filepath = os.path.join(os.path.dirname(os.path.join(CURRPATH, filepath)))
    persist(filepath, '#!/usr/bin/env python\n# coding=utf8')
    return unit


def getDatamodel(dmid):
    projection = {'filepath':1, 'digest':1, 'name':1}
    datamodel = request.post('%sgdc/api/datamodel/%s' % (HOST, str(dmid)), {'projection':json.dumps(projection), 'limit':'one'}, format='JSON')
    datamodel = datamodel['datamodel']
    filepath = datamodel['filepath']
    if filepath in Store and article['digest'] == Store[filepath]:
        return
    result = request.get('%sgds/static/exe/%s' % (HOST, filepath), format='TEXT')
    persist(filepath, result)
    Store[filepath] = datamodel['digest']
    return datamodel


def setDatamodel(filepath, fileupdate=False):
    fi = open(filepath, 'r')
    filepath = 'model/%s' % filepath.split('/model/')[-1]
    data = fi.read()
    fi.close()
    keyobj = hashlib.md5()
    keyobj.update(data)
    digest = keyobj.hexdigest()
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
                    model = info[1]
                    break
            if model is not None:
                fileupdate = True
                datamodel = request.post('%sgdc/api/datamodel' % HOST, {'condition':json.dumps({'name':model}), 'limit':'one', 'projection':json.dumps({'_id':1})}, format='JSON')
                datamodel = datamodel['datamodel']
                if datamodel:
                    continue
                data = {
                    "name": model,
                    "table": model.lower(),
                    "filepath": filepath,
                    "comment": comment,
                    'digest': digest
                }
                print request.post('%sgdc/api/datamodel' % HOST, {'data':json.dumps(data)}, format='JSON')
    if fileupdate:
        print request.post('%sgdc/api/datamodel' % HOST, files={'file':(filepath, open(filepath, 'rb'))}, format='JSON')


def setUnit(filepath):
    name = filepath[filepath.rindex('/')+1:].replace('spider.py', '')
    unit = request.post('%sgdc/api/unit' % HOST, {'condition':json.dumps({'name':name}), 'limit':'one', 'projection':json.dumps({'_id':1, 'digest':1})}, format='JSON')
    unit = unit['unit']
    keyobj = hashlib.md5()
    dmid = None
    fi = open(filepath, 'r')
    for one in fi.readlines():
        keyobj.update(one)
        if 'as Data' in one:
            model = one.replace('as Data', '').split('import')[-1].strip().lower()
            datamodel = request.post('%sgdc/api/datamodel' % HOST, {'condition':json.dumps({'name':model}), 'limit':'one', 'projection':json.dumps({'_id':1})}, format='JSON')
            datamodel = datamodel['datamodel']
            dmid = datamodel['_id']
            break
    fi.close()
    digest = keyobj.hexdigest()
    data = {}
    files = None
    displaypath = 'task/%s/%s' % (name, filepath[filepath.rindex('/')+1:])
    if not unit:
        data = {
            "dmid": dmid,
            "name": name,
            "filepath": displaypath,
            "desc": '',
            "digest": digest
        }
    if unit and not unit['digest'] == digest:
        files = {'file':(displaypath, open(filepath, 'rb'))}
    if data or files:
        print request.post('%sgdc/api/unit' % HOST, {'data':json.dumps(data)}, files=files, format='JSON')
    else:
        print 'Unit %s has been set.' % name


def setArticle(filepath):
    unit = None
    for one in os.listdir(os.path.dirname(filepath)):
        if one.endswith('spider.py'):
            unit = request.post('%sgdc/api/unit' % HOST, {'condition':json.dumps({'name':one.replace('spider.py', '')}), 'limit':'one', 'projection':json.dumps({'_id':1})}, format='JSON')
            unit = unit['unit']
            break
    if not unit:
        print 'Please set unit firstly.'
        return
    name = filepath[filepath.rindex('/')+1:filepath.rindex('.')]
    clsname = ''
    article = request.post('%sgdc/api/article' % HOST, {'condition':json.dumps({'name':name, 'uid':str(unit['_id'])}), 'limit':'one', 'projection':json.dumps({'_id':1, 'digest':1})}, format='JSON')
    article = article['article']
    lines = []
    flows = []
    fi = open(filepath, 'r')
    flag = False
    keyobj = hashlib.md5()
    for line in fi.readlines():
        keyobj.update(line)
        if line.startswith('class '):
            clsname = line.replace('class ', '').split('(')[0]
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
    digest = keyobj.hexdigest()
    data = {}
    files = {}
    displaypath = filepath[filepath.rindex('task/'):]
    if not article:
        data = {
            "uid": unit['_id'],
            "name": name,
            "clsname": clsname,
            "filepath": displaypath,
            "digest": digest
        }
    if article and not article['digest'] == digest:
        files = {'file': (displaypath, open(filepath, 'rb'))}
    if data or files:
        print request.post('%sgdc/api/article' % HOST, {'data':json.dumps(data)}, files=files, format='JSON')
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
    section = request.post('%sgdc/api/section' % HOST, {'condition':json.dumps({'name':section_name, 'aid':str(article_id), 'flow':flow}), 'limit':'one', 'projection':json.dumps({'_id':1})}, format='JSON')
    section = section['section']
    if section:
        print 'Section %s %s has been set.' % (flow, section_name)
        return section['_id']
    else:
        data = {
            "aid": article_id,
            "next_id": data.get('next_id'),
            "name": section_name,
            "flow": flow,
            "step": step,
            "index": data.get('index'),
            "retry": data.get('retry', 0),
            "timelimit": data.get('timelimit', 30),
            "store": data.get('store', 0)
        }
        section = request.post('%sgdc/api/section' % HOST, {'data':json.dumps(data)}, format='JSON')
        return section['sid']


if __name__ == '__main__':
    pass
