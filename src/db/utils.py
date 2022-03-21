import os

import psycopg2
import yaml
from psycopg2.extras import RealDictCursor
from sshtunnel import SSHTunnelForwarder, HandlerSSHTunnelForwarderError

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

        cfg['port'] = server.local_bind_port

        # Write local bind port back to database config
        with open(DB_CFG, 'w') as file:
            yaml.dump(cfg, file)

        return server

    except HandlerSSHTunnelForwarderError as err:
        print('Connection failed', err)


def connect():
    cfg = get_config()

    db_params = {
        'database': cfg['database'],
        'user': cfg['user'],
        'password': cfg['pass'],
        'host': cfg['host'],
        'port': cfg['port'],
        'options': f'-c search_path={cfg["schema"]}'
    }

    return psycopg2.connect(**db_params)


def fetch_one(sql, args=None):
    conn = connect()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql, args)
    one = cur.fetchone()
    conn.close()

    return one


def fetch_many(sql, args=None):
    conn = connect()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql, args)
    list_of_tuples = cur.fetchall()
    conn.close()

    return list_of_tuples


def commit(sql, args=None):
    conn = connect()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    result = cur.execute(sql, args)
    conn.commit()
    conn.close()

    return result


def row_count(sql, args=None):
    conn = connect()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql, args)
    conn.commit()
    conn.close()

    return cur.rowcount
