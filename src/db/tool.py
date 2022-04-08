from psycopg2.sql import SQL, Identifier

from .utils import fetch_many, fetch_one, commit

from src.api.utils import SortType


def fetch_tool(code):
    return fetch_one("""
        SELECT * FROM p320_24.tool WHERE barcode = %s
    """, (code,))


def fetch_all_tools(sort: SortType):
    return fetch_many("""
        SELECT * FROM p320_24.tool ORDER BY name %s
    """, (sort.value,)) if sort else fetch_many("""
        SELECT * FROM p320_24.tool
    """)


def fetch_available_tools():
    return fetch_many("""
        SELECT * FROM p320_24.tool WHERE shareable = true
    """)


def insert_tool(**kwargs):
    commit("""
        INSERT INTO p320_24.tool (barcode, category, shareable, name, description) VALUES (%s, %s, %s, %s, %s)
    """, (tuple(kwargs.values())))


def update_tool(code, **kwargs):
    query = SQL("UPDATE p320_24.tool SET ({}) = %s WHERE barcode = %s") \
        .format(SQL(', ').join(map(Identifier, list(kwargs.keys()))))

    commit(query, (tuple(kwargs.values()), code))


def view_user_tools(username):
    return fetch_many("""
        SELECT name FROM p320_24.tool WHERE holder = %s,
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
