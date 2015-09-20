create table `grab_config` (
  `id` int(11) not null auto_increment,
  `type` varchar(20) not null comment '配置值类型',
  `name` varchar(50) not null comment '配置名称',
  `key` varchar(50) not null comment '配置键',
  `val` varchar(200) not null comment '配置值',
  `filepath` varchar(100) default null comment '配置文件路径',
  `status` tinyint(1) not null default '1' comment '是否有效，1：有效，0：无效',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `name` (`type`,`name`,`key`)
) engine=innodb auto_increment=6 default charset=utf8 comment='配置文件信息表';

create table `grab_waycon` (
  `id` int(11) not null auto_increment,
  `name` varchar(50) not null comment '联系方式名称',
  `desc` varchar(200) not null comment '联系方式描述',
  `status` tinyint(1) not null default 1 comment '是否有效，1：有效，0：无效',
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
  `status` tinyint(1) not null default 1 comment '是否有效，1：有效，0：无效',
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
  `status` tinyint(1) not null default 1 comment '是否有效，1：有效，0：无效',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `gc` (`gid`, `cid`)
) engine=innodb default charset=utf8 comment='用户分组表';

create table `grab_permit` (
  `id` int(11) not null auto_increment,
  `sid` int(11) not null comment '权限所有者id',
  `stype` char(1) not null comment '权限所有者类型，c：creator，g：group',
  `oid` int(11) not null comment '权限对象id',
  `otype` char(1) not null comment '权限对象类型，u：unit，a：article，s：section',
  `weight` tinyint(1) not null default 1 comment '权重，0-7',
  `desc` char(4) not null default '---q' comment '权重描述，---q，-au-，d---',
  `notify` varchar(300) default '{}' comment '通知条件',
  `status` tinyint(1) not null default 1 comment '是否有效，1：有效，0：无效',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `so` (`sid`, `stype`, `oid`, `otype`)
) engine=innodb default charset=utf8 comment='用户权限表';

create table `grab_unit` (
  `id` int(11) not null auto_increment,
  `dmid` int(11) not null comment '数据模型id',
  `name` varchar(20) not null comment '抓取任务名称',
  `dirpath` varchar(64) not null default '' comment '任务业务分类目录路径',
  `filepath` varchar(64) not null default '' comment '任务业务分类脚本路径',
  `status` tinyint(1) not null default 1 comment '是否有效，1：有效，0：无效',
  `hm` tinyint(1) not null default 1 comment '是否有module，1：有效，0：无效',
  `hc` tinyint(1) not null default 1 comment '是否有class，1：有效，0：无效',
  `hf` tinyint(1) not null default 0 comment '是否有function，1：有效，0：无效',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `unit` (`name`)
) engine=innodb default charset=utf8 comment='抓取任务单元表';

create table `grab_article` (
  `id` int(11) not null auto_increment,
  `uid` int(11) not null comment '抓取任务所属类别id',
  `name` varchar(20) not null comment '抓取任务名称',
  `filepath` varchar(64) not null default '' comment '任务脚本文件路径',
  `status` tinyint(1) not null default 1 comment '是否有效，1：有效，0：无效',
  `hm` tinyint(1) not null default 1 comment '是否有module，1：有效，0：无效',
  `hc` tinyint(1) not null default 1 comment '是否有class，1：有效，0：无效',
  `hf` tinyint(1) not null default 0 comment '是否有function，1：有效，0：无效',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `unit_article` (`uid`,`name`)
) engine=innodb default charset=utf8 comment='抓取任务篇章表';

create table `grab_section` (
  `id` int(11) not null auto_increment,
  `aid` int(11) not null comment '工作流所属抓取篇id',
  `next_id` int(11) default null comment '工作流下一段id',
  `name` varchar(20) not null comment '工作流段名称',
  `initflow` varchar(20) default null comment '工作流初始化标志',
  `index` varchar(20) default null comment '遍历索引',
  `retry` tinyint(1) not null default 0 comment '重试次数',
  `timeout` int(4) not null default '30' comment '任务超时时间',
  `store` int(11) default null comment '工作流存储id',
  `status` tinyint(1) not null default '1' comment '是否有效，1：有效，0：无效',
  `hm` tinyint(1) not null default 0 comment '是否有module，1：有效，0：无效',
  `hc` tinyint(1) not null default 0 comment '是否有class，1：有效，0：无效',
  `hf` tinyint(1) not null default 1 comment '是否有function，1：有效，0：无效',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `article_section` (`refid`,`reftype`,`name`),
  unique key `next_id` (`next_id`)
) engine=innodb default charset=utf8 comment='抓取任务段落表';

create table `grab_datapath` (
  `id` int(11) not null auto_increment,
  `bid` int(11) NOT NULL default 0 COMMENT '业务id，0表示同等业务通用',
  `btype` varchar(30) NOT NULL DEFAULT '' COMMENT '业务类型',
  `sid` int(11) NOT NULL default 0 COMMENT '作用域id，0表示同等作用域通用',
  `stype` varchar(30) NOT NULL DEFAULT '' COMMENT '作用域类型',
  `pid` int(11) not null default '' comment '工作流段数据源id',
  `name` varchar(100) not null comment '工作流段变量名称',
  `index` varchar(100) not null default '' comment '工作流段复杂变量索引',
  `method` varchar(30) default null comment '工作流段变量对应方式',
  `xpath` varchar(500) default null comment '工作流段变量对应路径',
  `default` varchar(100) default null comment '工作流段变量默认值',
  `content` varchar(50) default null comment '工作流段变量内容',
  `datatype` varchar(20) not null comment '工作流段变量类型',
  primary key (`id`),
  unique key `var` (`bid`, `btype`, `sid`, `stype`, `pid`, `name`, `index`)
) engine=innodb default charset=utf8 comment='抓取数据数据路径表';

create table `grab_datasource` (
  `id` int(11) not null auto_increment,
  `name` varchar(100) not null comment '工作流段变量名称',
  `method` int(11) not null comment '工作流段数据源获取方式',
  `url` int(11) not null comment '工作流段数据源地址',
  `data` int(11) default null comment '工作流段数据源获取data',
  `headers` int(11) default null comment '工作流段数据源获取headers',
  `cookies` int(11) default null comment '工作流段数据源获取cookies',
  `timeout` int(11) not null comment '工作流段数据源获取超时设置',
  `format` varchar(30) default null comment '工作流段数据源格式',
  `sid` int(11) not null comment '工作流段id',
  `ssid` int(11) not null comment '会话工作流段id',
  primary key (`id`),
  unique key `src` (`sid`, `name`)
) engine=innodb default charset=utf8 comment='抓取数据数据源表';

create table `grab_datamodel` (
  `id` int(11) not null auto_increment,
  `name` varchar(64) not null default '' comment '数据模型名称',
  `table` varchar(64) not null default '' comment '数据表名称',
  `comment` varchar(200) default null comment '数据模型注释',
  `autocreate` tinyint(1) not null default 1 comment '状态值：1，需要自动创建； 0，不需要自动创建',
  `iscreated` tinyint(1) not null default 1 comment '状态值：1，已创建； 0，未创建',
  `status` tinyint(1) not null default 1 comment '是否有效，1：有效，0：无效',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `model` (`name`)
) engine=innodb default charset=utf8 comment='抓取任务模型表';

create table `grab_dataitem` (
  `id` int(11) not null auto_increment,
  `dmid` int(11) not null comment '数据模型id',
  `name` varchar(64) not null default '' comment '数据项名称',
  `default` longtext default null comment '数据项默认值',
  `comment` varchar(200) default null comment '数据项注释',
  `nullable` tinyint(1) not null default 1 comment '状态值：1，允许null； 0，不允许null',
  `unique` varchar(64) default null comment '状态值：1，是唯一索引数据项； 0，不是唯一索引数据项',
  primary key (`id`),
  unique key `model_time` (`dmid`, `name`)
) engine=innodb default charset=utf8 comment='抓取任务数据项表';

create table `grab_datatype` (
  `id` int(11) not null auto_increment,
  `diid` int(11) not null comment '数据项id',
  `type` varchar(30) not null comment '数据库类型',
  `ddl` varchar(64) not null default '' comment '数据项的具体类型',
  primary key (`id`),
  unique key `item` (`diid`, `type`)
) engine=innodb default charset=utf8 comment='抓取任务数据项类型表';

create table `grab_task` (
  `id` int(11) not null auto_increment,
  `aid` int(11) not null comment '工作篇id',
  `sid` int(11) not null comment '起始工作段id',
  `flow` varchar(20) default null comment '执行工作流',
  `args` varchar(30) default null comment '初始元组参数',
  `kwargs` varchar(30) default null comment '初始字典参数',
  `worknum` int(3) default null comment '工作者数量',
  `queuetype` char(1) default null comment '队列类型，B or P',
  `worktype` varchar(30) default null comment '工作类型，thread or coroutine',
  `trace` tinyint(1) not null default 0 comment '是否跟踪子任务',
  `timeout` int(4) not null default 30 comment '超时时间',
  `category` varchar(50) default '' comment '分类',
  `tag` varchar(500) default '' comment '标签',
  `status` tinyint(1) not null default 1 comment '是否有效，1：有效，0：无效',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `task` (`aid`, `sid`)
) engine=innodb default charset=utf8 comment='抓取任务表';

create table `grab_statistics` (
  `id` int(11) not null auto_increment,
  `tid` int(11) not null comment '统计工作流任务id',
  `sid` int(11) not null comment '统计工作流段id',
  `succ` int(11) not null comment '成功数',
  `fail` int(11) not null comment '失败数',
  `timeout` int(11) not null comment '超时数',
  `status` tinyint(1) not null default 1 comment '是否有效，1：有效，0：无效',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  key `task` (`sid`, `tid`)
) engine=innodb default charset=utf8 comment='抓取任务统计表';