import datetime

from psycopg2.sql import SQL, Identifier

from .utils import fetch_one, fetch_many, commit


# WORKS
def create_request(**kwargs):
    commit("""
            INSERT INTO p320_24.request (request_id, username, barcode, status, 
            borrow_period, request_date, owner_expected_date, actual_return_date) 
            VALUES (%s, %s, %s, 'Pending', %s, %s, %s, null)
        """, (tuple(kwargs.values())))


def get_request(request_id):
    return fetch_one("""
    Select p320_24.request.request_id
    FROM p320_24.request
    WHERE p320_24.request.request_id = %s 
    """, (request_id,))


# WORKS
def get_users_requests_received(username):
    return fetch_many("""
        SELECT * 
        FROM p320_24.request
        WHERE barcode IN
        (SELECT barcode FROM p320_24.ownership WHERE p320_24.ownership.username = %s)
    """, (username,))


# WORKS
def get_users_requests_made(username):
    return fetch_many("""
        SELECT p320_24.request.request_id, p320_24.request.request_date,
        p320_24.request.owner_expected_date, p320_24.ownership.username
        FROM p320_24.request 
        INNER JOIN p320_24.ownership
        ON p320_24.request.barcode = p320_24.ownership.barcode
        WHERE p320_24.request.username = %s 
    """, (username,))


def handle_requests(is_accepted, request_id, actual_return_date):
    if is_accepted:
        commit("""
            UPDATE p320_24.request 
            SET status = 'Accepted',
                actual_return_date = %s
             WHERE request_id = %s 
        """, (actual_return_date, request_id, ))

        commit("""
            UPDATE p320_24.tool 
            SET shareable = False 
            WHERE barcode IN 
            (SELECT barcode FROM p320_24.request WHERE request_id = %s)
        """, (request_id,))

        commit("""
            UPDATE p320_24.tool
            SET holder = p320_24.request.username
            FROM p320_24.request
            WHERE p320_24.tool.barcode = p320_24.request.barcode
            AND p320_24.request.request_id = %s
        """, (request_id,))

    else:
        commit("""
            UPDATE p320_24.request 
            SET status = 'DENIED' 
            WHERE request_id = %s
        """, (request_id,))


def return_tool(barcode):
    commit("""
        
UPDATE p320_24.tool
        SET holder = p320_24.ownership.username
        FROM p320_24.ownership
        WHERE p320_24.ownership.barcode = %s
        AND p320_24.tool.barcode = p320_24.ownership.barcode;
    """, (barcode,))

    commit("""
        UPDATE p320_24.tool 
        SET shareable = True 
        WHERE barcode = %s 
    """, (barcode,))

    commit("""
        UPDATE p320_24.request 
        SET p320_24.request.status = 'Finished'
        AND actual_return_date = now()
        WHERE barcode = %s
    """, (barcode,))
