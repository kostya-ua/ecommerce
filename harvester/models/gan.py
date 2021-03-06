from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship

from meta import Base

class GoogleCategory(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

class GoogleMerchant(Base):
    __tablename__ = 'google_merchants'

    id = Column(Integer, primary_key=True)
    external_id = Column(Integer)
    name = Column(String(50))
    description = Column(String(255))
    is_active = Column(Boolean)

    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(GoogleCategory, primaryjoin=category_id==GoogleCategory.id)

    domain = Column(String(50))
    destination_url = Column(String(255))

    start_date = Column(DateTime)
    end_date = Column(DateTime)

    epc_seven_days = Column(Numeric)
    epc_ninety_days = Column(Numeric)

    status = Column(String)

class GoogleDealType(Base):
    __tablename__ = 'google_deal_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

class GoogleDeal(Base):
    __tablename__ = 'google_deals'

    id = Column(Integer, primary_key=True)
    external_id = Column(Integer)
    description = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    is_active = Column(Boolean)
    is_expired = Column(Boolean)
    destination_url = Column(String(255))
    click_tracking_url = Column(String(255))

    merchant_id = Column(Integer, ForeignKey('google_merchants.id'))
    merchant = relationship(GoogleMerchant, primaryjoin=merchant_id==GoogleMerchant.id)

    link_type_id = Column(Integer, ForeignKey('google_deal_types.id'))
    link_type = relationship(GoogleDealType, primaryjoin=link_type_id==GoogleDealType.id)

class GoogleCredential(Base):
    __tablename__ = 'google_credentials'

    id = Column(Integer, primary_key=True)
    access_token = Column(String(255))
    client_id = Column(String(255))
    client_secret = Column(String(255))
    refresh_token = Column(String(255))
    token_expiry = Column(DateTime)
    token_uri = Column(String(255))

