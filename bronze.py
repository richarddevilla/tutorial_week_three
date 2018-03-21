import sqlite3
from os import path

BASE_DIR = path.dirname(path.abspath(__file__))
DB_PATH = path.join(BASE_DIR, 'test_profile.db')
SCHEMA_PATH = path.join(BASE_DIR, 'sqlite_schema.sql')


def create_table():
    with sqlite3.connect(DB_PATH) as conn:
        with open(SCHEMA_PATH, 'rt') as f:
            schema = f.read()
        conn.executescript(schema)
        print('Table created!')


if __name__ == '__main__':
    if not path.exists(DB_PATH): create_table()



