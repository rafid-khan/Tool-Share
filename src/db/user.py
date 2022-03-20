from psycopg2.sql import Identifier, SQL

from .utils import fetch_many, fetch_one, commit


def fetch_user(id):
    return fetch_one("""
        SELECT * FROM ts_test_catalog.ts_user WHERE user_id = %s 
    """, (id,))


def fetch_all_users():
    return fetch_many("""
        SELECT * FROM ts_test_catalog.ts_user
    """)


def insert_user(**kwargs):
    commit("""
        INSERT INTO ts_test_catalog.ts_user (first_name, last_name, username, password) VALUES (%s, %s, %s, %s)
    """, (tuple(kwargs.values())))


def update_user(id, **kwargs):
    query = SQL("UPDATE ts_test_catalog.ts_user SET ({}) = %s WHERE user_id = %s") \
        .format(SQL(', ').join(map(Identifier, list(kwargs.keys()))))

    commit(query, (tuple(kwargs.values()), id))


def delete_user(id):
    commit("""
        DELETE FROM ts_test_catalog.ts_user WHERE user_id = %s
    """, (id,))
