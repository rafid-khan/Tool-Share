from psycopg2.sql import SQL, Identifier

from api.utils import SortType
from .utils import fetch_many, fetch_one, commit


def fetch_tool(code):
    return fetch_one("""
        SELECT * FROM ts_tool WHERE barcode = %s
    """, (code,))


def fetch_all_tools(sort: SortType):
    return fetch_many("""
        SELECT * FROM ts_tool ORDER BY name %s
    """, (sort.value,)) if sort else fetch_many("""
        SELECT * FROM ts_tool
    """)


# TODO: Test
def fetch_available_tools():
    return fetch_many("""
        SELECT * FROM ts_tool WHERE shareable = true
    """)


def insert_tool(**kwargs):
    commit("""
        INSERT INTO ts_tool (barcode, category, shareable, name, description) VALUES (%s, %s, %s, %s, %s)
    """, (tuple(kwargs.values())))


def update_tool(code, **kwargs):
    query = SQL("UPDATE ts_tool SET ({}) = %s WHERE barcode = %s") \
        .format(SQL(', ').join(map(Identifier, list(kwargs.keys()))))

    commit(query, (tuple(kwargs.values()), code))


def delete_tool(code):
    commit("""
        DELETE FROM ts_tool WHERE barcode = %s
    """, (code,))
