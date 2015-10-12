from datakit.mysql.orm import *
from datakit.mysql.suit import dbpc
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
    __table__ = 'hotelinfo'
    hotel_id = Field(ddl='varchar(20)', unique='uq_official')
    hotel_type = Field(ddl='varchar(10)', unique='uq_official')
    hotel_name = Field(ddl='varchar(50)')

    address = Field(ddl='varchar(256)')
    lat = Field(ddl='varchar(50)')
    lnt = Field(ddl='varchar(50)')

    tel = Field(ddl='varchar(100)')
    logo = Field(ddl='varchar(256)')
    status = Field(ddl='tinyint(1)')

    create_time = Field(ddl='datetime')
    update_time = Field(ddl='timestamp')
    tid = Field(ddl='int(11)')