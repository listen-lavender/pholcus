#!/usr/bin/python
# coding=utf-8
import time

DISTINCT = True

def treeWeight(tree, node):
    tree[node]["#w"] = 1
    if tree[node]['#params']:
        for one in tree[node]['#params']:
            tree[node]["#w"] += treeWeight(tree, one)
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
    if material.get(node, {"stype":""})["stype"] in ('class', 'function', '') and not material.get(node, {"method":""})['method'] == '@':
        tree[node]["#s"] = num + 4
    else:
        tree[node]["#s"] = num
    if material.get(node, {"stype":""})["stype"] == 'list':
        childnum = tree[node]["#s"] + 4
    else:
        childnum = tree[node]["#s"]
    if len(tree[node]["#children"]) > 0:
        for one in tree[node]["#children"]:
            if tree[one]['#routed'] and tree[one]['#routed'] > 3:
                continue
            tree[one]['#routed'] = 3
            treeSpace(material, tree, one, childnum)
    if tree[node]['#pre']:
        for one in tree[node]['#pre']:
            if tree[one]['#routed'] and tree[one]['#routed'] > 2:
                continue
            tree[one]['#routed'] = 2
            treeSpace(material, tree, one, childnum)
    if tree[node]['#decorators']:
        for one in tree[node]['#decorators']:
            if tree[one]['#routed'] and tree[one]['#routed'] > 2:
                continue
            tree[one]['#routed'] = 2
            treeSpace(material, tree, one, childnum)
    if tree[node]['#next']:
        for one in tree[node]['#next']:
            if tree[one]['#routed'] and tree[one]['#routed'] > 1:
                continue
            tree[one]['#routed'] = 1
            treeSpace(material, tree, one, childnum)
            if material[one]['datatype'] in ('function', 'execute'):
                treeSpace(material, tree, one, childnum-4)
            else:
                treeSpace(material, tree, one, childnum)

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
                if material[one]['datatype'] == 'execute':
                    params.append({'name':material[one]['name'], 'belong':belong, 'txt':'%s=%s(%s%s)' % (material[one]['name'], material[str(material[material[one]['pid']]['sid'])]['name'], material[material[material[one]['pid']]['pid']]['name'], material[material[one]['pid']]['xpath'])})
                elif material[one]['datatype'] == 'method':
                    params.append({'name':material[one]['name'], 'belong':belong, 'txt':'%s=%s%s' % (material[one]['name'], material[material[one]['pid']]['name'], material[one]['xpath'])})
                elif material[one]['default'] is None:
                    if material[one]['stype'] == 'execute':
                        params.insert(0, {'name':material[one]['name'], 'belong':belong, 'txt':'%s=%s' % (material[one]['name'], material[one]['name'])})
                    else:
                        params.insert(0, {'name':material[one]['name'], 'belong':belong, 'txt':'%s' % material[one]['name']})
                else:
                    params.append({'name':material[one]['name'], 'belong':belong, 'txt':'%s="%s"' % (material[one]['name'], material[one]['default']) if material[one]['datatype'] == 'str' else '%s=%s' % (material[one]['name'], material[one]['default'])})

def nodeDecorate(material, tree, node):
    if material[node]['default'] is not None:
        txt = '\n%s@%s("%s")' % (' ' * tree[node]['#s'], material[node]['name'], material[node]['default']) if material[node]['datatype'] == 'str' else '\n%s@%s(%s)' % (' ' * tree[node]['#s'], material[node]['name'], material[node]['default'])
        return txt
    if material[node]['name'] == 'next' and material[node]['pid']:
        txt = '\n%s@%s(%s)' % (' ' * tree[node]['#s'], material[node]['name'], material[material[node]['pid']]['name'])
        return txt
    if material[node]['name'] == 'store':
        if not material[node]['datatype'] == 'None':
            params = []
            findParams(material, tree, node, params=params)
            txt = '\n%s@%s(%s)' % (' ' * tree[node]['#s'], material[node]['name'], ', '.join(one['txt'] for one in params))
            return txt
    return ''

def nodeClass(material, tree, node):
    txt = '\n'
    if tree[node]['#params']:
        b = '(%s):' % ', '.join([material[one]['name'] for one in tree[node]['#params']])
    else:
        b = '(object):'
    txt += '%s%s%s%s' % (' ' * tree[node]['#s'], 'class ', material[node]['name'], b)
    if not tree[node]['#hastxt']:
        txt += '%s%s' % (' ' * (material[node]['#s'] + 4), 'pass')
    return txt + '\n'

def nodeFunction(material, tree, node):
    txt = '\n'
    params = []
    if material[node]['name'] == '':
        return ''
    if material[node]['name'] == '__init__':
        parents = []
        for one in tree[str(material[node]['sid'])]['#params']:
            try:
                if material[one]['pid'] and material[material[one]['pid']]['datatype'] == 'class':
                    parents.append(material[one]['pid'])
            except:
                print one
                print material[one]['pid']
                raise
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

def nodeImport(material, tree, node):
    if material[node]['content'] == material[node]['name']:
        return '%s%s' % (' ' * tree[node]['#s'], ' '.join([material[node]['xpath'], material[node]['content']])) + '\n'
    else:
        return '%s%s' % (' ' * tree[node]['#s'], ' '.join([material[node]['xpath'], material[node]['content'], 'as', material[node]['name']])) + '\n'

def findIndex(material, node):
    indexs = []
    while True:
        if material[node]['index']:
            indexs.insert(0, node)
            node = str(material[node]['sid'])
        else:
            break
    return node, indexs

def nodeAssignleft(material, tree, node):
    root, indexs = findIndex(material, node)
    name = '%s%s' % (material[root]['name'], ''.join(['["%s"]' % material[one]['index'] if material[str(material[one]['sid'])]['datatype'] == 'dict' else '[%s]' % material[one]['index'] for one in indexs]))
    if material[str(material[node]['sid'])]['datatype'] == 'class' or material[str(material[node]['sid'])]['name'] == '__init__':
        return 'self.%s' % name
    else:
        return name

def nodeAssignright(material, tree, node):
    if material[node]['default'] is None:
        if material[node]['datatype'] == 'execute':
            params = []
            findParams(material, tree, node, params=params)
            txt = '%s(%s)' % (material[material[node]['pid']]['name'], ', '.join([one['txt'] for one in params]))
            return txt
        elif material[node]['method'] == '.find':
            pid = material[node]['pid']
            bid = None
            while True:
                if bid is None and material[pid]['datatype'] in ('object', 'execute'):
                    bid = material[node]['pid']
                if material[pid]['datatype'] == 'execute':
                    break
                else:
                    pid = material[pid]['pid']
            if material[node]['xpath'] is None:
                return 'get%sNodeContent(%s, %s)' % (tree[pid]['#format'], material[bid]['name'], '"TEXT"' if material[node]['content'] == 'TEXT' else material[node]['content'])
            else:
                return 'get%sNodeContent(%s.find("%s"), %s)' % (tree[pid]['#format'], material[bid]['name'], material[node]['xpath'], '"TEXT"' if material[node]['content'] == 'TEXT' else material[node]['content'])
        elif material[node]['method'] == '.findall':
            return '%s.findall("%s")' % (material[material[node]['pid']]['name'], material[node]['xpath'])
        elif material[node]['method'] == '%':
            if material[material[node]['pid']]['datatype'] == 'class' or material[str(material[material[node]['pid']]['sid'])]['name'] == '__init__':
                return '"%s" %s self.%s' % (material[node]['xpath'], material[node]['method'], material[material[node]['pid']]['name'])
            elif material[material[node]['pid']]['name']:
                return '"%s" %s %s' % (material[node]['xpath'], material[node]['method'], material[material[node]['pid']]['name'])
            else:
                return '"%s" %s %s["%s"]' % (material[node]['xpath'], material[node]['method'], material[str(material[material[node]['pid']]['sid'])]['name'], material[material[node]['pid']]['index'])
        else:
            if material[material[node]['pid']]['datatype'] == 'class' or material[str(material[material[node]['pid']]['sid'])]['name'] == '__init__':
                return 'self.%s' % material[material[node]['pid']]['name'] + ('' if material[node]['xpath'] is None else material[node]['xpath'])
            else:
                return material[material[node]['pid']]['name'] + ('' if material[node]['xpath'] is None else material[node]['xpath'])
    else:
        if material[node]['datatype'] == 'str':
            return '"%s"' % material[node]['default']
        else:
            return material[node]['default']

def nodeCommon(material, tree, node):
    return '%s%s = %s\n' % (' ' * tree[node]['#s'], nodeAssignleft(material, tree, node), nodeAssignright(material, tree, node))

def nodeExecute(material, tree, node):
    params = []
    findParams(material, tree, node, params=params)
    if material[node]['name'] == '':
        return '%s%s(%s)' % (' ' * tree[node]['#s'], material[material[node]['pid']]['name'], ', '.join(['%s=%s'%(one['name'], one['name']) for one in params])) + '\n'
    else:
        return '%s%s = %s(%s)' % (' ' * tree[node]['#s'], material[node]['name'], material[material[node]['pid']]['name'], ', '.join(['%s=%s'%(one['name'], one['name']) for one in params])) + '\n'

def nodeFor(material, tree, node):
    return '%sfor %s in %s:\n' % (' ' * tree[node]['#s'], material[node]['name'], material[material[node]['pid']]['name'])

def nodeYield(material, tree, node):
    if material[node]['datatype'] == 'object':
        return '%syield %s(%s)\n' % (' ' * tree[node]['#s'], material[material[node]['pid']]['name'], ', '.join(['%s=%s' % (material[one]['name'], material[one]['name']) for one in tree[node]['#pre']]))
    else:
        return '%syield %s\n' % (' ' * tree[node]['#s'], material[node]['name'])

def nodeTxt(material, tree, node):
    if not node in material:
        return ''
    if material[node]['method'] in ('params'):
        return ''
    elif material[node]['method'] == 'import':
        return nodeImport(material, tree, node)
    elif material[node]['method'] == 'init':
        txt = '\n'
        if material[node]['datatype'] == 'module':
            return ''
        elif material[node]['datatype'] == 'class':
            return nodeClass(material, tree, node)
        elif material[node]['datatype'] == 'function':
            return nodeFunction(material, tree, node)
        elif material[node]['datatype'] == 'execute':
            return nodeExecute(material, tree, node)
        else:
            return ''
    elif material[node]['method'] == '@':
        return nodeDecorate(material, tree, node)
    elif material[node]['method'] == 'in':
        return nodeFor(material, tree, node)
    elif material[node]['method'] == 'yield':
        return nodeYield(material, tree, node)
    else:
        return nodeCommon(material, tree, node)

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
        '#used':False,
        '#routed':None
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
                tree[key] = {'#w':0, '#s':0, '#children':[], '#hastxt':False, '#params':[], '#decorators':[], '#next':[], '#pre':[], '#store':None, '#used':False, '#routed':None}
                if val['method'] in ['params']:
                    tree[str(val['sid'])]["#params"].append(key)
                elif val['method'] in ['='] and material.get(str(val['sid']), {"datatype":""})["datatype"] in ['execute']:
                    tree[str(val['sid'])]["#params"].append(key)
                    # tree[str(material[str(val['sid'])]['sid'])]["#children"].append(key)
                    tree[str(val['sid'])]["#next"].append(key)
                elif val['method'] == '@':
                    tree[str(val['sid'])]['#decorators'].append(key)
                    if val['name'] == 'next' and val['pid']:
                        tree[str(val['sid'])]["#next"].append(val['pid'])
                    if val['name'] == 'store':
                        tree[str(val['sid'])]['#store'] = key
                elif material.get(str(val['sid']), {"name":"None"})['name'] == "":
                    tree[str(val['sid'])]['#pre'].append(key)
                    if val['pid']:
                        tree[str(val['sid'])]['#next'].append(val['pid'])
                        tree[str(val['sid'])]['#next'] = list(set(tree[str(val['sid'])]['#next']))
                elif val['method'] == '.findall':
                    tree[key]['#pre'].append(val['pid'])
                    tree[str(val['sid'])]['#children'].append(key)
                    tree[str(val['sid'])]['#hastxt'] = True
                else:
                    if val['method'] == 'yield' and val['name']:
                        tree[key]['#next'].append(val['pid'])
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
    food = default + treeTxt(material, tree, '0') + '\nif __name__ == "__main__":\n    pass\n\n'
    return food

if __name__ == '__main__':
    pass