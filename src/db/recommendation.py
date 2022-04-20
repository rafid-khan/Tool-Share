from psycopg2.sql import SQL, Identifier

from .utils import fetch_many, fetch_one, commit


def also_borrowed(barcode):
    get_top = fetch_many("""
    SELECT p320_24.tool.name, COUNT("p320_24".tool.name) AS "count"
    FROM p320_24.request
    INNER JOIN p320_24.tool
    ON p320_24.tool.barcode = p320_24.request.barcode
    WHERE username IN (
    SELECT username
    FROM p320_24.request
    INNER JOIN p320_24.tool
    ON p320_24.tool.barcode = p320_24.request.barcode
    WHERE p320_24.tool.name IN(
    SELECT p320_24.tool.name
    FROM p320_24.tool
    WHERE barcode = %s))
    AND p320_24.tool.name NOT IN (
    SELECT p320_24.tool.name
    FROM p320_24.tool
    WHERE barcode = %s)
    GROUP BY p320_24.tool.name
    ORDER BY count DESC
    LIMIT 3
    """, (barcode, barcode, ))

    name_list = []
    for user_tool in get_top:
        name_list.append(user_tool['name'])

    result = []
    for name in name_list:
        result.append(fetch_one("""
            SELECT p320_24.tool.barcode, p320_24.tool.name
            FROM p320_24.tool
            WHERE name = %s
            AND shareable = true
            LIMIT 1
        """, (name, )))

    return result


def top_lent_tools(username):
    print(username)

    result = fetch_many("""
        SELECT p320_24.tool.name, AVG(p320_24.request.borrow_period)
        AS "Average_lent_time"
        FROM p320_24.tool
        INNER JOIN p320_24.request
        ON p320_24.request.barcode = p320_24.tool.barcode
        WHERE p320_24.tool.name IN (
            SELECT p320_24.tool.name
            FROM p320_24.tool
            INNER JOIN p320_24.ownership
            ON p320_24.tool.barcode = p320_24.ownership.barcode
            AND p320_24.tool.holder != p320_24.ownership.username
            AND p320_24.ownership.username = %s
        )
        GROUP BY p320_24.tool.name
        ORDER BY "Average_lent_time" DESC
        LIMIT 10
    """, (username,))
    print(result)
    return result

def top_borrowed_tools(username):
    return fetch_many("""
        SELECT p320_24.tool.name, AVG(p320_24.request.borrow_period)
        AS "Average_borrowed_time"
        FROM p320_24.tool
        INNER JOIN p320_24.request
        ON p320_24.request.barcode = p320_24.tool.barcode
        WHERE p320_24.tool.name IN (
            SELECT p320_24.tool.name
            FROM p320_24.tool
            INNER JOIN p320_24.ownership
            ON p320_24.tool.barcode = p320_24.ownership.barcode
            AND p320_24.tool.holder != p320_24.ownership.username
            AND p320_24.tool.holder = %s
        )
        GROUP BY p320_24.tool.name
        ORDER BY "Average_borrowed_time" DESC
        LIMIT 10
    """, (username,))


def pie_chart(username):
    total = fetch_many("""
        SELECT COUNT(p320_24.tool.name) AS total
        FROM p320_24.tool
        INNER JOIN p320_24.ownership
        ON p320_24.tool.barcode = p320_24.ownership.barcode
        WHERE holder = %s OR p320_24.ownership.username = %s
    """, (username, username,))

    lent = fetch_many("""
        SELECT COUNT(p320_24.tool.name) AS total
        FROM p320_24.tool
        INNER JOIN p320_24.ownership
        ON p320_24.tool.barcode = p320_24.ownership.barcode
        AND p320_24.tool.holder != p320_24.ownership.username
        AND p320_24.ownership.username = %s
        INNER JOIN p320_24.request
        ON p320_24.tool.barcode = p320_24.request.barcode
    """, (username,))

    borrowed = fetch_many("""
        SELECT COUNT(p320_24.tool.name) AS total 
        FROM p320_24.tool
        INNER JOIN p320_24.ownership
        ON p320_24.tool.barcode = p320_24.ownership.barcode
        AND p320_24.tool.holder != p320_24.ownership.username
        AND p320_24.tool.holder = %s
        INNER JOIN p320_24.request
        ON p320_24.tool.barcode = p320_24.request.barcode
    """, (username, ))

    result = total + lent + borrowed

    return result


def latest_requests():
    return fetch_many("""
        SELECT p320_24.request.request_id, p320_24.tool.name,
        p320_24.request.barcode, p320_24.ownership.username
        FROM p320_24.request
        INNER JOIN p320_24.tool
        ON p320_24.tool.barcode = p320_24.request.barcode
        INNER JOIN p320_24.ownership
        ON p320_24.request.barcode = p320_24.ownership.barcode
        LIMIT 3
    """)

