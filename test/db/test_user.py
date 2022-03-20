from unittest import TestCase

from src.db.user import fetch_user
from src.db.utils import create_server, connect


class TestUser(TestCase):
    conn = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.server = create_server()
        cls.conn = connect()
        cls.cur = cls.conn.cursor()

    def test_fetch_user_bad_id(self):
        res = fetch_user(id=0)

        self.assertEqual(None, res)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.conn.close()
