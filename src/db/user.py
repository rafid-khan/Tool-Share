from .utils import fetch_many, fetch_one, commit


def fetch_user(id):
    return fetch_one("""
        SELECT * FROM ts_catalog.ts_user WHERE user_id = %s 
    """, (id,))


def insert_user():
    pass


def update_user():
    pass


def delete_user():
    pass
