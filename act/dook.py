#!/usr/bin/python
# coding=utf-8
import time
from webcrawl.godhand import cook
from datakit.mysql.suit import withMysql, dbpc
from task.config.db.mysql import RDB, WDB
from task.model.mysql import initDB

initDB()

DISTINCT = True

def treeWeight(tree, node):
    tree[node]["#w"] = 1
    if len(tree[node]["#children"]) > 0:
        for one in tree[node]["#children"]:
            tree[node]["#w"] += treeWeight(tree, one)
    if tree[node]['#pre']:
        for one in tree[node]['#pre']:
            tree[node]["#w"] += treeWeight(tree, one)
    if tree[node]['#decorators']:
        for one in tree[node]['#decorators']:
            tree[node]["#w"] += treeWeight(tree, one)
    if tree[node]['#next']:
        for one in tree[node]['#next']:
            tree[node]["#w"] += treeWeight(tree, one)
    return tree[node]["#w"]

def treeSpace(material, tree, node, num):
    if material.get(node, {"stype":""})["stype"] in ('class', 'function', '') and not material.get(node, {"method":""})['method'] == 'decorate':
        tree[node]["#s"] = num + 4
    else:
        tree[node]["#s"] = num
    if len(tree[node]["#children"]) > 0:
        for one in tree[node]["#children"]:
            treeSpace(material, tree, one, tree[node]["#s"])
    if tree[node]['#pre']:
        for one in tree[node]['#pre']:
            treeSpace(material, tree, one, tree[node]["#s"])
    if tree[node]['#decorators']:
        for one in tree[node]['#decorators']:
            treeSpace(material, tree, one, tree[node]["#s"])
    if tree[node]['#next']:
        for one in tree[node]['#next']:
            treeSpace(material, tree, one, tree[node]["#s"])

def initParams(material, tree):
    for k, v in material.items():
        if v['datatype'] == 'params':
            if '#params' in tree[material[k]['sid']]:
                tree[material[k]['sid']]['#params'].append(k)
            else:
                tree[material[k]['sid']]['#params'] = [k]

def findParams(material, tree, node, route='', parents=[], params=[]):
    route = route + '%s,' % node
    if parents:
        if material[node]['method'] == 'params' and material[node]['pid'] and material[material[node]['pid']]['datatype'] == 'class':
            findParams(material, tree, material[node]['pid'], route, parents, params)
        if material[node]['method'] == 'init' and material[node]['stype'] == 'class':
            findParams(material, tree, str(material[node]['sid']), route, parents, params)
    if tree[node]:
        for one in tree[node]['#params']:
            if material[one]['datatype'] == 'class':
                route = route + '%s,' % one
                findParams(material, tree, one, route, parents, params)
            else:
                route = route + node
                for p in parents:
                    if ('%s,' % p) in route:
                        belong = p
                        break
                else:
                    belong = None
                if material[one]['default'] is None:
                    params.insert(0, {'name':material[one]['name'], 'belong':belong, 'txt':material[one]['name']})
                else:
                    params.append({'name':material[one]['name'], 'belong':belong, 'txt':'%s="%s"' % (material[one]['name'], material[one]['default']) if material[one]['datatype'] == 'str' else '%s=%s' % (material[one]['name'], material[one]['default'])})

def nodeTxt(material, tree, node):
    if node > '0':
        if material[node]['datatype'] and material[node]['datatype'] in ('module'):
            return ''
        elif material[node]['method'] in ('params'):
            return ''
        elif material[node]['method'] in ('decorate'):
            if material[node]['default'] is not None:
                txt = '\n%s@%s("%s")' % (' ' * tree[node]['#s'], material[node]['name'], material[node]['default']) if material[node]['datatype'] == 'str' else '\n%s@%s(%s)' % (' ' * tree[node]['#s'], material[node]['name'], material[node]['default'])
                return txt
            return ''
        elif material[node]['method'] in ('find'):
            return '%s%s = get%sNodeContent(%s.find("%s"), %s)' % (' ' * tree[node]['#s'], material[node]['name'], tree[material[node]['pid']]['#format'], material[material[node]['pid']]['name'], material[node]['xpath'], '"TEXT"' if material[node]['content'] == 'TEXT' else material[node]['content']) + '\n'
        elif material[node]['method'] in ('findall'):
            return ''
        elif material[node]['datatype'] in ('find'):
            return ''
        elif material[node]['datatype'] in ('decorator') and material[node]['name'] == '':
            return ''
        elif material[node]['stype'] in ('dict', 'list'):
            if material[node]['method'] == 'init':
                if material[node]['default'] is None:
                    val = '%s' % material[material[node]['pid']]['name']
                else:
                    val = '"%s"' % material[node]['default'] if material[node]['datatype'] == 'str' else material[node]['default']
            else:
                val = '"%s" %s %s' % (material[node]['xpath'], material[node]['method'], material[material[node]['pid']]['name'])
            if material[node]['stype'] == 'dict':
                return '%s%s["%s"] = %s\n' % (' ' * tree[node]['#s'], material[str(material[node]['sid'])]['name'], material[node]['index'], val)
            else:
                return '%s%s[%s] = %s\n' % (' ' * tree[node]['#s'], material[str(material[node]['sid'])]['name'], material[node]['index'], val)
        elif material[node]['xpath'] is None and material[node]['default'] is None:
            txt = '\n'
            if material[node]['datatype'] == 'class':
                if tree[node]['#params']:
                    b = '(%s):' % ', '.join([material[one]['name'] for one in tree[node]['#params']])
                else:
                    b = '(object):'
                txt += '%s%s%s%s' % (' ' * tree[node]['#s'], 'class ', material[node]['name'], b)
                if not tree[node]['#hastxt']:
                    txt += '%s%s' % (' ' * (material[node]['#s'] + 4), 'pass')
                return txt + '\n'
            elif material[node]['datatype'] == 'function':
                txt = '\n'
                params = []
                if material[node]['name'] == '':
                    return ''
                if material[node]['name'] == '__init__':
                    parents = []
                    for one in tree[str(material[node]['sid'])]['#params']:
                        if material[one]['pid'] and material[material[one]['pid']]['datatype'] == 'class':
                            parents.append(material[one]['pid'])
                    findParams(material, tree, node, parents=parents, params=params)
                else:
                    findParams(material, tree, node, params=params)
                if material[node]['stype'] == 'class':
                    params.insert(0, {'name':'self', 'belong':None, 'txt':'self'})
                txt += '%s%s%s%s' % (' ' * tree[node]['#s'], 'def ', material[node]['name'], '(%s):' % ', '.join([one['txt'] for one in params]))
                if material[node]['name'] == '__init__' and len(set([one['belong'] for one in params if one['belong'] is not None])) > 0:
                    if len(parents) == 1:
                        txt += '\n%ssuper(%s, self).__init__(%s)' % (' ' * (tree[node]['#s'] + 4), material[str(material[node]['sid'])]['name'], ', '.join(['%s=%s' % (one['name'], one['name']) for one in params if one['belong'] is not None]))
                    else:
                        for p in parents:
                            txt += '%s%s.__init__(self, %s)' % (' ' * (tree[node]['#s'] + 4), material[p]['name'], ', '.join(['%s=%s' % (one['name'], one['name']) for one in params if one['belong'] == p]))
                elif not tree[node]['#hastxt']:
                    txt += '\n%s%s' % (' ' * (tree[node]['#s'] + 4), 'pass')
                return txt + '\n'
            elif material[node]['datatype'] == 'execute':
                params = []
                findParams(material, tree, node, params=params)
                if material[node]['name'] == '':
                    return '%s%s(%s)' % (' ' * tree[node]['#s'], material[material[node]['pid']]['name'], ', '.join([one['txt'] for one in params])) + '\n'
                else:
                    return '%s%s = %s(%s)' % (' ' * tree[node]['#s'], material[node]['name'], material[material[node]['pid']]['name'], ', '.join([one['txt'] for one in params])) + '\n'
            else:
                return ' ' * tree[node]['#s'] + material[node]['name'] + '\n'
        elif material[node]['default'] is None:
            if material[node]['content'] == material[node]['name']:
                return '%s%s' % (' ' * tree[node]['#s'], ' '.join([material[node]['xpath'], material[node]['content']])) + '\n'
            else:
                try:
                    return '%s%s' % (' ' * tree[node]['#s'], ' '.join([material[node]['xpath'], material[node]['content'], 'as', material[node]['name']])) + '\n'
                except:
                    print node
                    print tree[node]
                    print material[node]
                    raise
        else:
            if material[str(material[node]['sid'])]['datatype'] == 'class' or material[str(material[node]['sid'])]['name'] == '__init__':
                return '%sself.%s = "%s"\n' % (' ' * tree[node]['#s'], material[node]['name'], material[node]['default']) if material[node]['datatype'] == 'str' else '%sself.%s = %s\n' % (' ' * tree[node]['#s'], material[node]['name'], material[node]['default'])
            else:
                return '%s%s = "%s"\n' % (' ' * tree[node]['#s'], material[node]['name'], material[node]['default']) if material[node]['datatype'] == 'str' else '%s%s = %s\n' % (' ' * tree[node]['#s'], material[node]['name'], material[node]['default'])
    else:
        return ''

def treeTxt(material, tree, node):
    txt = ''
    if tree[node]['#next']:
        order = [(one, tree[one]["#w"]) for one in tree[node]["#next"]]
        order.sort(key=lambda m:m[-1])
        for one in order:
            txt += treeTxt(material, tree, one[0])
    if tree[node]['#pre']:
        order = [(one, tree[one]["#w"]) for one in tree[node]["#pre"]]
        order.sort(key=lambda m:m[-1])
        for one in order:
            txt += treeTxt(material, tree, one[0])
    if tree[node]['#decorators']:
        order = [(one, tree[one]["#w"]) for one in tree[node]["#decorators"]]
        order.sort(key=lambda m:m[-1])
        for one in order:
            txt += treeTxt(material, tree, one[0])
    if DISTINCT:
        if not tree[node]['#used']:
            txt += nodeTxt(material, tree, node)
            tree[node]['#used'] = True
    else:
        txt += nodeTxt(material, tree, node)
    if len(tree[node]["#children"]) > 0:
        order = [(one, tree[one]["#w"]) for one in tree[node]["#children"]]
        order.sort(key=lambda m:m[-1])
        for one in order:
            txt += treeTxt(material, tree, one[0])
    return txt

def initTree(material):
    tree = {'0':{'#w':0, '#s':0,
        '#children':[],
        '#params':[],
        '#decorators':[],
        '#next':[], '#pre':[], '#store':None,
        '#used':False
    }}
    pieces = material.items()
    total = len(pieces)
    num = 0
    while True:
        for key, val in pieces:
            if key in tree:
                continue
            if str(val['sid']) in tree:
                num += 1
                tree[key] = {'#w':0, '#s':0, '#children':[], '#hastxt':False, '#params':[], '#decorators':[], '#next':[], '#pre':[], '#store':None, '#used':False}
                if val['method'] in ['params']:
                    tree[str(val['sid'])]["#params"].append(key)
                elif val['method'] in ['init'] and material.get(str(val['sid']), {"datatype":""})["datatype"] in ['execute']:
                    tree[str(val['sid'])]["#params"].append(key)
                    # tree[str(material[str(val['sid'])]['sid'])]["#children"].append(key)
                    tree[str(val['sid'])]["#next"].append(key)
                elif val['method'] == 'decorate':
                    tree[str(val['sid'])]['#decorators'].append(key)
                    if val['name'] == 'next':
                        tree[str(val['sid'])]['#next'].append(key)
                    if val['name'] == 'store':
                        tree[str(val['sid'])]['#store'] = key
                elif material.get(str(val['sid']), {"name":"None"})['name'] == "":
                    tree[str(val['sid'])]['#pre'].append(key)
                    if val['pid']:
                        tree[str(val['sid'])]['#next'].append(val['pid'])
                        tree[str(val['sid'])]['#next'] = list(set(tree[str(val['sid'])]['#next']))
                else:
                    tree[str(val['sid'])]['#children'].append(key)
                    tree[str(val['sid'])]['#hastxt'] = True
                if val['name'] == 'format' and material[str(val['sid'])]['datatype'] == 'execute':
                    tree[str(val['sid'])]['#format'] = val['default'].capitalize()
        time.sleep(0.1)
        if total == num:
            break
    return tree

def cook(material):
    default = '#!/usr/bin/python\n# coding=utf-8\n\n'
    tree = initTree(material)
    treeWeight(tree, '0')
    treeSpace(material, tree, '0', -8)
    initParams(material, tree)
    food = default + treeTxt(material, tree, '0')
    return food
    
@withMysql(WDB, resutype='DICT')
def u():
    dirfile = dbpc.handler.queryOne(""" select gu.dmid, gu.name, concat(gc.val, gu.dirpath, gu.filepath) as filepath from grab_unit gu join grab_config gc on gc.type='ROOT' and gc.key ='dir' where gu.name = 'hotel'; """)
    material = {}
    for one in dbpc.handler.queryAll(""" select gd.* from grab_datapath gd where (gd.btype='unit' and (gd.bid = 1 or gd.bid=0)) or gd.sid in (select gd.id from grab_datapath gd where gd.btype='unit' and gd.bid = 1) order by gd.pid asc, gd.id asc; """):
        material[str(one['id'])] = one
    cook(material)
    fi = open(dirfile['filepath'], 'w')
    fi.write(cook(material))
    fi.close()

@withMysql(WDB, resutype='DICT')
def a():
    dirfile = dbpc.handler.queryOne(""" select gu.dmid, gu.name, concat(gc.val, gu.dirpath, ga.filepath) as filepath from grab_unit gu join grab_config gc join grab_article ga on gc.type='ROOT' and gc.key ='dir' and ga.uid =gu.id where gu.name = 'hotel' and ga.name = 'homeinns'; """)
    material = {}
    for one in dbpc.handler.queryAll(""" select gd.* from grab_datapath gd where gd.id > 16; """):
        material[str(one['id'])] = one
    fi = open(dirfile['filepath'], 'w')
    fi.write(cook(material))
    fi.close()

if __name__ == '__main__':
    print 'start'
    u()
    a()
    print 'end'