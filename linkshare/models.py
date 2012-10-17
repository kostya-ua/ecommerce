from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Table

Base = declarative_base()

deal_category = Table('deal_category', Base.metadata,
    Column('deal_id', Integer, ForeignKey('deal.id')),
    Column('category_id', Integer, ForeignKey('category.id'))
)

class LinkShareDeal(Base):
    __tablename__ = 'link_share_deal'

    id = Column(Integer, primary_key=True)

    merchant_id = Column(Integer, ForeignKey('link_share_merchant.id'))
    network_id = Column(Integer, ForeignKey('link_share_network.id'))

    categories = relationship("LinkShareCategory", secondary=deal_category, backref="deals")
    promotion_types = relationship("LinkSharePromotionType", secondary=deal_category, backref="deals")

    description  = Column(String(1024))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    coupon_code = Column(String(255))
    coupon_restriction  = Column(String(255))
    click_tracking_url = Column(String(1024))
    impression_pixel = Column(String(1024))

    status  = Column(Integer, default=1)

    score_up = Column(Integer, default=1)
    score_down = Column(Integer, default=0)
    calculated_score = Column(Float, default=0.206543)

class LinkShareMerchant(Base):
    __tablename__ = 'link_share_merchant'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    url = Column(String(255))
    external_id = Column(Integer)
    status = Column(Integer)
    network_id = Column(Integer, ForeignKey('link_share_network.id'))
    domain = Column(String(255))

    score_up = Column(Integer)
    score_down = Column(Integer)
    calculated_score = Column(Float, default=0.206543)
    calc_score_shipping = Column(Float)
    calc_score_service = Column(Float)
    calc_score_quality = Column(Float)
    calc_score_price = Column(Float)
    calc_score_overall = Column(Float)

    deals = relationship('LinkShareDeal')

class LinkShareNetwork(Base):
    __tablename__ = 'link_share_network'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    deals = relationship('LinkShareDeal')


class LinkShareCategory(Base):
    __tablename__ = 'link_share_category'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

class LinkSharePromotionType(Base):
    __tablename__ = 'link_share_promotion_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

