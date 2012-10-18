from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, Text, Date, Enum

from meta import Base
from harvester import constants



class CJMerchant(Base):
    __tablename__ = 'cj_merchants'

    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String)
    name = Column(String)
    account_status = Column(Enum(*constants.CJ_ACCOUNT_STATUSES))
    seven_day_epc = Column(Numeric)
    three_month_epc = Column(Numeric)
    language = Column(String)
    program_url = Column(String)
    relationship_status = Column(Enum(*constants.CJ_RELATIONSHIP_STATUSES))
    mobile_supported = Column(Boolean)
    mobile_tracking_certified = Column(Boolean)
    network_rank = Column(Integer)
    performance_incentives = Column(Boolean)

    #HERE be actions and categories

    def __repr__(self):
        return self.advertiser_name

class CJDeal(Base):
    __tablename__ = 'cj_deals'

    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String)
    merchant_id = Column(Integer, ForeignKey('cj_merchants.id'))
    name = Column(String)
    deal_type = Column(Enum(*constants.CJ_LINK_TYPES))
    destination = Column(String)
    code_html = Column(Text)
    code_javascript = Column(Text)
    click_comission = Column(Numeric)
    lead_comission = Column(Numeric)
    sale_comission = Column(Numeric)
    promotion_type = Column(Enum(*constants.CJ_PROMOTION_TYPES))
    promotion_start_date = Column(Date)
    promotion_end_date = Column(Date)
    seven_day_epc = Column(Numeric)
    three_month_epc = Column(Numeric)
    creative_height = Column(Integer)
    creative_width = Column(Integer)

    def __repr__(self):
        return self.link_name