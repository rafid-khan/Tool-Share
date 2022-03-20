import unittest
from unittest import TestCase

from src.db.user import fetch_user, fetch_all_users, insert_user, update_user
from src.db.utils import create_server, connect
from test.db.utils import TEST_USER, assert_sql_count, clean_test_data


class TestUser(TestCase):
    conn = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.server = create_server()
        cls.conn = connect()
        cls.cur = cls.conn.cursor()

    def setUp(self) -> None:
        clean_test_data()

        self.cur.execute("SELECT * FROM ts_test_catalog.ts_user")
        self.user_count = self.cur.rowcount

    def test_fetch_user_bad_id(self):
        res = fetch_user(id=0)

        self.assertIsNone(res)

    def test_fetch_all_users(self):
        res = fetch_all_users()

        assert_sql_count(test=self, sql="SELECT * FROM ts_test_catalog.ts_user", n=len(res))

    def test_insert_user(self):
        insert_user(**TEST_USER)

        assert_sql_count(test=self, sql="SELECT * FROM ts_test_catalog.ts_user", n=self.user_count + 1)

    @unittest.skip('not implemented')
    def test_update_user(self):
        insert_user(**TEST_USER)

        update_user(**{'first_name': 'idiot', 'last_name': 'sandwich'})

    @unittest.skip('not implemented')
    def test_delete_user(self):
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        # clean_test_data()
        cls.conn.close()
