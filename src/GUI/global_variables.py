username = "Aaron9932"
curs = None
conn = None


def set_conn(init_conn):
    global conn
    conn = init_conn


def set_curs(init_cursor):
    global curs
    curs = init_cursor


def set_username(init_username):
    global username
    username = init_username


