import unittest

from src.db.utils import create_server, connect


class TestDB(unittest.TestCase):
    server = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.server = create_server()

    def setUp(self) -> None:
        self.conn = connect()
        self.cur = self.conn.cursor()

    def test_can_connect(self):
        self.cur.execute('SELECT VERSION()')
        self.assertTrue(self.cur.fetchone()[0].startswith('PostgreSQL'))

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.close()
