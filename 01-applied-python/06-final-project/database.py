

import os

import psycopg2


def postgres_connection():
    """Return an autocommit connection; the caller is responsible for closing it."""
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )
    conn.autocommit = True
    return conn
