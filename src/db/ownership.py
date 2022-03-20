from psycopg2.sql import SQL, Identifier

from .utils import fetch_one, commit


def fetch_ownership(user, code):
    return fetch_one("""
        SELECT * FROM ts_ownership WHERE username = %s AND barcode = %s
    """, (user, code))


def insert_ownership(**kwargs):
    commit("""
        INSERT INTO ts_ownership (username, barcode, purchase_price, purchase_date) VALUES (%s, %s, %s, %s)
    """, (tuple(kwargs.values())))


def update_ownership(user, code, **kwargs):
    query = SQL("UPDATE ts_ownership SET ({}) = %s WHERE username = %s AND barcode = %s") \
        .format(SQL(', ').join(map(Identifier, list(kwargs.keys()))))

    commit(query, (tuple(kwargs.values()), user, code))


def delete_ownership(user, code):
    commit("""
        DELETE FROM ts_ownership WHERE username = %s AND barcode = %s
    """, (user, code))
