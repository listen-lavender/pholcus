#!/usr/bin/python
# coding=utf-8

TIMEOUT = 30

INSERTSQLS = {'fetchhotel':""" insert into official_hotel_info(`hotel_id`,`hotel_type`,`hotel_name`,`admin_area`,`business_area`,`star_rate`,`landmark`,`address`,`lat`,`lnt`,`tel`,`manager_tel`,`fax`,`logo`,`traffic`,`introduce`,`build_time`,`decorate_time`,`status`,`status_desc`,`wifi`, `public_wifi`, `parking`,`dining_room`,`meeting_room`,`swimming_pool`,`gym`,`morning_call`,`luggage`,`laundry`,`city`,`extra`,`hotel_prefix`,`create_time`)
                                                        values(%s        ,          %s,          %s,          %s,             %s,         %s,        %s,       %s,   %s,   %s,   %s,           %s,   %s,    %s,       %s,         %s,          %s,             %s,      %s,           %s,    %s,            %s,        %s,           %s,            %s,             %s,   %s,            %s,       %s,       %s,    %s,     %s,            %s,           %s)
                                    on duplicate key
                                update `hotel_name`=values(`hotel_name`),`admin_area`=values(`admin_area`),`business_area`=values(`business_area`),`star_rate`=values(`star_rate`),`landmark`=values(`landmark`),`address`=values(`address`),`lat`=values(`lat`),`lnt`=values(`lnt`),`tel`=values(`tel`),`manager_tel`=values(`manager_tel`),`fax`=values(`fax`),`logo`=values(`logo`),`traffic`=values(`traffic`),`introduce`=values(`introduce`),`build_time`=values(`build_time`),`decorate_time`=values(`decorate_time`),`status`=values(`status`),`status_desc`=values(`status_desc`),`wifi`=values(`wifi`), `public_wifi`=values(`public_wifi`), `parking`=values(`parking`),`dining_room`=values(`dining_room`),`meeting_room`=values(`meeting_room`),`swimming_pool`=values(`swimming_pool`),`gym`=values(`gym`),`morning_call`=values(`morning_call`),`luggage`=values(`luggage`),`laundry`=values(`laundry`),`city`=values(`city`),`extra`=values(`extra`),`hotel_prefix`=values(`hotel_prefix`);
          """,  
}
