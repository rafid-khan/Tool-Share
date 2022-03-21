from unittest import TestCase

from src.db.tool import fetch_tool, fetch_all_tools, insert_tool, update_tool, delete_tool
from src.db.utils import create_server, row_count
from test.db.utils import TEST_TOOL, clean_test_data, insert_test_tool, fetch_test_tool, assert_sql_count


class TestTool(TestCase):
    server = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.server = create_server()

    def setUp(self) -> None:
        insert_test_tool()
        self.test_tool = fetch_test_tool()
        self.test_params = {'category': 'drill', 'name': 'Electric Drill', 'description': 'Bro its a drill'}
        self.tool_count = row_count("SELECT * FROM ts_test_catalog.ts_tool")

    def test_fetch_tool(self):
        res = fetch_tool(self.test_tool['barcode'])

        self.assertIsNotNone(res)

    def test_fetch_all_tools(self):
        res = fetch_all_tools()

        self.assertIsNotNone(res)
        assert_sql_count(test=self, sql="SELECT * FROM ts_test_catalog.ts_tool", n=len(res))

    def test_insert_tool(self):
        insert_tool(**TEST_TOOL)

        assert_sql_count(test=self, sql="SELECT * FROM ts_test_catalog.ts_tool", n=self.tool_count + 1)

    def test_update_tool(self):
        update_tool(self.test_tool['barcode'], **self.test_params)

        updated_tool = fetch_test_tool()

        self.assertEqual(self.test_params['category'], updated_tool['category'])
        self.assertEqual(self.test_params['name'], updated_tool['name'])
        self.assertEqual(self.test_params['description'], updated_tool['description'])
        assert_sql_count(test=self, sql="SELECT * FROM ts_test_catalog.ts_tool", n=self.tool_count)

    def test_delete_tool(self):
        delete_tool(self.test_tool['barcode'])

        assert_sql_count(test=self, sql="SELECT * FROM ts_test_catalog.ts_tool", n=self.tool_count - 1)

    def tearDown(self) -> None:
        clean_test_data()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.close()
