import os

import psycopg2
import yaml
from psycopg2.extras import RealDictCursor
from sshtunnel import SSHTunnelForwarder, HandlerSSHTunnelForwarderError
import GUI.global_variables as gbl_var



DB_CFG = os.path.join(os.path.dirname(__file__), '../../db-cfg.yml')
LOCAL_PORT = 5432


def get_config():
    with open(DB_CFG, 'r') as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)
        return cfg


def create_server():
    cfg = get_config()

    server_params = {
        'ssh_address_or_host': (cfg['remote_host'], cfg['remote_port']),
        'ssh_username': cfg['user'],
        'ssh_password': cfg['pass'],
        'remote_bind_address': (cfg['host'], LOCAL_PORT)
    }

    try:
        server = SSHTunnelForwarder(**server_params)
        server.start()

        return cfg, server

    except HandlerSSHTunnelForwarderError as err:
        print('Connection failed', err)


def connect():
    cfg, server = create_server()
    print("SSH tunnel established")
    db_params = {
        'database': cfg['database'],
        'user': cfg['user'],
        'password': cfg['pass'],
        'host': 'localhost',
        'port': server.local_bind_port,
        'options': f'-c search_path={cfg["schema"]}'
    }

    return psycopg2.connect(**db_params)


def fetch_one(sql, args=None):
    gbl_var.curs.execute(sql, args)
    one = gbl_var.curs.fetchone()

    return one


def fetch_many(sql, args=None):
    gbl_var.curs.execute(sql, args)
    list_of_tuples = gbl_var.curs.fetchall()

    return list_of_tuples


def commit(sql, args=None):
    result = gbl_var.curs.execute(sql, args)
    gbl_var.conn.commit()

    return result


def row_count(sql, args=None):
    gbl_var.curs.execute(sql, args)
    gbl_var.conn.commit()


    return cur.rowcount
