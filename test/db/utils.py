from src.db.utils import connect, commit, fetch_one

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


def fetch_test_user():
    return fetch_one("""
        SELECT * FROM ts_test_catalog.ts_user WHERE username = %s
    """, (TEST_USER['username'],))


def insert_test_user():
    commit("""
        INSERT INTO ts_test_catalog.ts_user (first_name, last_name, username, password) VALUES (%s, %s, %s, %s)
    """, (tuple(TEST_USER.values())))


def assert_sql_count(test, sql, params=None, n=0, msg='Expected row count did not match query'):
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, params) if params else cur.execute(sql)
    test.assertEqual(n, cur.rowcount, msg)
    conn.close()
