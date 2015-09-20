#!/usr/bin/python
# coding=utf-8

TIMEOUT = 30

import hashlib
import random

"""
     各渠道数据源抓取常量
"""
SPIDERS = {'rujia':{'mod':'spiderRujia', 'cls':'SpiderHomeinns'},
}

EXCEPTOR = {
}

INSERTSQLS = {'fetchhotel':""" insert into official_hotel_info(`hotel_id`,`hotel_type`,`hotel_name`,`admin_area`,`business_area`,`star_rate`,`landmark`,`address`,`lat`,`lnt`,`tel`,`manager_tel`,`fax`,`logo`,`traffic`,`introduce`,`build_time`,`decorate_time`,`status`,`status_desc`,`wifi`, `public_wifi`, `parking`,`dining_room`,`meeting_room`,`swimming_pool`,`gym`,`morning_call`,`luggage`,`laundry`,`city`,`extra`,`hotel_prefix`,`create_time`)
                                                        values(%s        ,          %s,          %s,          %s,             %s,         %s,        %s,       %s,   %s,   %s,   %s,           %s,   %s,    %s,       %s,         %s,          %s,             %s,      %s,           %s,    %s,            %s,        %s,           %s,            %s,             %s,   %s,            %s,       %s,       %s,    %s,     %s,            %s,           %s)
                                    on duplicate key
                                update `hotel_name`=values(`hotel_name`),`admin_area`=values(`admin_area`),`business_area`=values(`business_area`),`star_rate`=values(`star_rate`),`landmark`=values(`landmark`),`address`=values(`address`),`lat`=values(`lat`),`lnt`=values(`lnt`),`tel`=values(`tel`),`manager_tel`=values(`manager_tel`),`fax`=values(`fax`),`logo`=values(`logo`),`traffic`=values(`traffic`),`introduce`=values(`introduce`),`build_time`=values(`build_time`),`decorate_time`=values(`decorate_time`),`status`=values(`status`),`status_desc`=values(`status_desc`),`wifi`=values(`wifi`), `public_wifi`=values(`public_wifi`), `parking`=values(`parking`),`dining_room`=values(`dining_room`),`meeting_room`=values(`meeting_room`),`swimming_pool`=values(`swimming_pool`),`gym`=values(`gym`),`morning_call`=values(`morning_call`),`luggage`=values(`luggage`),`laundry`=values(`laundry`),`city`=values(`city`),`extra`=values(`extra`),`hotel_prefix`=values(`hotel_prefix`);
          """,  
}

CLSCON = {
    # 'useenv':'testurls',
    'useenv':'onlineurls',
    'SpiderHomeinns':{'predicttotal':1891,
                    'usesrc':'MainWWW',
                    'srctype':'001',
                    'prefix':'如家',
                    'srctable':'official_hotel_info',
                    },
    'SpiderHtinns':{'predicttotal':1891,
                    'usesrc':'MainWWW',
                    'srctype':'002',
                    'prefix':'汉庭',
                    'srctable':'official_hotel_info',
                    },
    'SpiderJjinns':{'predicttotal':1891,
                    'usesrc':'MainWWW',
                    'srctype':'003',
                    'prefix':'锦江',
                    'srctable':'official_hotel_info',
                    },
    'Spider7day':{'predicttotal':1752,
                    'usesrc':'MainWWW',
                    'srctype':'020',
                    'prefix':'7天',
                    'srctable':'official_hotel_info',
                    },
    'Spider998':{'predicttotal':804,
                    'usesrc':'MainWWW',
                    'srctype':'008',
                    'prefix':'格林豪泰',
                    'srctable':'official_hotel_info',
                    },
    'SpiderPodinns':{'predicttotal':332,
                    'usesrc':'MainWWW',
                    'srctype':'010',
                    'prefix':'布丁',
                    'srctable':'official_hotel_info',
                    },
    'SpiderWyn88':{'predicttotal':137,
                    'usesrc':'MainWAP',
                    'srctype':'025',
                    'prefix':'维也纳',
                    'srctable':'official_hotel_info',
                    },
    'SpiderSuper8':{'predicttotal':600,
                    'usesrc':'MainDSR',
                    'srctype':'005',
                    'prefix':'速8',
                    'srctable':'official_hotel_info',
                    },
}

"""
     服务信息对照表
"""
SERVICES = {
    'status_desc':{'1':'营业中', '0':'已关闭', '2':'筹备中', '3':'暂时下线'},
    'public_wifi':{'Y':'大堂wifi服务', 'N':''},
    'wifi':{'F':'全楼覆盖wifi', 'C':'全楼覆盖wifi', 'N':''},
    'parking':{'F':'免费停车场', 'C':'收费停车场', 'N':''},
    'dining_room':{'F':'西餐厅', 'C':'中餐厅', 'D':'餐厅', 'N':''},
    'meeting_room':{'Y':'会议室', 'N':''},
    'swimming_pool':{'O':'游泳池', 'I':'室内游泳池', 'N':''},
    'gym':{'Y':'健身房', 'N':''},
    'morning_call':{'Y':'叫醒服务', 'N':''},
    'luggage':{'Y':'行李寄存', 'N':''},
    'laundry':{'Y':'洗衣服务', 'N':''},
}

"""
    来源品牌对照表
"""
HCT = {"如家":"001",
    "和颐":"001",
    "云上四季":"001",
    "汉庭":"002",
    "漫心":"002",
    "禧玥":"002",
    "海友":"027",
    "全季":"028",
    "星程":"029",
    "锦江之星":"003",
    "锦江都城":"003",
    "金广快捷":"021",
    "百时快捷":"013",
    "7天优品":"020",
    "7天阳光":"020",
    "稻家酒店":"020",
    "喆啡":"020",
    "麗枫":"020",
    "ZMAX潮漫":"020",
    "铂涛菲诺":"020",
    # "7天":"020",
    "速8":"005",
    "桔子":"006",
    "宜必思":"007",
    "格林豪泰":"008",
    "格林联盟":"008",
    "青皮树":"008",
    "格林东方":"008",
    "莫泰":"015",
    "布丁":"010",
    "Zhotels智尚":"010",
    "99旅馆":"011",
    "城市之家":"014",
    "古井君莱":"014",
    "禧龙快捷":"054",
    "南苑E家":"055",
    "清沐酒店":"057",
    "驿家365":"058",
    "城市客栈":"061",
    "今天连锁":"062",
    "欣燕都":"063",
    "山水时尚":"064",
    "富驿时尚":"068",
    "云端快捷":"900",
    "城市便捷":"016",
    "精通酒店":"017",
    "易佰":"018",
    "锐思特":"019",
    "A家连锁":"069",
    "爱尊客":"070",
    "八方快捷":"071",
    "春天时尚":"073",
    "方圆快捷":"074",
    "肯定":"075",
    "浦江之星":"076",
    "艳阳天":"077",
    "中州快捷":"079",
    "银座佳驿":"023",
    "吉泰":"024",
    "维也纳":"025",
    "都市118":"026",
    "格子微":"300",
    "e家连锁":"300",
    "其他品牌":"300",
    "尚客优":"032",
}
