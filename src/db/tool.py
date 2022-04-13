from psycopg2.sql import SQL, Identifier

from .utils import fetch_many, fetch_one, commit

from src.api.utils import SortType


# WORKS
def fetch_tool(code):
    return fetch_one("""
        SELECT * FROM p320_24.tool WHERE barcode = %s  
    """, (code,))


# WORKS
def fetch_all_tools(sort: SortType):
    return fetch_many("""
        SELECT * FROM p320_24.tool ORDER BY name %s
    """, (sort.value,)) if sort else fetch_many("""
        SELECT * FROM p320_24.tool
    """)


# We should consider making categories an attribute of tools
def fetch_all_tools_by_category(username):
    pass


# WORKS
def insert_tool(**kwargs):
    commit("""
        INSERT INTO p320_24.tool (barcode, category, shareable, name, description) 
        VALUES (%s, %s, %s, %s, %s)
    """, (tuple(kwargs.values())))


# WORKS
def update_tool(code, **kwargs):
    query = SQL("UPDATE p320_24.tool SET ({}) = %s WHERE barcode = %s") \
        .format(SQL(', ').join(map(Identifier, list(kwargs.keys()))))

    commit(query, (tuple(kwargs.values()), code))


# WORKS
def view_user_tools(username):
    return fetch_many("""
        SELECT * FROM p320_24.tool WHERE holder = %s,
    """, (username,))


# WORKS
def fetch_available_tools():
    return fetch_many("""
        SELECT * FROM p320_24.tool WHERE shareable = true
    """)


# WORKS
def fetch_users_lent_tools(username):
    return fetch_many("""
        SELECT p320_24.tool.barcode, p320_24.tool.name,
        p320_24.request.request_date, p320_24.tool.holder
        FROM p320_24.tool
        INNER JOIN p320_24.ownership
        ON p320_24.tool.barcode = p320_24.ownership.barcode
        AND p320_24.tool.holder != p320_24.ownership.username
        AND p320_24.ownership.username = %s
        INNER JOIN p320_24.request
        ON p320_24.tool.barcode = p320_24.request.barcode
        ORDER BY p320_24.request.request_date
    """, (username,))


# WORKS
def fetch_user_borrowed_tools(username):
    return fetch_many("""
        SELECT p320_24.tool.barcode, p320_24.tool.name, 
        p320_24.request.request_date, p320_24.ownership.username
        FROM p320_24.tool
        INNER JOIN p320_24.ownership
        ON p320_24.tool.barcode = p320_24.ownership.barcode
        AND p320_24.tool.holder != p320_24.ownership.username
        AND p320_24.tool.holder = %s
        INNER JOIN p320_24.request
        ON p320_24.tool.barcode = p320_24.request.barcode
        ORDER BY p320_24.request.request_date
    """, (username,))


# LGTM
def fetch_overdue_lent_tools(username):
    return fetch_many("""
        SELECT p320_24.tool.barcode, p320_24.tool.name,
        p320_24.request.request_date, p320_24.tool.holder
        FROM p320_24.tool
        INNER JOIN p320_24.ownership
        ON p320_24.tool.barcode = p320_24.ownership.barcode
        AND p320_24.tool.holder != p320_24.ownership.username
        AND p320_24.ownership.username = %s
        INNER JOIN p320_24.request
        ON p320_24.tool.barcode = p320_24.request.barcode
        ORDER BY p320_24.request.request_date
        WHERE (request_date + borrow_period) > now()
        AND status = 'Accepted'
    """, (username,))


# LGTM
def fetch_overdue_borrowed_tools(username):
    return fetch_many("""
        SELECT *
        FROM p320_24.request
        INNER JOIN p320_24.ownership
        ON p320_24.request.barcode = p320_24.ownership.barcode
        WHERE (request_date + borrow_period) < now()
        AND status = 'Accepted'
        AND p320_24.ownership.username = %s
    """, (username,))


# TODO
# how would we know if a tool is being lent out.
# lent out tools cannot be deleted so this function should contain a conditional
# statement that will tell you if deleting a tool is allowed
def delete_tool(code):
    commit("""
        DELETE FROM p320_24.tool WHERE barcode = %s
    """, (code,))


def create_category(**kwargs):
    commit("""
        INSERT INTO category (tag_name, barcode, username) 
        VALUES (%s, %s, %s)
    """, (tuple(kwargs.values())))
