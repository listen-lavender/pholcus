#!/usr/bin/python
# coding=utf-8

from datakit.mongo.orm import *
from datakit.mongo.suit import dbpc
from task.config.db.mongo import RDB, WDB, LIMIT, _DBCONN, USE


class MarkModel(Model):

    def __init__(self, **attributes):
        self.__mappings__['create_time'] = DatetimeField(ddl='datetime')
        self.__mappings__['update_time'] = DatetimeField(ddl='datetime')
        self.__mappings__['tid'] = IntField(ddl='int')
        attributes['create_time'] = attributes.get('create_time', datetime.datetime.now())
        attributes['update_time'] = attributes.get('update_time', datetime.datetime.now())
        for key in self.__mappings__:
            if not key in attributes:
                raise Exception('Need field %s. ' % key)
            attributes[key] = self.__mappings__[key].check_value(attributes[key])
        super(Model, self).__init__(**attributes)

    def __setstate__(self, state):
        self.__dict__ = state

    def __getstate__(self):
        return self.__dict__


def initDB():
    dbpc.addDB(RDB, LIMIT, host=_DBCONN[USE]['host'],
            port=27017,
            db=_DBCONN[USE]['db'])
    dbpc.addDB(WDB, LIMIT, host=_DBCONN[USE]['host'],
            port=27017,
            db=_DBCONN[USE]['db'])

'''
@comment('视频数据')
'''
class Video(MarkModel):
    __table__ = 'video'
    cat = ListField(ddl='list', comment='资源分类')
    url = StrField(ddl='str', comment='资源地址')
    format = StrField(ddl='str', comment='资源格式')
    size = IntField(ddl='int', comment='资源大小')
    during = IntField(ddl='int', comment='资源时常')
    tag = ListField(ddl='list', comment='资源标签')
    name = StrField(ddl='str', comment='资源名称')
    desc = StrField(ddl='str', comment='资源描述')
    cover = StrField(ddl='str', comment='资源封面')
    # director = StrField(ddl='str')
    # actor = ListField(ddl='list')
    # role = ListField(ddl='list')
    author = StrField(ddl='str', comment='资源作者')
    owner = DictField(ddl='dict', comment='资源拥有者')
    # url_type = StrField(ddl='str')
    snum = IntField(ddl='int', comment='资源序号')
    src = StrField(ddl='str', comment='资源来源')
    host = StrField(ddl='str', comment='资源域名')
    page_url = StrField(ddl='str', comment='资源原页面地址')
    page_id = IntField(ddl='int', unique='uq_video', comment='资源页面id')
    parent_page_id = IntField(ddl='int', comment='资源父页面id')
    atime = StrField(ddl='str', comment='资源来源时间')

'''
@comment('音频数据')
'''
class Audio(MarkModel):
    __table__ = 'audio'
    cat = ListField(ddl='list', comment='资源分类')
    url = StrField(ddl='str', comment='资源地址')
    format = StrField(ddl='str', comment='资源格式')
    size = IntField(ddl='int', comment='资源大小')
    during = IntField(ddl='int', comment='资源时长')
    tag = ListField(ddl='list', comment='资源标签')
    name = StrField(ddl='str', comment='资源名称')
    desc = StrField(ddl='str', comment='资源描述')
    cover = StrField(ddl='str', comment='资源封面')
    singer = StrField(ddl='str', comment='资源歌手')
    # url_type = StrField(ddl='str')
    snum = IntField(ddl='int', comment='资源序号')
    src = StrField(ddl='str', comment='资源来源')
    host = StrField(ddl='str', comment='资源域名')
    page_url = StrField(ddl='str', comment='资源原页面地址')
    page_id = IntField(ddl='int', unique='uq_audio', comment='资源页面id')
    parent_page_id = IntField(ddl='int', comment='资源父页面id')
    atime = DatetimeField(ddl='datetime', comment='资源来源时间')


if __name__ == '__main__':
    pass


