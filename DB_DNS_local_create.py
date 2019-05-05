from sqlalchemy import  Column, Integer,String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///DB_DNS_Server')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()



class DNS(Base):
    __tablename__ = 'DNS'
    dns_id = Column(Integer(), primary_key=True)
    NAME = Column(String(63))
    TYPE = Column(String(16))
    CLASS = Column(String(16))
    TTL = Column(String(32))
    RDLENGTH = Column(String(16))
    ANCOUNT = Column(String(16))
    RDATA = Column(String(255))
    Time = Column(String(255))
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

def __ini__(self, dns_id,NAME,TYPE,CLASS,TTL,RDLENGTH,ANCOUNT,RDATA,Time,created_on,updated_on):
        self.dns_id = dns_id
        self.NAME = NAME
        self.TYPE = TYPE
        self.CLASS = CLASS
        self.TTL = TTL
        self.RDLENGTH = RDLENGTH
        self.ANCOUNT=ANCOUNT
        self.RDATA = RDATA
        self.Time = Time
        self.created_on = created_on
        self.updated_on = updated_on


def __repr__(self):
    return "DNS(NAME='{self.NAME}', " \
"TYPE='{self.TYPE}', " \
"CLASS='{self.CLASS}', " \
"TTL='{self.TTL}', " \
"RDLENGTH='{self.RDLENGTH}', " \
"RDATA='{self.RDATA}', " \
"ANCOUNT='{self.ANCOUNT}',"\
"Time='{self.Time}', " \
"created_on='{self.created_on}', " \
"updated_on='{self.updated_on}')".format(self=self)

Base.metadata.create_all(engine)

