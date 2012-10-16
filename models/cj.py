from sqlalchemy import Column, Integer, String, Numeric, Boolean, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

advertiser_link_types = Table('cj_advertiser_link_types', Base.metadata,
                                Column('advertiser_id', Integer, ForeignKey('cj_advertisers.id')),
                                Column('link_type_id', Integer, ForeignKey('cj_link_types.id')))

class CJLinkType(Base):
    __tablename__ = 'cj_link_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

class CJAdvertiser(Base):
    __tablename__ = 'cj_advertisers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    advertiser_id = Column(String)
    account_active = Column(Boolean)
    seven_day_epc = Column(Numeric)
    three_month_epc = Column(Numeric)
    language = Column(String)
    advertiser_name = Column(String)
    program_url = Column(String)
    account_joined = Column(Boolean)
    mobile_supported = Column(Boolean)
    mobile_tracking_certified = Column(Boolean)
    network_rank = Column(Integer)
    performance_incentives = Column(Boolean)

    link_types = relationship('CJLinkType', secondary=advertiser_link_types)
    #HERE be actions and categories

    def __repr__(self):
        return self.advertiser_name

