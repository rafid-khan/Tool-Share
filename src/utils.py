import os

import yaml
from psycopg2 import connect
from sshtunnel import SSHTunnelForwarder, HandlerSSHTunnelForwarderError


def get_config():
    yml_path = os.path.join(os.path.dirname(__file__), '../db-cfg.yml')
    with open(yml_path, 'r') as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)

        return cfg


def start_server():
    cfg = get_config()

    server_params = {
        'ssh_address_or_host': (cfg['remote_host'], cfg['remote_port']),
        'ssh_username': cfg['user'],
        'ssh_password': cfg['pass'],
        'remote_bind_address': (cfg['host'], cfg['port'])
    }

    try:
        with SSHTunnelForwarder(**server_params) as tunnel:

            server = tunnel.start()

            print('SSH tunnel established')

            return server

    except HandlerSSHTunnelForwarderError as err:
        print('Connection failed', err)


def get_conn():
    cfg = get_config()

    db_params = {
        'database': cfg['database'],
        'user': cfg['user'],
        'password': cfg['pass'],
        'host': cfg['host'],
        'port': cfg['port']
    }

    conn = connect(**db_params)
    cur = conn.cursor()

    print('Database connection established')

    return cur
