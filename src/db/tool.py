from psycopg2.sql import SQL, Identifier

from .utils import fetch_many, fetch_one, commit

from src.api.utils import SortType, SortBy


def fetch_tool(code):
    return fetch_one("""
        SELECT p320_24.tool.* 
        FROM p320_24.tool
        WHERE barcode = %s  
    """, (code,))


def fetch_all_tools(order: SortBy, group: SortType):
    return fetch_many("""
        SELECT p320_24.tool.* 
        FROM p320_24.tool
        ORDER BY %s %s
    """, (group.value, order.value,))


def search_tool(identifier, keyword, order: SortBy, group: SortType):
    if identifier == "name":
        commit("""
           SELECT p320_24.tool.*
           FROM p320_24.tool
           WHERE p320_24.tool.name LIKE ('%' + %s + '%')
           ORDER BY %s %s 
        """, (keyword, group.value, order.value))
    elif identifier == "category":
        commit("""
           SELECT p320_24.tool.*
           FROM p320_24.tool
           INNER JOIN p320_24.category
           ON p320_24.tool.barcode = p320_24.category.barcode
           WHERE p320_24.category.tag_name LIKE ('%' + %s + '%')
           ORDER BY %s %s  
        """, (keyword, group.value, order.value,))
    elif identifier == "barcode":
        commit("""
           SELECT p320_24.tool.*
           FROM p320_24.tool
           WHERE p320_24.tool.barcode LIKE ('%' + %s + '%')
           ORDER BY %s %s  
        """, (keyword, group.value, order.value,))
    else:
        Exception(ValueError)


def insert_tool(**kwargs):
    commit("""
        INSERT INTO p320_24.tool (barcode, category, shareable, name, description) 
        VALUES (%s, %s, %s, %s, %s)
    """, (tuple(kwargs.values())))


def create_category(**kwargs):
    commit("""
        INSERT INTO category (tag_name, barcode, username) 
        VALUES (%s, %s, %s)
    """, (tuple(kwargs.values())))


def fetch_category(barcode):
    fetch_many("""
        SELECT tag_name
        FROM p320_24.category
        WHERE barcode = %s
    """, (barcode,))


def update_tool(code, **kwargs):
    query = SQL("UPDATE p320_24.tool SET ({}) = %s WHERE barcode = %s") \
        .format(SQL(', ').join(map(Identifier, list(kwargs.keys()))))

    commit(query, (tuple(kwargs.values()), code))


def view_user_tools(username, order: SortBy, group: SortType):
    return fetch_many("""
        SELECT p320_24.tool.*, 
        p320_24.ownership.username
        FROM p320_24.tool
        INNER JOIN p320_24.ownership
        ON p320_24.tool.barcode = p320_24.ownership.barcode
        WHERE holder = %s OR p320_24.ownership.username = %s
        ORDER BY %s %s
    """, (username, order.value, group.value))


def fetch_available_tools(order: SortBy, group: SortType):
    return fetch_many("""
        SELECT p320_24.tool.* 
        FROM p320_24.tool
        WHERE shareable = true
        ORDER BY %s %s
    """, (order.value, group.value))


def fetch_users_lent_tools(username, ):
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


def fetch_user_borrowed_tools(username, ):
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


def fetch_overdue_lent_tools(username, ):
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
        WHERE p320_24.request.owner_expected_date > now()
        AND status = 'Accepted'
        ORDER BY p320_24.request.request_date
    """, (username,))


def fetch_overdue_borrowed_tools(username, ):
    return fetch_many("""
        SELECT p320_24.tool.barcode, p320_24.tool.name,
        p320_24.request.request_date, p320_24.ownership.username
        FROM p320_24.request
        INNER JOIN p320_24.ownership
        ON p320_24.request.barcode = p320_24.ownership.barcode
        WHERE p320_24.request.owner_expected_date > now()
        AND status = 'Accepted'
        AND p320_24.tool.holder = %s
        ORDER BY p320_24.request.request_date
    """, (username,))


def delete_tool(barcode):
    commit("""
        DELETE
        FROM p320_24.request
        WHERE EXISTS 
            (SELECT * 
             FROM p320_24.tool
             WHERE p320_24.request.barcode = p320_24.tool.barcode
             AND p320_24.tool.barcode = %s)
    """, (barcode,))

    commit("""
        DELETE
        FROM p320_24.tool 
        USING p320_24.ownership
        WHERE p320_24.tool.barcode = %s
        AND p320_24.tool.barcode = p320_24.ownership.barcode
    """, (barcode,))

    commit("""
        DELETE
        FROM p320_24.ownership
        WHERE barcode = %s
    """, (barcode,))
