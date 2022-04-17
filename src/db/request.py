import datetime

from psycopg2.sql import SQL, Identifier

from .utils import fetch_one, fetch_many, commit


# WORKS
def create_request(**kwargs):
    commit("""
            INSERT INTO p320_24.request (request_id, username, barcode, status, borrow_period, request_date) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (tuple(kwargs.values())))


# WORKS
def get_users_requests_received(username):
    return fetch_many("""
        SELECT * FROM p320_24.request WHERE barcode IN
        (SELECT barcode FROM p320_24.ownership WHERE p320_24.ownership.username = %s)
    """, (username,))


# WORKS
def get_users_requests_made(username):
    return fetch_many("""
        SELECT * FROM p320_24.request WHERE username = %s 
    """, (username,))


def handle_requests(is_accepted, request_id):
    if is_accepted:
        commit("""
            UPDATE p320_24.request SET status = 'ACCEPTED' WHERE request_id = %s 
        """, (request_id,))

        commit("""
            UPDATE p320_24.tool SET shareable = False WHERE barcode IN 
            (SELECT barcode FROM p320_24.request WHERE request_id = %s)
        """, (request_id,))

        commit("""
            UPDATE p320_24.tool
            SET holder = p320_24.request.username
            FROM p320_24.tool, p320_24.request
            WHERE p320_24.tool.barcode = p320_24.request.barcode
            AND p320_24.request.request_id = %s
        """, (request_id,))

    else:
        commit("""
            UPDATE p320_24.request SET status = 'DENIED' WHERE request_id = %s
        """, (request_id,))


def return_tool(barcode):
    commit("""
        UPDATE p320_24.tool SET holder = p320_24.ownership.username 
        WHERE p320_24.ownership.username IN (SELECT username FROM p320_24.ownership 
        WHERE p320_24.ownership.barcode = %s)
    """, (barcode,))

    commit("""
        UPDATE p320_24.tool SET shareable = True WHERE barcode = %s 
    """, (barcode,))

    commit("""
        UPDATE p320_24.request SET status = 'Finished' WHERE barcode = %s
    """)
