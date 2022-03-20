import unittest

from src.utils import start_server


class TestDB(unittest.TestCase):
    server = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.server = start_server().start()
        # return cls.server

    def test_can_connect(self):
        self.cur.execute('SELECT VERSION()')
        self.assertTrue(self.cur.fetchone()[0].startswith('PostgreSQL'))

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.close()
