from sqlalchemy import create_engine, Column, Integer, String,Boolean, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Events(Base):
    __tablename__ = 'events'
    
    event_id = Column(Integer, primary_key=True)
    url = Column(String(100), nullable=False)
    title = Column(String(100), nullable=False)
    title_event = Column(String(100))
    lead_text = Column(String(1000))
    description = Column(String(1000))
    address_name = Column(String(100))
    locations = Column(String(1000))
    address_street = Column(String(100))
    address_zipcode = Column(String(10))
    address_city = Column(String(50))
    address_text = Column(String(100))
    lat_lon = Column(String(20))
    date_start = Column(DateTime, default=datetime.now)
    date_end = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    has_card = Column(Boolean,default=False)
    access_link = Column(String(100))
    access_link_text = Column(String(100))
    address_url = Column(String(100))
    address_url_text = Column(String(100))
    address_name = Column(String(100))
    qfap_tags = Column(String(50))
    flag_interest = Column(Boolean)




    def __repr__(self):
        return f"<Events(event_id='{self.event_id}', title={self.title})>"


"""
event_id             int64
url                 object
title               object
lead_text           object
description         object
date_start          object
date_end            object
locations           object
address_name        object
address_street      object
address_zipcode     object
address_city        object
lat_lon             object
access_link         object
access_link_text    object
updated_at          object
address_url         object
address_url_text    object
address_text        object
title_event         object
qfap_tags           object
"""