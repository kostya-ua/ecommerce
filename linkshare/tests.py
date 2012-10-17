import datetime
import unittest
from linkshare.linkshare import parse_response, save

class TestLinkshare(unittest.TestCase):
    def setUp(self):
        self.response = """<?xml version="1.0" encoding="UTF-8"?>
        <couponfeed>
           <TotalMatches>1</TotalMatches>
           <TotalPages>1</TotalPages>
           <PageNumberRequested>1</PageNumberRequested>
           <link type="TEXT">
              <categories>
                 <category id="983">computers</category>
                 <category id="12">electronics</category>
                 <category id="14">gifts</category>
              </categories>
              <promotiontypes>
                 <promotiontype id="22">percentage off</promotiontype>
              </promotiontypes>
              <offerdescription>15 percent off</offerdescription>
              <offerstartdate>2009-04-01</offerstartdate>
              <offerenddate>2009-05-31</offerenddate>
              <couponcode>KJEISLD</couponcode>
              <couponrestriction>New Customers Only</couponrestriction>
              <clickurl>http://click.linksynergy.com/fs-bin/click?id=XXXXXXXXXXX&offerid=164317.10002595&type=4&subid=0</clickurl>
              <impressionpixel>http://ad.linksynergy.com/fs-bin/show?id=XXXXXXXXXXX&bids=164317.10002595&type=4&subid=0</impressionpixel>
              <advertiserid>000</advertiserid>
              <advertisername>Sample Advertiser Name</advertisername>
              <network id="1">Linkshare Network</network>
           </link>
        </couponfeed>

        """

        self.response_elements = {'merchant': {'external_id': 0, 'name': 'Sample Advertiser Name'},
                                  'network': {'id': 1, 'name': 'Linkshare Network'},
                                  'deal': {'description': '15 percent off', 'end_date': datetime.datetime(2009, 5, 31, 0, 0),
                                           'impression_pixel': 'http://ad.linksynergy.com/fs-bin/show?id=XXXXXXXXXXX&bids=164317.10002595&type=4&subid=0',
                                           'coupon_code': 'KJEISLD', 'coupon_restriction': 'New Customers Only',
                                           'click_tracking_url': 'http://click.linksynergy.com/fs-bin/click?id=XXXXXXXXXXX&offerid=164317.10002595&type=4&subid=0',
                                           'start_date': datetime.datetime(2009, 4, 1, 0, 0)},
                                  'total_matches': 1, 'total_pages': 1, 'page_number_requested': 1,
                                  'promotion_types': [{'id': 22, 'name': 'percentage off'}],
                                  'categories': [{'id': 983, 'name': 'computers'}, {'id': 12, 'name': 'electronics'}, {'id': 14, 'name': 'gifts'}]}


    def test_parse_response(self):
        response_elements = parse_response(self.response)

        self.assertEqual(response_elements['total_matches'], 1)
        self.assertEqual(response_elements['total_pages'], 1)
        self.assertEqual(response_elements['page_number_requested'], 1)
        self.assertEqual(response_elements['categories'],  [{'id': 983, 'name': 'computers'}, {'id': 12, 'name': 'electronics'}, {'id': 14, 'name': 'gifts'}])
        self.assertEqual(response_elements['promotion_types'],[{'id': 22, 'name': 'percentage off'}])
        self.assertEqual(response_elements['merchant'], {'external_id': 0, 'name': 'Sample Advertiser Name'})
        self.assertEqual(response_elements['network'], {'id': 1, 'name': 'Linkshare Network'})

        self.assertEqual(response_elements['deal'], {'description': '15 percent off', 'end_date': datetime.datetime(2009, 5, 31, 0, 0),
                                                     'impression_pixel': 'http://ad.linksynergy.com/fs-bin/show?id=XXXXXXXXXXX&bids=164317.10002595&type=4&subid=0',
                                                     'coupon_code': 'KJEISLD', 'coupon_restriction': 'New Customers Only',
                                                     'click_tracking_url': 'http://click.linksynergy.com/fs-bin/click?id=XXXXXXXXXXX&offerid=164317.10002595&type=4&subid=0',
                                                     'start_date': datetime.datetime(2009, 4, 1, 0, 0)})

    def test_save(self):
        save(self.response_elements)


