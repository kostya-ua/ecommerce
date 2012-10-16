from sqlalchemy import Column, Integer, String, Numeric, Boolean, Table, ForeignKey, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import sqlalchemy.types as types

import constants

class ChoiceType(types.TypeDecorator):

    impl = types.Integer

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.iteritems() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]

Base = declarative_base()


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

    #HERE be actions and categories

    def __repr__(self):
        return self.advertiser_name

class CJLink(Base):
    __tablename__ = 'cj_links'

    id = Column(Integer, primary_key=True, autoincrement=True)
    link_id = Column(String)
    advertiser_id = Column(Integer, ForeignKey('cj_advertisers.id'))
    link_name = Column(String)
    link_type_id = Column(ChoiceType(constants.CJ_LINK_TYPES))
    link_destination = Column(String)
    link_code_html = Column(Text)
    link_code_javascript = Column(Text)
    click_comission = Column(Numeric)
    lead_comission = Column(Numeric)
    sale_comission = Column(Numeric)
    promotion_type = Column(ChoiceType(constants.CJ_PROMOTION_TYPES))
    promotion_start_date = Column(Date)
    promotion_end_date = Column(Date)
    seven_day_epc = Column(Numeric)
    three_month_epc = Column(Numeric)
    creative_height = Column(Integer)
    creative_width = Column(Integer)

    def __repr__(self):
        return self.link_name