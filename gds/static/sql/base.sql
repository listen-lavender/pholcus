create table `grabtask_config` (
  `id` int(11) not null auto_increment,
  `name` varchar(50) not null comment '配置名称',
  `value` varchar(200) not null comment '配置值',
  `desc` varchar(200) not null comment '配置描述',
  `filepath` varchar(100) not null comment '配置文件路径',
  `effect` tinyint(1) not null default '0' comment '是否生效，1：已生效，0：未生效',
  `status` tinyint(1) not null default '1' comment '是否有效，1：有效，0：无效',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `name` (`name`)
) engine=innodb default charset=utf8 comment='配置文件信息表';

create table `grabtask_waycon` (
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

create table `grabtask_creator` (
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

create table `grabtask_group` (
  `id` int(11) not null auto_increment,
  `cid` int(11) not null comment '用户id',
  `status` tinyint(1) not null default '1' comment '是否有效，1：有效，0：无效',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `gc` (`gid`, `cid`)
) engine=innodb default charset=utf8 comment='用户分组表';

create table `grabtask_permit` (
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
  unique key `so` (`sid`, `stype`, `oid`, `otype`)
) engine=innodb default charset=utf8 comment='用户权限表';

create table `grabtask_unit` (
  `id` int(11) not null auto_increment,
  `dmid` int(11) not null comment '数据模型id',
  `unit_name` varchar(20) not null comment '抓取任务名称',
  `public` varchar(1000) default null comment '公共通用资源',
  `status` tinyint(1) not null default '1' comment '是否有效，1：有效，0：无效',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `unit` (`unit_name`)
) engine=innodb default charset=utf8 comment='抓取任务单元表';

create table `grabtask_article` (
  `id` int(11) not null auto_increment,
  `uid` int(11) not null comment '抓取任务所属类别id',
  `article_name` varchar(20) not null comment '抓取任务名称',
  `prepare` varchar(1000) default null comment '准备资源',
  `worknum` int(3) default null comment '工作者数量',
  `queuetype` char(1) default null comment '队列类型，B or P',
  `worktype` varchar(30) default null comment '工作类型，thread or coroutine',
  `timeout` int(4) not null default 30 comment '超时时间',
  `status` tinyint(1) not null default '1' comment '是否有效，1：有效，0：无效',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `unit_article` (`uid`,`article_name`)
) engine=innodb default charset=utf8 comment='抓取任务篇章表';

create table `grabtask_section` (
  `id` int(11) not null auto_increment,
  `aid` int(11) not null comment '工作流所属抓取任务id',
  `next_id` int(11) default null comment '工作流下一段id',
  `section_name` varchar(20) not null comment '工作流段名称',
  `initflow` varchar(20) default null comment '工作流初始化标志',
  `index` varchar(20) default null comment '遍历索引',
  `timelimit` int(4) not null default 30 comment '任务超时时间',
  `store` varchar(50) not null comment '存储',
  `url` varchar(200) default null comment '资源定位',
  `additions` varchar(500) default null comment '条件',
  `timeout` int(4) not null default 30 comment '通信超时',
  `implementor` varchar(1000) default null comment '补充抓取',
  `returntuple` varchar(1000) default null comment '返回序列',
  `returndict` varchar(1000) default null comment '返回字典',
  `effect` tinyint(1) not null default '0' comment '是否生效，1：已生效，0：未生效',
  `status` tinyint(1) not null default '1' comment '是否有效，1：有效，0：无效',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`),
  unique key `article_section` (`aid`,`section_name`),
  unique key `next_id` (`next_id`)
) engine=innodb default charset=utf8 comment='抓取任务段落表';

create table `grabtask_datamodel` (
  `id` int(11) not null auto_increment,
  `name` varchar(64) not null default '' comment '数据模型名称',
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
) engine=innodb default charset=utf8 comment='抓取任务模型表';

create table `grabtask_dataitem` (
  `id` int(11) not null auto_increment,
  `dmid` int(11) not null comment '数据模型id',
  `name` varchar(64) not null default '' comment '数据项名称',
  `default` longtext default null comment '数据项默认值',
  `comment` varchar(200) default null comment '数据项注释',
  `nullable` tinyint(1) not null default '1' comment '状态值：1，允许null； 0，不允许null',
  `unique` varchar(64) default null comment '状态值：1，是唯一索引数据项； 0，不是唯一索引数据项',
  primary key (`id`),
  unique key `model_time` (`dmid`, `name`)
) engine=innodb default charset=utf8 comment='抓取任务数据项表';

create table `grabtask_datatype` (
  `id` int(11) not null auto_increment,
  `diid` int(11) not null comment '数据项id',
  `ditype` varchar(10) not null comment '数据项的数据库',
  `ddl` varchar(64) not null default '' comment '数据项的具体类型',
  primary key (`id`),
  unique key `item` (`diid`)
) engine=innodb default charset=utf8 comment='抓取任务数据项类型表';

create table `grabtask_statistics` (
  `id` int(11) not null auto_increment,
  `sid` int(11) not null comment '统计工作流段id',
  `succ` int(11) not null comment '成功数',
  `fail` int(11) not null comment '失败数',
  `timeout` int(11) not null comment '超时数',
  `status` tinyint(1) not null default '1' comment '是否有效，1：有效，0：无效',
  `extra` varchar(300) default null comment '附加内容',
  `creator` int(11) not null comment '创建者id',
  `updator` int(11) not null comment '更新者id',
  `create_time` datetime not null comment '创建时间',
  `update_time` timestamp not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (`id`)
) engine=innodb default charset=utf8 comment='抓取任务统计表';