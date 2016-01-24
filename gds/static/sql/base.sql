create table `grab_config` (
  `id` int(11) not null auto_increment,
  `type` varchar(20) not null comment '配置值类型',
  `name` varchar(50) not null comment '配置名称',
  `key` varchar(50) not null comment '配置键',
  `val` varchar(200) not null comment '配置值',
  `filepath` varchar(100) default '' comment '配置文件路径',
  `status` tinyint(1) not null default '1' comment '是否有效，1：有效，0：无效',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `name` (`type`,`name`,`key`)
) engine=innodb auto_increment=0 default charset=utf8 comment='配置文件信息表';

create table `grab_waycon` (
  `id` int(11) not null auto_increment,
  `name` varchar(50) not null comment '联系方式名称',
  `desc` varchar(200) not null comment '联系方式描述',
  `status` tinyint(1) not null default '1' comment '是否有效，1：有效，0：无效',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `name` (`name`)
) engine=innodb default charset=utf8 comment='联系方式表';

create table `grab_creator` (
  `id` int(11) not null auto_increment,
  `username` varchar(20) not null comment '用户名',
  `password` varchar(20) not null comment '密码',
  `contact` varchar(500) default '{}' comment '联系方式',
  `notify` varchar(100) default '{}' comment '通知条件',
  `status` tinyint(1) not null default '1' comment '是否有效，1：有效，0：无效',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `user` (`username`)
) engine=innodb default charset=utf8 comment='用户表';

create table `grab_group` (
  `id` int(11) not null auto_increment,
  `gid` int(11) not null comment '用户组id',
  `cid` int(11) not null comment '用户id',
  `status` tinyint(1) not null default '1' comment '是否有效，1：有效，0：无效',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `gc` (`gid`,`cid`)
) engine=innodb default charset=utf8 comment='用户分组表';

create table `grab_permit` (
  `id` int(11) not null auto_increment,
  `sid` int(11) not null comment '权限所有者id',
  `stype` char(1) not null comment '权限所有者类型，c：creator，g：group',
  `oid` int(11) not null comment '权限对象id',
  `otype` char(1) not null comment '权限对象类型，u：unit，a：article，s：section',
  `weight` tinyint(1) not null default '1' comment '权重，0-7',
  `desc` char(4) not null default '---q' comment '权重描述，---q，-au-，d---',
  `notify` varchar(300) default '{}' comment '通知条件',
  `status` tinyint(1) not null default '1' comment '是否有效，1：有效，0：无效',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `so` (`sid`,`stype`,`oid`,`otype`)
) engine=innodb default charset=utf8 comment='用户权限表';

create table `grab_unit` (
  `id` int(11) not null auto_increment,
  `dmid` int(11) not null comment '数据模型id',
  `name` varchar(20) not null comment '抓取任务名称',
  `dirpath` varchar(64) not null default '' comment '任务业务分类目录路径',
  `filepath` varchar(64) not null default '' comment '任务业务分类脚本路径',
  `status` tinyint(1) not null default '1' comment '是否有效，1：有效，0：无效',
  `distribute` char(2) not null default 'sc' comment '分布方式，sc共享代码配置；sf，共享文件配置；sn，不共享',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `unit` (`name`)
) engine=innodb auto_increment=16 default charset=utf8 comment='抓取任务单元表';

create table `grab_article` (
  `id` int(11) not null auto_increment,
  `uid` int(11) not null comment '抓取任务所属类别id',
  `name` varchar(20) not null comment '抓取任务名称',
  `pinyin` varchar(50) not null default '' comment '中文拼音，例如如家(rujia)',
  `host` varchar(50) not null default '' comment '抓取网站域名',
  `filepath` varchar(64) not null default '' comment '任务脚本文件路径',
  `status` tinyint(1) not null default '1' comment '是否有效，1：有效，0：无效',
  `distribute` char(2) not null default 'sc' comment '分布方式，sc共享代码配置；sf，共享文件配置；sn，不共享',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null default '0' comment '创建者id',
  `updator` int(11) not null default '0' comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `unit_article` (`uid`,`name`)
) engine=innodb auto_increment=41 default charset=utf8 comment='抓取任务篇章表';

create table `grab_section` (
  `id` int(11) not null auto_increment,
  `aid` int(11) not null comment '工作流所属抓取任务id',
  `next_id` int(11) default null comment '工作流下一段id',
  `name` varchar(20) not null comment '工作流段名称',
  `flow` varchar(20) default null comment '工作流初始化标志',
  `index` varchar(20) default null comment '遍历索引',
  `retry` tinyint(1) not null default '0' comment '重试次数',
  `timelimit` int(4) not null default '30' comment '任务超时时间',
  `store` tinyint(1) not null default '0' comment '工作流存储id',
  `status` tinyint(1) not null default '1' comment '是否有效，1：有效，0：无效',
  `distribute` char(2) not null default 'sc' comment '分布方式，sc共享代码配置；sf，共享文件配置；sn，不共享',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `article_section` (`aid`,`name`,`flow`),
  unique key `next_id` (`next_id`)
) engine=innodb auto_increment=10 default charset=utf8 comment='抓取任务段落表';

create table `grab_datapath` (
  `id` int(11) not null auto_increment,
  `bid` int(11) not null default '0' comment '业务id，0表示同等业务通用',
  `btype` varchar(30) not null default '' comment '业务类型',
  `sid` int(11) not null default '0' comment '作用域id，0表示同等作用域公用',
  `stype` varchar(30) not null default '' comment '作用域类型',
  `pid` varchar(50) not null default '' comment '工作流段数据源id',
  `name` varchar(100) not null comment '工作流段变量名称',
  `index` varchar(100) not null default '' comment '工作流段复杂变量索引',
  `method` varchar(30) default null comment '工作流段变量对应方式',
  `xpath` varchar(500) default null comment '工作流段变量对应路径',
  `default` varchar(100) default null comment '工作流段变量默认值',
  `content` varchar(50) default null comment '工作流段变量内容',
  `datatype` varchar(20) default null comment '工作流段变量类型',
  primary key (`id`),
  unique key `dbsp` (`bid`,`btype`,`sid`,`stype`,`pid`,`name`,`index`,`method`)
) engine=innodb auto_increment=1296 default charset=utf8 comment='抓取数据路径表';

create table `grab_datasource` (
  `id` int(11) not null auto_increment,
  `name` varchar(100) not null comment '工作流段变量名称',
  `method` varchar(30) default '' comment '工作流段数据源获取方式',
  `url` varchar(100) default '' comment '工作流段数据源地址',
  `data` varchar(100) default null comment '工作流段数据源获取data',
  `headers` varchar(100) default null comment '工作流段数据源获取headers',
  `cookies` varchar(100) default null comment '工作流段数据源获取cookies',
  `timeout` int(11) default '30' comment '工作流段数据源获取超时设置',
  `format` varchar(30) default '' comment '工作流段数据源格式',
  `sid` int(11) not null comment '工作流段id',
  `ssid` int(11) not null comment '会话工作流段id',
  primary key (`id`),
  unique key `src` (`sid`,`name`)
) engine=innodb auto_increment=5 default charset=utf8 comment='抓取数据数据源表';

create table `grab_datamodel` (
  `id` int(11) not null auto_increment,
  `name` varchar(64) not null default '' comment '数据模型名称',
  `table` varchar(64) default null comment '数据表名称',
  `comment` varchar(200) default null comment '数据模型注释',
  `autocreate` tinyint(1) not null default '1' comment '状态值：1，需要自动创建； 0，不需要自动创建',
  `iscreated` tinyint(1) not null default '1' comment '状态值：1，已创建； 0，未创建',
  `status` tinyint(1) not null default '1' comment '是否有效，1：有效，0：无效',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `model` (`name`)
) engine=innodb auto_increment=13 default charset=utf8 comment='抓取任务模型表';

create table `grab_dataitem` (
  `id` int(11) not null auto_increment,
  `dmid` int(11) not null comment '数据模型id',
  `name` varchar(64) not null default '' comment '数据项名称',
  `length` int(11) default null comment '数据项长度',
  `default` varchar(100) default null comment '数据项默认值',
  `comment` varchar(200) default null comment '数据项注释',
  `unique` varchar(64) default null comment '状态值：1，是唯一索引数据项； 0，不是唯一索引数据项',
  primary key (`id`),
  unique key `model_time` (`dmid`,`name`)
) engine=innodb auto_increment=10 default charset=utf8 comment='抓取任务数据项表';

create table `grab_task` (
  `id` int(11) not null auto_increment,
  `type` varchar(8) default 'once' comment '任务类型，forever周期，once一次',
  `period` int(4) not null default '12' comment 'forever任务周期，单位小时，默认12小时',
  `aid` int(11) not null comment '工作篇id',
  `sid` int(11) not null comment '起始工作段id',
  `name` varchar(50) not null default '' comment '任务名称',
  `flow` varchar(20) default null comment '执行工作流',
  `params` varchar(3000) default null comment '参数，json格式',
  `worknum` int(3) not null default '6' comment '工作者数量',
  `queuetype` char(1) not null default 'p' comment '队列类型，b or p',
  `worktype` varchar(30) not null default 'thread' comment '工作类型，thread or coroutine',
  `trace` tinyint(1) not null default '0' comment '是否跟踪子任务',
  `timeout` int(4) not null default '30' comment '超时时间',
  `category` varchar(50) default '' comment '分类',
  `tag` varchar(500) default '' comment '标签',
  `status` tinyint(1) not null default '1' comment '是否有效，1：start，0：stop，2：running，3：error',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `task` (`aid`,`sid`)
) engine=innodb auto_increment=4 default charset=utf8 comment='抓取任务表';

create table `grab_statistics` (
  `id` int(11) not null auto_increment,
  `tid` int(11) not null comment '统计工作流任务id',
  `succ` int(11) not null comment '成功数',
  `fail` int(11) not null comment '失败数',
  `timeout` int(11) not null comment '超时数',
  `elapse` float not null comment '耗时',
  `create_time` datetime not null comment '创建时间',
  primary key (`id`)
) engine=innodb auto_increment=629 default charset=utf8 comment='抓取任务统计表';

create table `grab_proxy` (
  `id` int(11) not null auto_increment,
  `ip` varchar(20) not null comment '代理地址',
  `port` int(10) not null comment '代理端口',
  `location` varchar(30) default null comment '代理地理位置',
  `safetype` varchar(30) not null comment '代理类型',
  `protocol` varchar(30) not null comment '通信协议类型',
  `refspeed` float default '0' comment '参考速度',
  `usespeed` float default '0' comment '使用速度',
  `usenum` int(10) default '0' comment '使用次数',
  `status` tinyint(1) not null default '1' comment '是否有效，1：有效，0：无效',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `proxy` (`ip`,`port`)
) engine=innodb default charset=utf8 comment='代理表';

create table `grab_proxy_log` (
  `id` int(11) not null auto_increment,
  `pid` int(11) not null comment '代理id',
  `elapse` float default '0' comment '消耗时间',
  `create_time` datetime not null comment '创建时间',
  primary key (`id`)
) engine=innodb default charset=utf8 comment='代理使用日志表';

create table `grab_log` (
  `id` int(11) not null auto_increment,
  `gsid` int(11) not null comment '统计工作流任务id',
  `sname` varchar(20) not null comment '工作流段名称',
  `succ` int(11) not null comment '成功数',
  `fail` int(11) not null comment '失败数',
  `timeout` int(11) not null comment '超时数',
  `create_time` datetime not null comment '创建时间',
  primary key (`id`)
) engine=innodb auto_increment=2550 default charset=utf8 comment='抓取任务日志表';

insert into `grab_config` (`id`, `type`, `name`, `key`, `val`, `filepath`, `status`, `extra`, `creator`, `updator`, `create_time`, `update_time`)
values
  (1, 'db', 'mongo', 'jxqctm', '{\"host\":\"210.14.154.142\",\"port\":27017,\"db\":\"dandan-jiang\",\"charset\":\"utf8\",\"use_unicode\":false}', 'db.py', 1, null, 0, 0, '2015-08-27 22:39:16', '2015-12-16 17:24:41'),
  (2, 'db', 'mysql', 'localhost', '{\"host\":\"127.0.0.1\",\"port\":3306,\"user\":\"root\",\"passwd\":\"\",\"db\":\"kuaijie\",\"charset\":\"utf8\",\"use_unicode\":false}', 'db.py', 1, null, 0, 0, '2015-08-29 09:21:59', '2015-08-29 12:00:28'),
  (3, 'db', 'mongo', 'localhost', '{\"host\":\"127.0.0.1\",\"port\":27017,\"db\":\"adesk_video\",\"charset\":\"utf8\",\"use_unicode\":false}', 'db.py', 1, null, 0, 0, '2015-08-29 09:21:59', '2015-08-29 12:00:33'),
  (4, 'db', 'mysql', 'use', '{\"rdb\":\"localhost\",\"wdb\":\"localhost\",\"limit\":20}', 'db.py', 1, null, 0, 0, '2015-08-29 09:21:59', '2015-08-29 16:45:40'),
  (5, 'db', 'mongo', 'use', '{\"rdb\":\"localhost\",\"wdb\":\"localhost\",\"limit\":20}', 'db.py', 1, null, 0, 0, '2015-08-29 09:21:59', '2015-08-29 16:45:46'),
  (6, 'root', '', 'dir', 'task/', null, 1, null, 0, 0, '2015-08-26 23:42:58', '2015-09-03 16:20:25'),
  (7, 'model', '', 'dir', 'model/', null, 1, null, 0, 0, '2015-08-26 23:42:58', '2015-09-03 16:20:29'),
  (8, 'config', '', 'dir', 'config/', null, 1, null, 0, 0, '2015-08-26 23:42:58', '2015-09-03 16:20:39');