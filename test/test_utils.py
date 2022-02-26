import unittest

from src.utils import start_server, get_conn


class TestDB(unittest.TestCase):
    server = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.server = start_server()

    def test_can_connect(self):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('SELECT VERSION()')
        self.assertTrue(cur.fetchone()[0].startswith('PostgreSQL'))
        conn.close()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.close()
