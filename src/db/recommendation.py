from psycopg2.sql import SQL, Identifier

from .utils import fetch_many, fetch_one, commit

from src.api.utils import SortType, SortBy


# AFTER A USER MADE A BORROW REQUEST THE APPLICATION MUST RECOMMEND OTHER TOOLS
# GIVEN A REQUEST.BARCODE -> GET THE TOOLS NAME -> GET ALL THE PEOPLE THAT BORROWED THE SAME TOOL
# -> OUT OF THIS GROUP FIND THE PERSON THAT HAS THE MOST ACCEPTED REQUESTS -> GET THREE TOOL NAMES THAT
# THE USER ALSO BORROWED
# RETURN A TOOL WHERE TOOL.SHAREABLE = TRUE


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
    """, (barcode,))

    i = 0
    name = []
    for user_tool in get_top:
        name[i] = user_tool['name']
        i += 1

    result = ()
    for names in name:
        result.__add__(fetch_one("""
            SELECT p320_24.tool.barcode, name,
            description, p320_24.category.tag_name
            FROM p320_24.tool
            INNER JOIN p320_24.category
            ON p320_24.tool.barcode = p320_24.category.barcode
            WHERE name = %s
            AND shareable = true
            LIMIT 1
        """, (name[names])))

    return result


# TOP 10 MOST FREQUENTLY LENT TOOLS PERCENTAGE OF TIME LENT VS AVAILABLE AND
# AVERAGE LENT TIME
def top_lent_tools():
    pass


# TOP 10 MOST FREQUENTLY BORROWED TOOLS
def top_borrowed_tools():
    pass

