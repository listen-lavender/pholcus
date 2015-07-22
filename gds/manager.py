#!/usr/bin/python
# coding=utf8

from flask.ext.script import Manager, Server
from views import app
from settings import useport
from werkzeug.contrib.fixers import ProxyFix
from datakit.mysql.suit import dbpc, withMysql, DBPoolCollector

@withMysql('wdb')
def buildbase():
    sql = """
create table if not exists `grabtask_admin` (
  `id` int(11) not null auto_increment,
  `username` varchar(20) not null comment '用户名',
  `password` varchar(20) not null comment '密码',
  `read` tinyint(1) not null default '1' comment '是否有效，1：可读，0：不可读',
  `write` tinyint(1) not null default '0' comment '是否有效，1：可写，0：不可写',
  `status` tinyint(1) not null default '1' comment '是否有效，1：有效，0：无效',
  `extra` varchar(30) default null comment '附加内容',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `user` (`username`)
) engine=innodb default charset=utf8;
    """
    dbpc.handler.operate(sql, None)
    sql = """
create table if not exists `grabtask_article` (
  `id` int(11) not null auto_increment,
  `uid` int(11) not null comment '抓取任务所属类别id',
  `article_name` varchar(20) not null comment '抓取任务名称',
  `prepare` varchar(1000) default null comment '准备资源',
  `status` tinyint(1) not null default '1' comment '是否有效，1：有效，0：无效',
  `extra` varchar(30) default null comment '附加内容',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `unit_article` (`uid`,`article_name`)
) engine=innodb default charset=utf8;
    """
    dbpc.handler.operate(sql, None)
    sql = """
create table if not exists `grabtask_datamodel` (
  `id` int(11) not null auto_increment,
  `table_name` varchar(64) not null default '' comment '表名称',
  `table_comment` varchar(200) not null default '' comment '表注释',
  `character_set` varchar(32) default null comment '表字符集',
  `column_name` varchar(64) not null default '' comment '字段名称',
  `column_type` varchar(64) not null default '' comment '字段类型',
  `column_length` int(10) default null comment '字段长度',
  `column_default` longtext comment '字段默认值',
  `column_comment` varchar(200) not null default '' comment '字段注释',
  `is_nullable` tinyint(1) not null default '1' comment '状态值：1，允许null； 0，不允许null',
  `is_autoincrement` tinyint(1) not null default '1' comment '状态值：1，是自增长； 0，不是自增长',
  `is_primary` tinyint(1) not null default '1' comment '状态值：1，是主键； 0，不是主键',
  `is_unique` tinyint(1) not null default '1' comment '状态值：1，是唯一索引字段； 0，不是唯一索引字段',
  `is_key` tinyint(1) not null default '1' comment '状态值：1，是索引字段； 0，不是索引字段',
  `auto_create` tinyint(1) not null default '1' comment '状态值：1，需要自动创建； 0，不需要自动创建',
  `is_created` tinyint(1) not null default '1' comment '状态值：1，已创建； 0，未创建',
  `status` tinyint(1) not null default '1' comment '是否有效，1：有效，0：无效',
  `extra` varchar(30) default null comment '附加内容',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `table_column` (`table_name`,`column_name`)
) engine=innodb default charset=utf8;
    """
    dbpc.handler.operate(sql, None)
    sql = """
create table if not exists `grabtask_section` (
  `id` int(11) not null auto_increment,
  `aid` int(11) not null comment '工作流所属抓取任务id',
  `next_id` int(11) default null comment '工作流下一段id',
  `section_name` varchar(20) not null comment '工作流段名称',
  `initflow` varchar(20) default null comment '工作流初始化标志',
  `index` varchar(20) default null comment '遍历索引',
  `timelimit` int(6) not null default '6' comment '资源定位',
  `url` varchar(200) default null comment '资源定位',
  `additions` varchar(500) default null comment '条件',
  `timeout` int(6) not null default '6' comment '通信超时',
  `implementor` varchar(1000) default null comment '补充抓取',
  `returntuple` varchar(1000) default null comment '返回序列',
  `returndict` varchar(1000) default null comment '返回字典',
  `status` tinyint(1) not null default '1' comment '是否有效，1：有效，0：无效',
  `extra` varchar(30) default null comment '附加内容',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `article_section` (`aid`,`section_name`),
  unique key `next_id` (`next_id`)
) engine=innodb default charset=utf8;
    """
    dbpc.handler.operate(sql, None)
    sql = """
create table if not exists `grabtask_unit` (
  `id` int(11) not null auto_increment,
  `dmid` int(11) not null comment '数据模型id',
  `unit_name` varchar(20) not null comment '抓取任务名称',
  `public` varchar(1000) default null comment '公共通用资源',
  `status` tinyint(1) not null default '1' comment '是否有效，1：有效，0：无效',
  `extra` varchar(30) default null comment '附加内容',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `unit` (`unit_name`)
) engine=innodb default charset=utf8;
    """
    dbpc.handler.operate(sql, None)

app.wsgi_app = ProxyFix(app.wsgi_app)

manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0',
    port = useport)
)

@manager.command
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)
    
    for line in sorted(output):
        print line

if __name__ == "__main__":
    manager.run()

