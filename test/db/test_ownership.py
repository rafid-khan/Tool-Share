import unittest
from unittest import TestCase

from src.db.ownership import fetch_ownership
from src.db.utils import create_server, row_count
from test.db.utils import clean_test_data, insert_test_ownership, fetch_test_ownership, assert_sql_count


class TestOwnership(TestCase):
    server = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.server = create_server()

    def setUp(self) -> None:
        insert_test_ownership()
        self.test_ownership = fetch_test_ownership()
        self.test_params = {'purchase_price': 694.20, 'purchase_date': '12/19/2001'}
        self.ownership_count = row_count("SELECT * FROM ts_test_catalog.ts_ownership")

    def test_fetch_ownership(self):
        fetch_ownership(self.test_ownership['username'], self.test_ownership['barcode'])

        assert_sql_count(test=self, sql="SELECT * FROM ts_test_catalog.ts_ownership", n=1)

    @unittest.skip('not implemented')
    def test_insert_ownership(self):
        pass

    @unittest.skip('not implemented')
    def test_update_ownership(self):
        pass

    @unittest.skip('not implemented')
    def test_delete_ownership(self):
        pass

    def tearDown(self) -> None:
        clean_test_data()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.close()
