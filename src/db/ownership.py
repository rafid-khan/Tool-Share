from psycopg2.sql import SQL, Identifier

from .utils import fetch_one, commit


# ALL FUNCTIONS SHOULD WORK
def fetch_ownership(user, code=None):
    return fetch_one("""
        SELECT * FROM p320_24.ownership WHERE username = %s AND barcode = %s
    """, (user, code)) if code else fetch_one("""
        SELECT * FROM p320_24.ownership WHERE username = %s
    """, (user,))


def insert_ownership(**kwargs):
    commit("""
        INSERT INTO p320_24.ownership (username, barcode, purchase_price, purchase_date) VALUES (%s, %s, %s, now())
    """, (tuple(kwargs.values())))


def update_ownership(user, code, **kwargs):
    query = SQL("UPDATE p320_24.ownership SET ({}) = %s WHERE username = %s AND barcode = %s") \
        .format(SQL(', ').join(map(Identifier, list(kwargs.keys()))))

    commit(query, (tuple(kwargs.values()), user, code))


def delete_ownership(user, code):
    commit("""
        DELETE FROM p320_24.ownership WHERE username = %s AND barcode = %s
    """, (user, code))
