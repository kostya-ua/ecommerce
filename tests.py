import unittest
import datetime

import simplejson as json

from mock import patch, Mock
from sqlalchemy import create_engine
from oauth2client.client import OAuth2Credentials, AccessTokenRefreshError

from harvester.models.gan import GoogleCredential
from harvester.gan.gan import DBCredentialStorage
from harvester.models.meta import initialize_sql, DBSession
from harvester.linkshare import parse_response, save
from harvester.models.linkshare import LinkShareDeal


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite://', echo=False)
        cls.connection = cls.engine.connect()
        initialize_sql(cls.connection)

    def setUp(self):
        # begin a non-ORM transaction
        self.trans = self.connection.begin()

        # bind an individual Session to the connection
        self.session = DBSession()

    def tearDown(self):
        self.trans.rollback()
        self.session.close()


class GANCredentialTest(BaseTestCase):
    def setUp(self):
        super(GANCredentialTest, self).setUp()

        self.base_credential = GoogleCredential(
            access_token="ya29.AHES6ZSxOii_ZzC2kozr3MMMi_2gzjTehD_5TELtW3T_y2Q6kot32Q",
            token_uri="https://accounts.google.com/o/oauth2/token",
            client_id="982196753510-89egjhekmmmqmn9fthdvngr836k03tgu.apps.googleusercontent.com",
            client_secret="ZpVxOuv4v55oqkolllkF3S41",
        )

    def test_credentials(self):
        self.session.add(self.base_credential)
        self.session.flush()

        credentials = DBCredentialStorage().get()
        self.assertEqual(self.base_credential.access_token, credentials.access_token)


    def test_expired_credentials(self):
        self.base_credential.token_expiry = datetime.datetime(2012, 01, 01)

        self.session.add(self.base_credential)
        self.session.flush()

        response = Mock()
        response.status = 200
        content = json.dumps({
            'access_token': 'aaaaa',
            'refresh_token': 'bbbbb',
            'expires_in': 86400
        })

        with patch('httplib2.Http.request', return_value=(response, content)):
            credentials = DBCredentialStorage().get()

        self.assertEqual(credentials.access_token, 'aaaaa')
        self.assertAlmostEqualDates(credentials.token_expiry, datetime.datetime.utcnow() + datetime.timedelta(days=1))

        self.session.refresh(self.base_credential)
        self.assertEqual(self.base_credential.refresh_token, 'bbbbb')

    def test_saving_credentials(self):
        oauth_credentials = OAuth2Credentials(
            access_token='aaa',
            refresh_token='bbb',
            client_id='12345',
            client_secret='1111',
            token_uri=None,
            token_expiry=datetime.datetime.now(),
            user_agent=None
        )

        storage = DBCredentialStorage()
        storage.put(oauth_credentials)

        credentials = self.session.query(GoogleCredential).first()
        self.assertEqual(credentials.access_token, 'aaa')
        self.assertEqual(credentials.client_id, '12345')

    @patch('oauth2client.client.OAuth2Credentials._refresh', side_effect=AccessTokenRefreshError)
    @patch('harvester.gan.credentials.DBCredentialStorage.refresh', return_value='result')
    def test_refreshing_credentials(self, run, refresh):
        self.base_credential.token_expiry = datetime.datetime(2012, 01, 01)

        self.session.add(self.base_credential)
        self.session.flush()

        storage = DBCredentialStorage()
        self.assertEqual(storage.get(), 'result')



    def assertAlmostEqualDates(self, date1, date2):
        assert isinstance(date1, datetime.datetime)
        assert isinstance(date2, datetime.datetime)

        self.assertEqual(date1.replace(microsecond=0), date2.replace(microsecond=0))

class CJTest(BaseTestCase):
    pass


class TestLinkshare(BaseTestCase):
    def setUp(self):
        super(TestLinkshare, self).setUp()
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
        self.response_elements = {
            'merchant': {
                'external_id': 0,
                'name': 'Sample Advertiser Name'
            },
            'network': {
                'id': 1,
                'name': 'Linkshare Network'
            },
            'deal': {
                'description': '15 percent off',
                'end_date': datetime.datetime(2009, 5, 31, 0, 0),
                'impression_pixel': 'http://ad.linksynergy.com/fs-bin/show?id=XXXXXXXXXXX&bids=164317.10002595&type=4&subid=0',
                'coupon_code': 'KJEISLD',
                'coupon_restriction': 'New Customers Only',
                'click_tracking_url': 'http://click.linksynergy.com/fs-bin/click?id=XXXXXXXXXXX&offerid=164317.10002595&type=4&subid=0',
                'start_date': datetime.datetime(2009, 4, 1, 0, 0)
            },
            'total_matches': 1,
            'total_pages': 1,
            'page_number_requested': 1,
            'promotion_types': [{'id': 22, 'name': 'percentage off'}],
            'categories': [
                {'id': 983, 'name': 'computers'},
                {'id': 12, 'name': 'electronics'},
                {'id': 14, 'name': 'gifts'}]
        }


    def test_parse_response(self):
        response_elements = parse_response(self.response)

        self.assertEqual(response_elements['total_matches'], 1)
        self.assertEqual(response_elements['total_pages'], 1)
        self.assertEqual(response_elements['page_number_requested'], 1)
        self.assertEqual(response_elements['categories'],  self.response_elements['categories'])
        self.assertEqual(response_elements['promotion_types'],[{'id': 22, 'name': 'percentage off'}])
        self.assertEqual(response_elements['merchant'], {'external_id': 0, 'name': 'Sample Advertiser Name'})
        self.assertEqual(response_elements['network'], {'id': 1, 'name': 'Linkshare Network'})
        self.assertEqual(response_elements['deal'], self.response_elements['deal'])

    def test_save(self):
        save(self.response_elements)
        deal = self.session.query(LinkShareDeal).all()[0]

        self.assertEqual(deal.description, self.response_elements['deal']['description'])
        self.assertEqual(deal.start_date, self.response_elements['deal']['start_date'])
        self.assertEqual(deal.end_date, self.response_elements['deal']['end_date'])
        self.assertEqual(deal.coupon_code, self.response_elements['deal']['coupon_code'])
        self.assertEqual(deal.coupon_restriction, self.response_elements['deal']['coupon_restriction'])
        self.assertEqual(deal.click_tracking_url, self.response_elements['deal']['click_tracking_url'])
        self.assertEqual(deal.impression_pixel, self.response_elements['deal']['impression_pixel'])


if __name__ == '__main__':
    unittest.main()