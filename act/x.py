#!/usr/bin/python
# coding=utf-8
import time
from webcrawl.godhand import cook
from datakit.mysql.suit import withMysql, dbpc
from task.config.db.mysql import RDB, WDB
from task.model.mysql import initDB

initDB()

space = {'moduleint':0, 'modulestr':0, 'modulelist':0, 'moduledict':0, 'moduleexecute':0, 'moduledecorator':0, 'modulefunction':0, 'moduleclass':0,
    'classint':4, 'classstr':4, 'classlist':4, 'classdict':4, 'classexecute':4, 'classdecorator':4, 'classfunction':4, 'classclass':4,
    'functionint':4, 'functionstr':4, 'functionlist':4, 'functiondict':4, 'functionexecute':4, 'functiondecorator':4, 'functionfunction':4, 'functionclass':4,
}

weight = {'moduleint':0, 'modulestr':1, 'modulelist':20, 'moduledict':50, 'moduleexecute':4, 'moduledecorator':5, 'modulefunction':500, 'moduleclass':1000,
    'classint':0, 'classstr':1, 'classlist':20, 'classdict':50, 'classexecute':4, 'classdecorator':5, 'classfunction':500, 'classclass':1000,
    'functionint':0, 'functionstr':1, 'functionlist':20, 'functiondict':50, 'functionexecute':4, 'functiondecorator':5, 'functionfunction':500, 'functionclass':1000,
}

span = {'#hc':1000, '#hf':500, '#ht':30, '#hd':30, '#he':1}

def combineParams(function, material, params, clsname):
    parent = None
    self = None
    if function['name'] == '__init__' or function['datatype'] == 'class':
        if not function['pid'] == '':
            combineParams(material[function['pid']], material, params, clsname)
            parent = material[function['pid']]['name']
            self = function['name']
        elif function['sid'] > 0:
            combineParams(material[str(function['sid'])], material, params, clsname)
            parent = material[str(function['sid'])]['name']
            self = function['name']
    for one in function['params']:
        if parent == clsname:
            flag = 'S'
        else:
            flag = 'P'
        if material[one]['default'] is None:
            if material[one]['name'] == '':
                if material[one]['xpath'] is None:
                    if one['stype'] == 'function':
                        combineParams(material[one['sid']], material, params, clsname)
                    else:
                        params.insert(0, {'name':material[one]['name'], 'belong':parent, 'flag':flag, 'txt':'db=%s(%s)' % (material[material[one]['sid']]['name'], material[material[one]['pid']]['name'])})
                else:
                    params.insert(0, {'name':material[one]['name'], 'belong':parent, 'flag':flag, 'txt':'way='+material[one['pid']][name]+one['xpath']})
            else:
                params.insert(0, {'name':material[one]['name'], 'belong':parent, 'flag':flag, 'txt':material[one]['name']})
        else:
            params.append({'name':material[one]['name'], 'belong':parent, 'flag':flag, 'txt':'%s="%s"' % (material[one]['name'], material[one]['default']) if material[one]['datatype'] == 'str' else '%s=%s' % (material[one]['name'], material[one]['default'])})

def cook(material, root, additions={}):
    food = ['#!/usr/bin/python', '# coding=utf-8']
    while True:
        hasws = True
        for key, val in material.items():
            hasws = val.has_key('#w') and val.has_key('#s') and hasws
        if hasws:
            break
        for key, val in material.items():
            if val.has_key('#w') and val.has_key('#s'):
                continue
            else:
                if val['datatype'] in ('module', 'class', 'function'):
                    val['#hc'] = 0
                    val['#hf'] = 0
                    val['#ht'] = 0
                    val['#hd'] = 0
                    val['#he'] = 0
                    val['hastxt'] = False
                    val['params'] = []
                    val['decos'] = []
                    if (val['pid'] == '' or val['sid'] == 0):
                        val['#w'] = weight.get(''.join((val['stype'], val['datatype'])), 0)
                        val['#s'] = space.get(''.join((val['stype'], val['datatype'])), 0)
                if val['stype'] == '':
                    continue
                if val['sid'] > 0:
                    parent = str(val['sid'])
                else:
                    parent = root
                bw = material.get(parent, {}).get("#w")
                bs = material.get(parent, {}).get("#s")
                if bw is None or bs is None:
                    continue
                if val['pid']:
                    try:
                        bw = bw + (material.get(val['pid'], {}).get("#w") or 0)
                        bs = bs + (material.get(val['pid'], {}).get("#s") or 0)
                    except:
                        print key, val
                        print material.get(val['pid'], {}).get("#w"), type(material.get(val['pid'], {}).get("#w"))
                        print material.get(val['pid'], {}).get("#s"), type(material.get(val['pid'], {}).get("#s"))
                        raise
                if val['method'] == 'params':
                    # if val['default'] is None:
                    #     material[parent]['params'].insert(0, key)
                    # else:
                    material[parent]['params'].append(key)
                    material[key]["#w"] = 0
                    material[key]["#s"] = 0
                    continue
                elif val['datatype'] == 'class':
                    if val['xpath'] is None and val['default'] is None:
                        material[parent]['#hc'] += 1
                        wh = material[parent]['#hc'] * span['#hc']
                    else:
                        material[parent]['#he'] += 1
                        wh = material[parent]['#he'] * span['#he']
                    val['hastxt'] = False
                    val['params'] = []
                    val['decos'] = []
                elif val['datatype'] == 'function':
                    material[parent]['#hf'] += 1
                    if val['name'] == '__init__':
                        wh = 0 * span['#hf'] + 1
                    elif val['name'] == '__del__':
                        wh = 20 * span['#hf'] + 1
                    else:
                        wh = material[parent]['#hf'] * span['#hf']
                    val['hastxt'] = False
                    val['params'] = []
                    val['decos'] = []
                elif val['datatype'] == 'tuple':
                    material[parent]['#ht'] = material[parent].get('#ht', 0) + 1
                    wh = material[parent]['#ht'] * span['#ht']
                elif val['datatype'] == 'dict':
                    material[parent]['#hd'] = material[parent].get('#hd', 0) + 1
                    wh = material[parent]['#hd'] * span['#hd']
                else:
                    material[parent]['#he'] = material[parent].get('#he', 0) + 1
                    wh = material[parent]['#he'] * span['#he']
                w = bw + wh
                s = bs + space.get(''.join((val['stype'], val['datatype'])), 0)
                material[key]["#w"] = w
                material[key]["#s"] = s
                if material[parent]['datatype'] in ('function', 'class'):
                    material[parent]['hastxt'] = True
    for val in sorted(material.values(), key=lambda m:m['#w']):
        if val['method'] == 'params':
            continue
        elif val['xpath'] is None and val['default'] is None:
            if val['datatype'] == 'class':
                food.append('\n')
                if val['pid'] == '':
                    b = '(object):'
                else:
                    b = '(%s):' % material[val['pid']]['name']
                food.append('%s%s%s%s' % (' ' * val['#s'], 'class ', val['name'], b))
                if not val['hastxt']:
                    food.append('%s%s' % (' ' * (val['#s'] + 4), 'pass'))
            elif val['datatype'] == 'function':
                params = []
                combineParams(val, material, params, material[str(val['sid'])]['name'])
                if val['stype'] == 'class':
                    params.insert(0, {'name':'self', 'belong':material[str(val['sid'])]['name'], 'flag':'S', 'txt':'self'})
                if val.get('store'):
                    store_params = []
                    combineParams(material[val['store']], material, params, material[str(val['sid'])]['name'])
                    food.append('%s%s%s%s' % (' ' * val['#s'], 'def ', val['name'], '(%s):' % ', '.join([one['txt'] for one in params])))
                    food.append('%s@store(%s)' % (' ' * val['#s'], '(%s):' % ', '.join([one['txt'] for one in store_params])))
                if val.get('timelimit'):
                    food.append('%s@timelimit(%s)' % (' ' * val['#s'], val['timelimit']))
                if val.get('retry'):
                    food.append('%s@retry(%s)' % (' ' * val['#s'], val['timelimit']))
                if val.get('index'):
                    food.append('%s@index("%s")' % (' ' * val['#s'], val['index']))
                if val.get('next_id'):
                    food.append('%s@next("%s")' % (' ' * val['#s'], material[val['next_id']]['name']))
                if val.get('initflow'):
                    food.append('%s@initflow("%s")' % (' ' * val['#s'], val['initflow']))
                food.append('%s%s%s%s' % (' ' * val['#s'], 'def ', val['name'], '(%s):' % ', '.join([one['txt'] for one in params])))
                pn = set([one['belong'] for one in params if one['flag'] == 'P'])
                if val['name'] == '__init__' and len(pn) > 0:
                    food.append('%ssuper(%s, self).__init__(%s)' % (' ' * (val['#s'] + 4), material[str(val['sid'])]['name'], ','.join(['%s=%s' % (one['name'], one['name']) for one in params if one['flag'] == 'P'])))
                elif not val['hastxt']:
                    food.append('%s%s' % (' ' * (val['#s'] + 4), 'pass'))
            elif val['datatype'] == 'execute':
                food.append('%s%s%s' % (' ' * val['#s'], material[val['pid']]['name'], '()'))
        elif val['default'] is None:
            if val['content'] == val['name']:
                food.append('%s%s' % (' ' * val['#s'], ' '.join([val['xpath'], val['content']])))
            elif val['datatype'] == 'decorator':
                pass
            else:
                try:
                    if val['stype'] == 'dict':
                        if val['pid'] == '':
                            food.append('%s[%s]="%s"' % (material[str(val['sid'])]['name'], val['index'], val['default']))
                        else:
                            if val['method'] == '%':
                                food.append('%s[%s]="%s"' % (material[str(val['sid'])]['name'], val['index'], val['xpath']%material[str(val['pid'])]['name']))
                            else:
                                food.append('%s[%s]=%s' % (material[str(val['sid'])]['name'], val['index'], material[str(val['pid'])]['name']))
                    elif val['ptype'] == 'datasource':
                        food.append('%s%s=%s' % (' ' * val['#s'], val['name'], '' % ()))
                    elif val['method'] == '%':
                        food.append('%s%s' % (' ' * val['#s'], ' '.join([val['xpath'], val['content'], 'as', val['name']])))
                    else:
                        food.append('%s%s' % (' ' * val['#s'], ' '.join([val['xpath'], val['content'], 'as', val['name']])))
                except:
                    print val['id'], val
                    raise
        else:
            if val['datatype'] == 'str':
                food.append('%s%s="%s"' % (' ' * val['#s'], val['name'], val['default']))
            else:
                food.append('%s%s=%s' % (' ' * val['#s'], val['name'], val['default']))
    food = '\n'.join(food)
    return food

@withMysql(WDB, resutype='DICT')
def u():
    dirfile = dbpc.handler.queryOne(""" select gu.id, gu.dmid, gu.name, concat(gc.val, gu.dirpath, gu.filepath) as filepath from grab_unit gu join grab_config gc on gc.type='ROOT' and gc.key ='dir' where gu.name = %s; """, ('hotel',))
    print '===>>>>', dirfile
    material = {}
    root = ''
    for one in dbpc.handler.queryAll(""" select gd.* from grab_datapath gd where gd.btype=%s and (gd.bid = %s or gd.bid=0); """, ('unit', dirfile['id'])):
        material[str(one['id'])] = one
        if one['datatype'] == 'module':
            root = str(one['id'])
    fi = open(dirfile['filepath'], 'w')
    fi.write(cook(material, root))
    fi.close()
    # for item in dbpc.handler.queryAll(""" select gd.* from grab_datapath gd where gd.btype='unit' and gd.method='classinit' and (gd.bid = 1 or gd.bid=0) order by gd.pid asc, gd.id asc; """):

    # for item in dbpc.handler.queryAll(""" select * from grab_datapath; """):
    #     print item
    # for item in dbpc.handler.queryAll(""" select * from grab_datapath; """):
    #     print item

@withMysql(WDB, resutype='DICT')
def a():
    dirfile = dbpc.handler.queryOne(""" select gu.id, gu.dmid, gu.name, concat(gc.val, gu.dirpath, ga.filepath) as filepath from grab_unit gu join grab_config gc join grab_article ga on gc.type='ROOT' and gc.key ='dir' and ga.uid = gu.id where gu.name = %s and ga.name = %s; """, ('hotel', 'homeinns'))
    print '===>>>>', dirfile
    material = {}
    decos = {}
    additions = {}
    root = ''
    for one in dbpc.handler.queryAll(""" select * from grab_datasource where sid in (select gs.id from grab_article ga join grab_section gs on gs.aid = ga.id where ga.id = %s);  """, (1,)):
        additions[str(id)] = one
    for one in dbpc.handler.queryAll(""" select gs.* from grab_article ga join grab_section gs on gs.aid = ga.id where ga.id = 1; """):
        decos[one['id']] = one
    for one in dbpc.handler.queryAll(""" select * from grab_datapath gd where (gd.btype=%s and (gd.bid = %s or gd.bid=0)) or (gd.btype=%s and (gd.bid in (select gs.id from grab_article ga join grab_section gs on gs.aid = ga.id where ga.id = %s) or gd.bid=0)); """, ('article', 1, 'section', 1)):
        material[str(one['id'])] = one
        if one['datatype'] == 'module':
            root = str(one['id'])
        if one['btype'] == 'section' and one['ptype'] == '' and one['datatype'] in ('function', 'decorator') and one['bid'] in decos:
            material[str(one['id'])]['next_id'] = decos[one['bid']]['next_id']
            material[str(one['id'])]['initflow'] = decos[one['bid']]['initflow']
            material[str(one['id'])]['index'] = decos[one['bid']]['index']
            material[str(one['id'])]['retry'] = decos[one['bid']]['retry']
            material[str(one['id'])]['timelimit'] = decos[one['bid']]['timelimit']
            material[str(one['id'])]['store'] = decos[one['bid']]['store']
    print '<><><>', len(material.items())
    fi = open(dirfile['filepath'], 'w')
    fi.write(cook(material, root))
    fi.close()
    # for item in dbpc.handler.queryAll(""" select gd.* from grab_datapath gd where gd.btype='unit' and gd.method='classinit' and (gd.bid = 1 or gd.bid=0) order by gd.pid asc, gd.id asc; """):

    # for item in dbpc.handler.queryAll(""" select * from grab_datapath; """):
    #     print item
    # for item in dbpc.handler.queryAll(""" select * from grab_datapath; """):
    #     print item

if __name__ == '__main__':
    print 'start'
    a()
    # u()
    print 'end'