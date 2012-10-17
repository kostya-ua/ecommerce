import unittest
import datetime

import simplejson as json

from mock import patch, Mock
from sqlalchemy import create_engine

from oauth2client.client import OAuth2Credentials, AccessTokenRefreshError

from harvester.models.gan import GoogleCredential
from harvester.models.meta import initialize_sql, DBSession

from harvester.gan.credentials import DBCredentialStorage

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


if __name__ == '__main__':
    unittest.main()