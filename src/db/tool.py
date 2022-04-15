from psycopg2.sql import SQL, Identifier

from .utils import fetch_many, fetch_one, commit

from src.api.utils import SortType


# WORKS
def fetch_tool(code):
    return fetch_one("""
        SELECT p320_24.tool.* 
        FROM p320_24.tool
        WHERE barcode = %s  
    """, (code,))


def fetch_all_tools(sort: SortType,):
    return fetch_many("""
        SELECT p320_24.tool.*, p320_24.category.tag_name 
        FROM p320_24.tool
        INNER JOIN p320_24.category 
        ON p320_24.tool.barcode = p320_24.category.barcode
        ORDER BY p320_24.tool.name %s
    """, (sort.value,)) \
        if sort else \
        fetch_many("""
        SELECT p320_24.tool.*, p320_24.category.tag_name 
        FROM p320_24.tool
        INNER JOIN p320_24.category 
        ON p320_24.tool.barcode = p320_24.category.barcode
    """)


def search_tool(identifier, keyword):
    if identifier == "name":
        commit("""
           SELECT p320_24.tool.*, p320_24.category.tag_name
           FROM p320_24.tool
           INNER JOIN p320_24.category
           ON p320_24.tool.barcode = p320_24.category.barcode
           WHERE p320_24.tool.name LIKE ('%' + %s + '%')
           ORDER BY p320_24.tool.name 
        """, (keyword,))
    elif identifier == "category":
        commit("""
           SELECT p320_24.tool.*, p320_24.category.tag_name
           FROM p320_24.tool
           INNER JOIN p320_24.category
           ON p320_24.tool.barcode = p320_24.category.barcode
           WHERE p320_24.category.tag_name LIKE ('%' + %s + '%')
           ORDER BY p320_24.tool.name 
        """, (keyword,))
    elif identifier == "barcode":
        commit("""
           SELECT p320_24.tool.*, p320_24.category.tag_name
           FROM p320_24.tool
           INNER JOIN p320_24.category
           ON p320_24.tool.barcode = p320_24.category.barcode
           WHERE p320_24.tool.barcode LIKE ('%' + %s + '%')
           ORDER BY p320_24.tool.name 
        """, (keyword,))
    else:
        Exception(ValueError)


def insert_tool(**kwargs):
    commit("""
        INSERT INTO p320_24.tool (barcode, shareable, name, description, holder) 
        VALUES (%s, %s, %s, %s, %s)
    """, (tuple(kwargs.values())))


def create_category(**kwargs):
    commit("""
        INSERT INTO category (tag_name, barcode, username) 
        VALUES (%s, %s, %s)
    """, (tuple(kwargs.values())))


def update_tool(code, **kwargs):
    query = SQL("UPDATE p320_24.tool SET ({}) = %s WHERE barcode = %s") \
        .format(SQL(', ').join(map(Identifier, list(kwargs.keys()))))

    commit(query, (tuple(kwargs.values()), code))


# WORKS
def view_user_tools(username):
    return fetch_many("""
        SELECT p320_24.tool.*, p320_24.ownership.username
        FROM p320_24.tool
        INNER JOIN p320_24.ownership
        ON p320_24.tool.barcode = p320_24.ownership.barcode
        WHERE holder = %s OR p320_24.ownership.username = %s
        ORDER BY p320_24.tool.name ASC
    """, (username, username))


def view_tool_category(barcode):
    return fetch_many("""
    SELECT p320_24.category.tag_name
    FROM p320_24.category
    WHERE p320_24.category.barcode = %s
    """, (barcode,))


def fetch_available_tools():
    return fetch_many("""
        SELECT p320_24.tool.*, p320_24.category.tag_name 
        FROM p320_24.tool
        WHERE shareable = true
        ORDER BY p320_24.tool.name ASC
    """)


def fetch_users_lent_tools(username):
    return fetch_many("""
        SELECT p320_24.tool.barcode, p320_24.tool.name,
        p320_24.request.owner_expected_date, p320_24.tool.holder,
        p320_24.tool.description
        FROM p320_24.tool
        INNER JOIN p320_24.ownership
        ON p320_24.tool.barcode = p320_24.ownership.barcode
        AND p320_24.tool.holder != p320_24.ownership.username
        AND p320_24.ownership.username = %s
        INNER JOIN p320_24.request
        ON p320_24.tool.barcode = p320_24.request.barcode
        WHERE p320_24.request.owner_expected_date > now()
        ORDER BY p320_24.request.request_date
    """, (username,))


# WORKS
def fetch_users_borrowed_tools(username):
    return fetch_many("""
        SELECT p320_24.tool.barcode, p320_24.tool.name, 
        p320_24.request.owner_expected_date, p320_24.ownership.username,
        p320_24.tool.description
        FROM p320_24.tool
        INNER JOIN p320_24.ownership
        ON p320_24.tool.barcode = p320_24.ownership.barcode
        AND p320_24.tool.holder != p320_24.ownership.username
        AND p320_24.tool.holder = %s
        INNER JOIN p320_24.request
        ON p320_24.tool.barcode = p320_24.request.barcode
        WHERE p320_24.request.owner_expected_date > now()
        ORDER BY p320_24.request.request_date
    """, (username,))


def fetch_overdue_lent_tools(username):
    return fetch_many("""
        SELECT p320_24.tool.barcode, p320_24.tool.name,
        p320_24.request.owner_expected_date, p320_24.tool.holder,
        p320_24.tool.description
        FROM p320_24.tool
        INNER JOIN p320_24.ownership
        ON p320_24.tool.barcode = p320_24.ownership.barcode
        AND p320_24.tool.holder != p320_24.ownership.username
        AND p320_24.ownership.username = %s
        INNER JOIN p320_24.request
        ON p320_24.tool.barcode = p320_24.request.barcode
        WHERE p320_24.request.owner_expected_date < now()
        AND status = 'Accepted'
        ORDER BY p320_24.request.request_date
    """, (username,))


# NEEDS TO BE UPDATED TO REFLECT CHANGES IN THE REQUEST TABLE
def fetch_overdue_borrowed_tools(username):
    return fetch_many("""
        SELECT p320_24.tool.barcode, p320_24.tool.name, 
        p320_24.request.owner_expected_date, p320_24.ownership.username, 
        p320_24.tool.description
        FROM p320_24.request
        INNER JOIN p320_24.ownership
        ON p320_24.request.barcode = p320_24.ownership.barcode
        INNER JOIN p320_24.tool
        on p320_24.request.barcode = p320_24.tool.barcode
        WHERE p320_24.request.owner_expected_date < now()
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
        AND p320_24.tool.holder = p320_24.ownership.username
    """, (barcode,))

    commit("""
        DELETE
        FROM p320_24.ownership
        WHERE barcode = %s
    """, (barcode,))
    print("ownership")
