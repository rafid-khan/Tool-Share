from unittest import TestCase

from src.db.user import fetch_user, fetch_all_users, insert_user, update_user, delete_user
from src.db.utils import create_server, row_count
from test.db.utils import TEST_USER, assert_sql_count, clean_test_data, fetch_test_user, insert_test_user


class TestUser(TestCase):
    server = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.server = create_server()

    def setUp(self) -> None:
        insert_test_user()
        self.test_user = fetch_test_user()
        self.test_params = {'first_name': 'idiot', 'last_name': 'sandwich'}
        self.user_count = row_count("SELECT * FROM ts_test_catalog.ts_user")

    def test_fetch_user(self):
        res = fetch_user(id=self.test_user['user_id'])

        self.assertIsNotNone(res)

    def test_fetch_user_bad_id(self):
        res = fetch_user(id=0)

        self.assertIsNone(res)

    def test_fetch_all_users(self):
        res = fetch_all_users()

        assert_sql_count(test=self, sql="SELECT * FROM ts_test_catalog.ts_user", n=len(res))

    def test_insert_user(self):
        insert_user(**TEST_USER)

        assert_sql_count(test=self, sql="SELECT * FROM ts_test_catalog.ts_user", n=self.user_count + 1)

    def test_update_user(self):
        update_user(self.test_user['user_id'], **self.test_params)

        updated_user = fetch_test_user()

        self.assertEqual(self.test_params['first_name'], updated_user['first_name'])
        self.assertEqual(self.test_params['last_name'], updated_user['last_name'])

        assert_sql_count(test=self, sql="SELECT * FROM ts_test_catalog.ts_user", n=self.user_count)

    def test_delete_user(self):
        delete_user(self.test_user['user_id'])

        assert_sql_count(test=self, sql="SELECT * FROM ts_test_catalog.ts_user", n=self.user_count - 1)

    def tearDown(self) -> None:
        clean_test_data()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.close()
