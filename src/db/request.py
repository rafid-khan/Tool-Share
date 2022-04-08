from psycopg2.sql import SQL, Identifier

from .utils import fetch_one, fetch_many, commit


def fetch_users_borrowed_tools(username):
    return fetch_many("""
        SELECT barcode FROM p320_24.request WHERE username = %s AND status = TRUE
    """, (username,))


def create_request(**kwargs):
    commit("""
            INSERT INTO p320_24.request (request_id, username, barcode, status, borrow_period, request_date) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (tuple(kwargs.values())))


# TODO
def get_users_requests_received(username):
    return fetch_many("""
        SELECT username = %s FROM p320_24.ownership WHERE barcode 
        IN (SELECT barcode FROM p320_24.request)
    """, (username,))


def get_users_requests_made(**kwargs):
    return fetch_many("""
        SELECT request_id, barcode, borrow_period, request_date, status 
        FROM p320_24.request WHERE username = %s 
    """, (tuple(kwargs.values())))


# TODO
def handle_requests(is_accepted, request_id):
    pass


def fetch_lent_tools():
    return fetch_many("""
        SELECT barcode FROM p320_24.request WHERE request_date < (request_date + borrow_period)
    """)


# TODO
def fetch_borrowed_tools():
    pass


# TODO
def fetch_overdue_tools():
    pass


# TODO
def get_available_tools():
    pass

