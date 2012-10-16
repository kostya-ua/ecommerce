from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, SmallInteger

Base = declarative_base()

class ActionLog(Base):
    __tablename__ = 'action_log'

    id = Column(Integer, primary_key=True)
    user_id =  Column(Integer, ForeignKey('user.id'))
    action = Column(String(2000))
    attributes = Column(Text)
    created_on = Column(DateTime)


class AdminConfigurationOptions(Base):
    __tablename__ = 'admin_configuration_options'

    name = Column(Integer)
    value = Column(String(45))

class AdminUiOptions(Base):
    __tablename__ = 'admin_ui_options'

    id = Column(Integer, primary_key=True)


class AffiliateNetwork(Base):
    __tablename__ = 'affiliate_network'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    sid_name = Column(String(10))
    an_category = relationship("AnCategory")
    deal = relationship("deal")
    merchant = relationship("merchant")


class AnCategory(Base):
    __tablename__ = 'an_category'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    affiliate_network_id = Column(Integer, ForeignKey('affiliate_network.id'))
    an_category_mapping = relationship("AnCategoryMapping")


class AnCategoryMapping(Base):
    __tablename__ = 'an_category_mapping'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    an_category_id = Column(Integer, ForeignKey('an_category.id'))

class BHO(Base):
    __tablename__ = 'bho'

    id = Column(Integer, primary_key=True)
    bho_hash = Column(String(45))
    user_id =  Column(Integer, ForeignKey('user.id'))
    version = Column(String(45))
    key = Column(String(45))
    browser_id = Column(String(45))


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    parent = Column(Integer)
    name = Column(String(225))
    description = Column(Text)

    an_category_mapping = relationship("AnCategoryMapping")
    deal = relationship("Deal")


class Deal(Base):
    __tablename__ = 'deal'

    id = Column(Integer, primary_key=True)

    merchant_id = Column(Integer, ForeignKey('merchant.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
    score_up = Column(Integer, default=1)
    score_down = Column(Integer, default=0)
    coupon_code = Column(String(255))
    coupon_restriction  = Column(String(255))
    description  = Column(String(1024))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    deal_type = Column(String(45))
    commission  = Column(String(45))
    seven_day_epc = Column(Float)
    three_month_epc = Column(Float)
    affiliate_network_id = Column(Integer, ForeignKey('affiliate_network.id'))
    deal_type_id = Column(Integer, ForeignKey('deal_type.id'))
    deal_id = Column(String(20))
    status  = Column(Integer, default=1)
    calculated_score = Column(Float, default=0.206543)
    click_tracking_url = Column(String(1024))
    sid_name = Column(String(1024))

    featured_deal = relationship("featured_deal")

class FeaturedCategory(Base):
    __tablename__ = 'featured_category'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    display_text = Column(String(225))
    location = Column(Integer)
    order = Column(Integer)

class FeaturedDeal(Base):
    __tablename__ = 'featured_deal'

    id = Column(Integer, primary_key=True)
    description = Column(String(45))
    shown_counter = Column(Integer)
    status = Column(Integer)
    banner_html = Column(String(2048))
    updated_on = Column(DateTime)
    created_on = Column(DateTime)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    deal_id = Column(Integer, ForeignKey('deal.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    order = Column(Integer)
    location = Column(Integer)


class FeaturedMerchant(Base):
    __tablename__ = 'featured_merchant'

    id = Column(Integer, primary_key=True)
    merchant_id = Column(Integer, ForeignKey('merchant.id'))
    description = Column(String(45))
    shown_counter = Column(Integer)
    status = Column(Integer)
    banner_html = Column(String(2048))
    updated_on = Column(DateTime)
    created_on = Column(DateTime)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))
    order = Column(Integer)
    location = Column(Integer)
    image_location = Column(String(255))
    rating_box = Column(String(11))


class Merchant(Base):
    __tablename__ = 'merchant'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    url = Column(String(255))
    main_category_id= Column(Integer)
    score_up = Column(Integer)
    score_down = Column(Integer)
    an_merchant_id = Column(Integer, ForeignKey('an_merchant.id'))
    calculated_score = Column(Float, default=0.206543)
    status = Column(Integer)
    affiliate_network_id = Column(Integer, ForeignKey('affiliate_network.id'))
    domain = Column(String(255))
    calc_score_shipping = Column(Float)
    calc_score_service = Column(Float)
    calc_score_quality = Column(Float)
    calc_score_price = Column(Float)
    calc_score_overall = Column(Float)

    featured_merchant = relationship("FeaturedMerchant")
    review = relationship("Review")


class PointAction(Base):
    __tablename__ = "point_action"

    id = Column(Integer, primary_key=True)
    user_id =  Column(Integer, ForeignKey('user.id'))
    points = Column(Integer)
    action = Column(String(45))
    type = Column(String(10))
    type_id = Column(Integer)

class Review(Base):
    __tablename__ = 'avg_review'

    id = Column(Integer, primary_key=True)
    user_id =  Column(Integer, ForeignKey('user.id'))
    merchant_id = Column(Integer, ForeignKey('merchant.id'))
    score_shipping = Column(Integer)
    score_service = Column(Integer)
    score_quality = Column(Integer)
    score_price = Column(Integer)
    score_overall = Column(Integer)
    title = Column(String(45))
    body = Column(Text)
    score_up = Column(Integer)
    score_down = Column(Integer)
    calculated_score = Column(Float, default=0.206543)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)

    user_preference_id = Column(Integer, ForeignKey('user_preference.id'))
    first_name = Column(String(45))
    last_name = Column(String(45))
    email = Column(String(45))
    total_influence = Column(Integer, default=1)
    current_balance_influence = Column(Integer)
    score_up = Column(Integer, default=1)
    score_down = Column(Integer, default=0)
    calculated_score = Column(Float, default=0.206543)
    ip_address = Column(String(40))
    username = Column(String(100))
    password = Column(String(40))
    salt = Column(String(40))
    activation_code = Column(String(40))
    forgotten_password_code = Column(String(40))
    forgotten_password_time = Column(String(40))
    remember_code = Column(String(40))
    created_on = Column(Integer)
    last_login = Column(Integer)
    active = Column(SmallInteger)
    company = Column(String(100))
    phone = Column(String(20))
    oauth_uid = Column(String(100))
    oauth_provider = Column(String(20))

    action_log = relationship("ActionLog")
    bho = relationship("BHO")
    featured_deal = relationship("FeaturedDeal")
    featured_merchant = relationship("FeaturedMerchant")
    point_action = relationship("PointAction")
    review = relationship("Review")