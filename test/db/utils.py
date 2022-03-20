from src.db.utils import connect, commit

TEST_USER = {
    'first_name': 'Johnny',
    'last_name': 'Test',
    'username': 'lab-rat',
    'password': 'Str0ngP@ssword22'
}


def clean_test_data():
    commit("""
        CALL ts_test_catalog.delete_test_data()
    """)


def assert_sql_count(test, sql, params=None, n=0, msg='Expected row count did not match query'):
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, params) if params else cur.execute(sql)
    test.assertEqual(n, cur.rowcount, msg)
    conn.close()
