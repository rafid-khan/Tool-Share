from GUI import sign_in
from db import utils
from psycopg2.extras import RealDictCursor
import GUI.global_variables as gbl_var


def main():
    conn = utils.connect()
    curs = conn.cursor(cursor_factory=RealDictCursor)
    gbl_var.set_curs(curs)
    gbl_var.set_conn(conn)
    sign_in.main()


if __name__ == '__main__':
    main()
