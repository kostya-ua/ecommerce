import datetime
import urllib
from lxml import etree

from harvester.models.meta import DBSession

from models.linkshare import LinkShareCategory, LinkShareDeal, LinkShareMerchant, LinkShareNetwork, LinkSharePromotionType

API_URL = "http://couponfeed.linksynergy.com/coupon"

class InternalError(Exception):
    pass

class AccessDenied(Exception):
    pass

class QuotaExceeded(Exception):
    pass

class InvalidRequest(Exception):
    pass


def get_deals_and_merchants(token, results_per_page =100, **kwargs):
    page_number = 1
    last_page = False

    while not last_page:

        url = "{}?{}".format(API_URL, urllib.urlencode({'token': token,
                                                    'resultsperpage': results_per_page,
                                                    'pagenumber': page_number}.update(kwargs)))
        file = urllib.urlopen(url)
        response_elements = parse_response(file.read())

        if response_elements['page_number_requested'] == response_elements['total_pages']:
            last_page = True

        url = response_elements['deal']['click_tracking_url']
        redirect_url = urllib.urlopen(url).geturl()
        response_elements['merchant']['domain'] = redirect_url.split('?')[0]

        save(response_elements)
        page_number += 1


def parse_response(response):
    root = etree.fromstring(response.replace('&','&amp;'))

    if root.tag == 'fault':
        code = root.find('errorcode').text
        message = root.find('errorstring').text
        handle_error(code, message)

    total_matches = root.find('TotalMatches').text
    total_pages = root.find('TotalPages')
    page_number_requested = root.find('PageNumberRequested')

    link = root.find('link')
    categories = link.find('categories')
    promotion_types = link.find('promotiontypes')
    offer_description = link.find('offerdescription').text
    offer_start_date = link.find('offerstartdate').text
    offer_end_date = link.find('offerenddate').text
    coupon_code = link.find('couponcode')
    coupon_restriction= link.find('couponrestriction')
    click_url = link.find('clickurl').text
    impression_pixel = link.find('impressionpixel')
    advertiser_id= link.find('advertiserid').text
    advertiser_name= link.find('advertisername').text
    network = link.find('network')

    response_elements = {
        'total_matches': int(total_matches),
        'total_pages': int(total_pages.text) if total_pages is not None else None,
        'page_number_requested': int(page_number_requested.text) if page_number_requested  is not None else None,
        'merchant': {
            'external_id': int(advertiser_id),
            'name': advertiser_name
        },
        'network': {
            'id': int(network.attrib.get('id')),
            'name': network.text
        }
    }

    deal = {
        'description': offer_description,
        'start_date': datetime.datetime.strptime(offer_start_date, "%Y-%m-%d"),
        'end_date': datetime.datetime.strptime(offer_end_date, "%Y-%m-%d"),
        'coupon_code': coupon_code.text if coupon_code is not None else None,
        'coupon_restriction': coupon_restriction.text if coupon_restriction is not None else None,
        'click_tracking_url': click_url,
        'impression_pixel': impression_pixel.text if impression_pixel is not None else None,
    }

    response_elements['deal'] = deal

    response_elements['categories'] = []
    for category in categories.findall('category'):
        response_elements['categories'].append({'id': int(category.attrib.get('id')), 'name':category.text})

    response_elements['promotion_types'] = []
    for promotion_type in promotion_types.findall('promotiontype'):
        response_elements['promotion_types'].append({'id': int(promotion_type.attrib.get('id')),
                                                     'name':promotion_type.text})

    return response_elements


def save(response_elements):
    session = DBSession()

    network = LinkShareNetwork(**response_elements['network'])
    if not session.query(LinkShareNetwork).filter_by(id=response_elements['network']['id']):
        session.add(network)

    merchant = LinkShareMerchant(network_id=network.id, **response_elements['merchant'])
    session.add(merchant)

    deal = LinkShareDeal(network_id=network.id, merchant_id=merchant.id, **response_elements['deal'])
    deal.categories=[LinkShareCategory(**category) for category in response_elements['categories']]
    deal.promotion_types=[LinkSharePromotionType(**promotion_type) for promotion_type in response_elements['promotion_types']]

    session.add(deal)
    session.commit()


def handle_error(code, message):
    errors = {'10': InternalError, '20': AccessDenied, '30': QuotaExceeded, '40': InvalidRequest}

    raise errors.get(code, Exception)(message)