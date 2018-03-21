import mysql.connector

SCHEMA_PATH = 'mysql_schema.txt'
mysql_conn = mysql.connector.connect(
    user='richard',
    password='password',
    host='35.189.34.179')
mysql_cursor = mysql_conn.cursor()
with open(SCHEMA_PATH, 'rt') as f:
    schema = f.read()
    try:
        mysql_cursor.execute(schema)
    except Exception:
        mysql_cursor.execute(schema,multi=True)
mysql_conn.close()
