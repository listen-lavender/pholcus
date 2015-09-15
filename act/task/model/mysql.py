from datakit.mysql.orm import *
from datakit.mysql.suit import withMysql, dbpc
from task.config.db.mysql import RDB, WDB, LIMIT, _DBCONN, USE

def initDB():
    dbpc.addDB(RDB, LIMIT, host=_DBCONN[USE]['host'],
                port=_DBCONN[USE]['port'],
                user=_DBCONN[USE]['user'],
                passwd=_DBCONN[USE]['passwd'],
                db=_DBCONN[USE]['db'],
                charset=_DBCONN[USE]['charset'],
                use_unicode=_DBCONN[USE]['use_unicode'],
                override=False)
    dbpc.addDB(WDB, LIMIT, host=_DBCONN[USE]['host'],
                port=_DBCONN[USE]['port'],
                user=_DBCONN[USE]['user'],
                passwd=_DBCONN[USE]['passwd'],
                db=_DBCONN[USE]['db'],
                charset=_DBCONN[USE]['charset'],
                use_unicode=_DBCONN[USE]['use_unicode'],
                override=False)

class Hotel(Model):
    __table__ = 'official_hotel_info'
    hotel_id = Field(ddl='varchar(20)', unique='uq_official')
    hotel_type = Field(ddl='varchar(10)', unique='uq_official')
    hotel_name = Field(ddl='varchar(50)')
    admin_area = Field(ddl='varchar(50)')
    business_area = Field(ddl='varchar(256)')
    star_rate = Field(ddl='tinyint(1)')
    landmark = Field(ddl='varchar(256)')
    address = Field(ddl='varchar(256)')
    lat = Field(ddl='double')
    lnt = Field(ddl='double')
    tel = Field(ddl='varchar(100)')
    manager_tel = Field(ddl='varchar(50)')
    fax = Field(ddl='varchar(50)')
    logo = Field(ddl='varchar(256)')
    traffic = Field(ddl='mediumtext')
    introduce = Field(ddl='mediumtext')
    build_time = Field(ddl='varchar(20)')
    decorate_time = Field(ddl='varchar(20)')
    status = Field(ddl='tinyint(1)')
    status_desc = Field(ddl='varchar(50)')
    wifi = Field(ddl='varchar(10)')
    parking = Field(ddl='varchar(10)')
    dining_room = Field(ddl='varchar(10)')
    meeting_room = Field(ddl='varchar(10)')
    swimming_pool = Field(ddl='varchar(10)')
    gym = Field(ddl='varchar(10)')
    morning_call = Field(ddl='varchar(10)')
    luggage = Field(ddl='varchar(10)')
    laundry = Field(ddl='varchar(10)')
    city = Field(ddl='varchar(20)')
    extra = Field(ddl='mediumtext')
    create_time = Field(ddl='datetime')
    update_time = Field(ddl='timestamp')
    hotel_prefix = Field(ddl='varchar(10)')
    public_wifi = Field(ddl='varchar(10)')