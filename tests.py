import unittest
import datetime

import simplejson as json

from mock import patch, Mock
from sqlalchemy import create_engine

from harvester.models.gan import GoogleCredential
from harvester.models.meta import initialize_sql, DBSession

from harvester.gan import DBCredentialStorage

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

class GANTest(BaseTestCase):
    def setUp(self):
        super(GANTest, self).setUp()

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



if __name__ == '__main__':
    unittest.main()