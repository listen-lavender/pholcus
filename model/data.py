#!/usr/bin/env python
# coding=utf-8

from setting import baseorm, dataorm

class MarkModel(dataorm.Model):
    create_time = dataorm.DatetimeField(ddl='datetime', updatable=False)
    update_time = dataorm.DatetimeField(ddl='timestamp')
    tid = baseorm.IdField(unique='data', updatable=False)

    def __init__(self, **attributes):
        # self.__mappings__['create_time'] = dataorm.DatetimeField(ddl='datetime')
        # self.__mappings__['update_time'] = dataorm.DatetimeField(ddl='datetime')
        # self.__mappings__['tid'] = baseorm.IdField(unique='data', updatable=False)
        attributes['create_time'] = attributes.get('create_time', datetime.datetime.now())
        attributes['update_time'] = attributes.get('update_time', datetime.datetime.now())
        for key in self.__mappings__:
            if not key in attributes:
                raise Exception('Need field %s. ' % key)
            attributes[key] = self.__mappings__[key].check_value(attributes[key])
        super(MarkModel, self).__init__(**attributes)

    def __setstate__(self, state):
        self.__dict__ = state

    def __getstate__(self):
        return self.__dict__


'''
@comment('代理数据')
'''
class Proxy(MarkModel):
    __table__ = 'grab_proxy'
    ip = dataorm.StrField(ddl='varchar(20)', unique='data', updatable=False)
    port = dataorm.IntField(ddl='int(10)', unique='data', updatable=False)
    location = dataorm.StrField(ddl='varchar(30)')
    safetype = dataorm.StrField(ddl='varchar(30)')
    protocol = dataorm.StrField(ddl='varchar(30)')
    refspeed = dataorm.FloatField(ddl='float')
    usespeed = dataorm.FloatField(ddl='float')
    usenum = dataorm.IntField(ddl='int(10)')
    status = dataorm.IntField(ddl='tinyint(1)')
    extra = dataorm.StrField(ddl='varchar(300)')
    creator = dataorm.IdField()
    updator = dataorm.IdField()


'''
@comment('视频数据')
'''
class Video(MarkModel):
    __table__ = 'video'
    cat = dataorm.ListField(ddl='list', comment='资源分类')
    url = dataorm.StrField(ddl='str', comment='资源地址')
    format = dataorm.StrField(ddl='str', comment='资源格式')
    size = dataorm.IntField(ddl='int', comment='资源大小')
    during = dataorm.IntField(ddl='int', comment='资源时常')
    tag = dataorm.ListField(ddl='list', comment='资源标签')
    name = dataorm.StrField(ddl='str', comment='资源名称')
    desc = dataorm.StrField(ddl='str', comment='资源描述')
    cover = dataorm.StrField(ddl='str', comment='资源封面')
    # director = dataorm.StrField(ddl='str')
    # actor = dataorm.ListField(ddl='list')
    # role = dataorm.ListField(ddl='list')
    author = dataorm.StrField(ddl='str', comment='资源作者')
    owner = dataorm.DictField(ddl='dict', comment='资源拥有者')
    # url_type = dataorm.StrField(ddl='str')
    snum = dataorm.IntField(ddl='int', comment='资源序号')
    src = dataorm.StrField(ddl='str', comment='资源来源')
    host = dataorm.StrField(ddl='str', comment='资源域名')
    page_url = dataorm.StrField(ddl='str', comment='资源原页面地址')
    page_id = dataorm.IntField(ddl='int', unique='data', updatable=False, comment='资源页面id')
    parent_page_id = dataorm.IntField(ddl='int', comment='资源父页面id')
    atime = dataorm.StrField(ddl='str', comment='资源来源时间')

'''
@comment('音频数据')
'''
class Audio(MarkModel):
    __table__ = 'audio'
    cat = dataorm.ListField(ddl='list', comment='资源分类')
    url = dataorm.StrField(ddl='str', comment='资源地址')
    format = dataorm.StrField(ddl='str', comment='资源格式')
    size = dataorm.IntField(ddl='int', comment='资源大小')
    during = dataorm.IntField(ddl='int', comment='资源时长')
    tag = dataorm.ListField(ddl='list', comment='资源标签')
    name = dataorm.StrField(ddl='str', comment='资源名称')
    desc = dataorm.StrField(ddl='str', comment='资源描述')
    cover = dataorm.StrField(ddl='str', comment='资源封面')
    singer = dataorm.StrField(ddl='str', comment='资源歌手')
    # url_type = dataorm.StrField(ddl='str')
    snum = dataorm.IntField(ddl='int', comment='资源序号')
    src = dataorm.StrField(ddl='str', comment='资源来源')
    host = dataorm.StrField(ddl='str', comment='资源域名')
    page_url = dataorm.StrField(ddl='str', comment='资源原页面地址')
    page_id = dataorm.IntField(ddl='int', unique='data', updatable=False, comment='资源页面id')
    parent_page_id = dataorm.IntField(ddl='int', comment='资源父页面id')
    atime = dataorm.DatetimeField(ddl='datetime', comment='资源来源时间')

'''
@comment('漫画数据')
'''
class Comic(MarkModel):
    __table__ = 'comic'
    cat = dataorm.ListField(ddl='list', comment='资源分类')
    url = dataorm.StrField(ddl='str', comment='资源地址')
    tag = dataorm.ListField(ddl='list', comment='资源标签')
    name = dataorm.StrField(ddl='str', comment='资源名称')
    desc = dataorm.StrField(ddl='str', comment='资源描述')
    cover = dataorm.StrField(ddl='str', comment='资源封面')
    # director = dataorm.StrField(ddl='str')
    # actor = dataorm.ListField(ddl='list')
    # role = dataorm.ListField(ddl='list')
    author = dataorm.StrField(ddl='str', comment='资源作者')
    owner = dataorm.DictField(ddl='dict', comment='资源拥有者')
    # url_type = dataorm.StrField(ddl='str')
    snum = dataorm.IntField(ddl='int', comment='资源序号')
    src = dataorm.StrField(ddl='str', comment='资源来源')
    host = dataorm.StrField(ddl='str', comment='资源域名')
    page_url = dataorm.StrField(ddl='str', comment='资源原页面地址')
    page_id = dataorm.IntField(ddl='int', unique='data', updatable=False, comment='资源页面id')
    parent_page_id = dataorm.IntField(ddl='int', comment='资源父页面id')
    atime = dataorm.StrField(ddl='str', comment='资源来源时间')

if __name__ == '__main__':
    pass


