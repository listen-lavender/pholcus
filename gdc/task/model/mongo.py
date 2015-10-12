#!/usr/bin/python
# coding=utf-8

from datakit.mongo.orm import *
from datakit.mongo.suit import withMongo, dbpc
from task.config.db.mysql import RDB, WDB, LIMIT, _DBCONN, USE

def initDb():
    dbpc.addDB(RDB, LIMIT, host=_DBCONN[USE]['host'],
            port=27017,
            db=_DBCONN[USE]['db'])
    dbpc.addDB(WDB, LIMIT, host=_DBCONN[USE]['host'],
            port=27017,
            db=_DBCONN[USE]['db'])

class Hotel(Model):
    __table__ = 'official_hotel_info'
    hotel_id = StrField(ddl='str', unique='uq_official')
    hotel_type = StrField(ddl='str', unique='uq_official')
    hotel_name = StrField(ddl='str')
    admin_area = StrField(ddl='str')
    business_area = StrField(ddl='str')
    star_rate = IntField(ddl='int', nullable=0, default=1)
    landmark = StrField(ddl='str')
    address = StrField(ddl='str')
    lat = FloatField(ddl='float')
    lnt = FloatField(ddl='float')
    tel = StrField(ddl='str')
    manager_tel = StrField(ddl='str')
    fax = StrField(ddl='str')
    logo = StrField(ddl='str')
    traffic = StrField(ddl='str')
    introduce = StrField(ddl='str')
    build_time = StrField(ddl='str')
    decorate_time = StrField(ddl='str')
    status = IntField(ddl='int')
    status_desc = StrField(ddl='str')
    wifi = StrField(ddl='str')
    parking = StrField(ddl='str')
    dining_room = StrField(ddl='str')
    meeting_room = StrField(ddl='str')
    swimming_pool = StrField(ddl='str')
    gym = StrField(ddl='str')
    morning_call = StrField(ddl='str')
    luggage = StrField(ddl='str')
    laundry = StrField(ddl='str')
    city = StrField(ddl='str')
    extra = StrField(ddl='str')
    create_time = StrField(ddl='str')
    update_time = StrField(ddl='str')
    hotel_prefix = StrField(ddl='str')
    public_wifi = StrField(ddl='str')