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
    string_to_fetch = """
        SELECT p320_24.tool.*
        FROM p320_24.tool
        INNER JOIN p320_24.category
        ON p320_24.category.barcode = p320_24.tool.barcode 
        ORDER BY 
        """
    string_to_fetch += group.value + order.value
    return fetch_many(string_to_fetch)


def search_tool(identifier, keyword, order: SortBy, group: SortType):
    if identifier == "Name":
        string_to_fetch = """
           SELECT p320_24.tool.*
           FROM p320_24.tool
           WHERE p320_24.tool.name LIKE (\'%"""
        string_to_fetch += keyword + "%\')\nORDER BY "
        string_to_fetch += group.value + order.value

        return fetch_many(string_to_fetch)
    elif identifier == "Category":
        string_to_fetch = """
           SELECT p320_24.tool.*
           FROM p320_24.tool
           INNER JOIN p320_24.category
           ON p320_24.tool.barcode = p320_24.category.barcode
           WHERE p320_24.category.tag_name LIKE (\'%"""
        string_to_fetch += keyword + "%\')\nORDER BY "
        string_to_fetch += group.value + order.value
        return fetch_many(string_to_fetch)
    elif identifier == "Barcode":
        string_to_fetch = """
           SELECT p320_24.tool.*
           FROM p320_24.tool
           WHERE p320_24.tool.barcode LIKE (\'%"""
        string_to_fetch += keyword + "%\')\nORDER BY "
        string_to_fetch += group.value + order.value
        return fetch_many(string_to_fetch)
    else:
        Exception(ValueError)


def insert_tool(**kwargs):
    commit("""
        INSERT INTO p320_24.tool (barcode, shareable, name, description, holder) 
        VALUES (%s, %s, %s, %s, %s)
    """, (tuple(kwargs.values())))


def create_category(**kwargs):
    commit("""
        INSERT INTO category (tag_name, barcode) 
        VALUES (%s, %s)
    """, (tuple(kwargs.values())))


def fetch_category(barcode):
    return fetch_many("""
        SELECT p320_24.category.tag_name
        FROM p320_24.category
        WHERE p320_24.category.barcode = %s
    """, (barcode,))


def update_tool_description(description, code):
    string_to_update = "UPDATE p320_24.tool SET description = %s WHERE barcode = %s"

    commit(string_to_update, (description, code, ))


def update_tool_name(name, code):
    string_to_update = "UPDATE p320_24.tool SET name = %s WHERE barcode = %s"

    commit(string_to_update, (name, code, ))


def update_tool_sharable(sharable, code):
    string_to_update = "UPDATE p320_24.tool SET shareable = %s WHERE barcode = %s"
    commit(string_to_update, (sharable, code,))


def view_user_tools(username, order: SortBy, group: SortType):
    string_to_fetch = """
        SELECT p320_24.tool.*, 
        p320_24.ownership.username
        FROM p320_24.tool
        INNER JOIN p320_24.ownership
        ON p320_24.tool.barcode = p320_24.ownership.barcode
        WHERE holder = %s OR p320_24.ownership.username = %s
        ORDER BY
    """
    string_to_fetch += group.value + order.value
    return fetch_many(string_to_fetch, (username, username,))


def search_user_tools(identifier, keyword, username, order: SortBy, group: SortType):
    if identifier == "Name":
        string_to_fetch = """
                        SELECT p320_24.tool.*, 
                        p320_24.ownership.username
                        FROM p320_24.tool
                        INNER JOIN p320_24.ownership
                        ON p320_24.tool.barcode = p320_24.ownership.barcode
                        WHERE ( holder = """
        string_to_fetch += " '" + username + "' " + "OR p320_24.ownership.username = "
        string_to_fetch += " '" + username + "' ) " + "AND p320_24.tool.name LIKE (\'%"
        string_to_fetch += keyword + "%\')\nORDER BY "
        string_to_fetch += group.value + order.value
        return fetch_many(string_to_fetch)
    elif identifier == "Category":
        string_to_fetch = """
                        SELECT p320_24.tool.*, 
                        p320_24.ownership.username
                        FROM p320_24.tool
                        INNER JOIN p320_24.ownership
                        ON p320_24.tool.barcode = p320_24.ownership.barcode
                        INNER JOIN p320_24.category
                        ON p320_24.ownership.barcode = p320_24.category.barcode
                        WHERE ( p320_24.tool.holder = """
        string_to_fetch += " '" + username + "' " + "OR p320_24.ownership.username = "
        string_to_fetch += " '" + username + "' ) " + "AND p320_24.category.tag_name LIKE (\'%"
        string_to_fetch += keyword + "%\')\nORDER BY "
        string_to_fetch += group.value + order.value
        print(string_to_fetch)
    if identifier == "Barcode":
        string_to_fetch = """
                        SELECT p320_24.tool.*, 
                        p320_24.ownership.username
                        FROM p320_24.tool
                        INNER JOIN p320_24.ownership
                        ON p320_24.tool.barcode = p320_24.ownership.barcode
                        WHERE ( p320_24.tool.holder = """
        string_to_fetch += " '" + username + "' " + "OR p320_24.ownership.username = "
        string_to_fetch += " '" + username + "' )" + "AND p320_24.tool.barcode LIKE (\'%"
        string_to_fetch += keyword + "%\')\nORDER BY "
        string_to_fetch += group.value + order.value
        print(string_to_fetch)
        return fetch_many(string_to_fetch)
    else:
        Exception(ValueError)


def fetch_available_tools(order: SortBy, group: SortType):
    string_to_fetch = """
        SELECT p320_24.tool.* 
        FROM p320_24.tool
        INNER JOIN p320_24.category
        ON p320_24.category.barcode = p320_24.tool.barcode 
        WHERE shareable = true
        ORDER BY
    """
    string_to_fetch += group.value + order.value
    return fetch_many(string_to_fetch)


def fetch_users_lent_tools(username):
    return fetch_many("""
        SELECT p320_24.tool.barcode, p320_24.tool.name,
        p320_24.request.request_date, p320_24.tool.holder,
        p320_24.request.owner_expected_date, p320_24.tool.description
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


def fetch_users_borrowed_tools(username):
    return fetch_many("""
        SELECT p320_24.tool.barcode, p320_24.tool.name, 
        p320_24.request.request_date, p320_24.ownership.username,
        p320_24.request.owner_expected_date, p320_24.tool.description
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
        p320_24.request.request_date, p320_24.tool.holder,
        p320_24.request.owner_expected_date, p320_24.tool.description
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


def fetch_overdue_borrowed_tools(username):
    return fetch_many("""
        SELECT p320_24.tool.barcode, p320_24.tool.name,
        p320_24.request.request_date, p320_24.ownership.username,
        p320_24.request.owner_expected_date, p320_24.tool.description
        FROM p320_24.tool
        INNER JOIN p320_24.request
        ON p320_24.tool.barcode = p320_24.request.barcode
        INNER JOIN p320_24.ownership
        ON p320_24.request.barcode = p320_24.ownership.barcode
        WHERE p320_24.request.owner_expected_date < now()
        AND status = 'Accepted'
        AND p320_24.tool.holder = %s
        ORDER BY p320_24.request.request_date
    """, (username,))


def delete_tool(barcode):
    users = fetch_one("""
                SELECT p320_24.tool.holder, p320_24.ownership.username
                FROM p320_24.tool
                INNER JOIN p320_24.ownership
                ON p320_24.tool.barcode = p320_24.ownership.barcode
                WHERE p320_24.tool.barcode = %s
    """, (barcode, ))
    print(users['holder'])
    print(users['username'])

    if users['holder'] == users['username']:

        commit("""
                DELETE
                FROM p320_24.request
                WHERE barcode = %s
        """, (barcode,))

        commit("""
                DELETE
                FROM p320_24.ownership
                WHERE barcode = %s
            """, (barcode,))

        commit("""
                DELETE 
                FROM p320_24.category
                WHERE barcode = %s 
        """, (barcode, ))

        commit("""
                DELETE
                FROM p320_24.tool
                WHERE barcode = %s
        """, (barcode,))

