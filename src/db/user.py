
from psycopg2.sql import Identifier, SQL

from .utils import fetch_many, fetch_one, commit


# WORKS
def fetch_user(username):
    return fetch_one("""
        SELECT * FROM p320_24.user WHERE username = %s 
    """, (username,))


# WORKS
def fetch_all_users():
    return fetch_many("""
        SELECT * FROM p320_24.user
    """)


def insert_user(**kwargs):
    commit("""
        INSERT INTO p320_24.user (first_name, last_name, username, password) VALUES (%s, %s, %s, %s)
    """, (tuple(kwargs.values())))

    commit("""
                UPDATE p320_24.user SET last_date_accessed = now() WHERE username = %s
            """, (kwargs.get("a"),))
    commit("""
                    UPDATE p320_24.user SET creation_date = now() WHERE username = %s
                """, (kwargs.get("a"),))


def insert_email(**kwargs):
    commit("""
        INSERT INTO p320_24.email (username, email) VALUES (%s, %s)
    """, (tuple(kwargs.values())))


def update_user(username, **kwargs):
    query = SQL("UPDATE p320_24.user SET ({}) = %s WHERE username = %s") \
        .format(SQL(', ').join(map(Identifier, list(kwargs.keys()))))

    commit(query, (tuple(kwargs.values()), username))


def update_email(username, **kwargs):
    query = SQL("UPDATE p320_24.email SET ({}) = %s WHERE username = %s") \
        .format(SQL(', ').join(map(Identifier, list(kwargs.keys()))))

    commit(query, (tuple(kwargs.values()), username))


def delete_user(username):
    commit("""
        DELETE FROM p320_24."user" WHERE username = '%s'
    """, (username,))


# QUERY WORKS
def log_in(username, password):
    correct_password = fetch_one("""
        SELECT password FROM p320_24.user WHERE username = %s
    """, (username,))
    if correct_password is not None:
        if correct_password['password'] == password:
            commit("""
                UPDATE p320_24.user SET last_date_accessed = now() WHERE username = %s
            """, (username,))
            return True

    return False

