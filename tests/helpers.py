import unittest
from sqlalchemy import create_engine

from harvester.models.meta import initialize_sql, DBSession


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
