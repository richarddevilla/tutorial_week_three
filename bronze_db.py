import mysql.connector
import sqlite3
import time
from faker import Faker
from os import path


BASE_DIR = path.dirname(path.abspath(__file__))
DB_PATH = path.join(BASE_DIR, 'profile.db')
SCHEMA_PATH = path.join(BASE_DIR, 'schema.sql')

TABLES = {}
TABLES['profile'] = (
    "CREATE TABLE `profile` ("
    "  `id` int(11) AUTO_INCREMENT,"
    "  `birth_date` date,"
    "  `first_name` varchar(30),"
    "  `last_name` varchar(30),"
    "  `phone_number1` varchar(30),"
    "  `phone_number2` varchar(30),"
    "  `address_id` int(11) REFERENCES `address`(`id`),"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")
TABLES['address'] = (
    "CREATE TABLE `address` ("
    "   `id`    int(11)  AUTO_INCREMENT,"
    "   `line1` varchar(100) DEFAULT '',"
    "   `street` varchar(100) DEFAULT '',"
    "   `suburb` varchar(100)  DEFAULT '',"
    "   `postcode` varchar(100) DEFAULT '',"
    "   `state` varchar(100) DEFAULT '',"
    "   `country` varchar(100) DEFAULT 'Australia',"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")
DB_NAME = 'profile'
mysqlconn = mysql.connector.connect(user='richard',
                                    password='password',
                                    host='35.189.34.179')
    #host='35.185.54.69')
mysqlcursor = mysqlconn.cursor()
sqliteconn = sqlite3.connect(DB_PATH)
sqlitec = sqliteconn.cursor()
fake_gen = Faker('en_AU')

def mysqlcreate_db():
    try:
        print('Checking if MySQL Database exist')
        mysqlcursor.execute('CREATE DATABASE {};'.format(DB_NAME))
        print('MySQL Database {} created!\n'.format(DB_NAME))
        mysqlconn.database = DB_NAME
        for name, ddl in TABLES.items():
            print("Creating table {}: \n".format(name), end='')
            mysqlcursor.execute(ddl)
    except Exception:
        mysqlconn.database = DB_NAME
        print('MySQL Database already exist')

def create_table():
    try:
        print('Checking if SQLite3 Database exist')
        with open(SCHEMA_PATH, 'rt') as f:
            schema = f.read()
            sqliteconn.executescript(schema)
        print('SQLite3 Database profile created!')
    except Exception:
        print('SQLite3 Database already exist')

def create_fakes(quantity):
    fakes = []
    for i in range(0,quantity):
        fake=(fake_gen.building_number(),
                        fake_gen.street_name(),
                        fake_gen.city(),
                        fake_gen.postcode(),
                        fake_gen.state_abbr(),
                        'Australia',
                        fake_gen.first_name(),
                        fake_gen.last_name(),
                        fake_gen.phone_number(),
                        fake_gen.phone_number(),
                        fake_gen.date_time_this_century(
                            before_now=True,
                            after_now=False,
                            tzinfo=None)
                 )
        fakes.append(fake)
    return fakes

def insert_fakes(entries):
    data = create_fakes(entries)
    start = time.clock()
    for each in data:
        sqlitecreate_entry(each)
    sqliteconn.commit()
    end = time.clock()
    print('Insert SQLite total time '+str(end-start))
    mysqlconn.database = DB_NAME
    start = time.clock()
    for each in data:
        mysqlcreate_entry(each)
    mysqlconn.commit()
    end = time.clock()
    print('Insert MySQL total time ' + str(end - start))

def sqlitecreate_entry(data):
        sqlitec.execute("""
                    INSERT INTO address(
                    'line1',
                    'street',
                    'suburb',
                    'postcode',
                    'state',
                    'country'
                    )
                    VALUES(
                      ?,?,?,?,?,?
                    )
                  """, (
                    data[0:6]
                    )
                        )
        sqlitec.execute("""
                    INSERT INTO profile(
                    'first_name',
                    'last_name',
                    'phone_number1',
                    'phone_number2',
                    'birth_date',
                    'address_id'
                    )
                    VALUES(
                      ?,?,?,?,?,LAST_INSERT_ROWID()
                    )
                  """, (
                    data[6:]
                    )
                        )

def mysqlcreate_entry(data):
        mysqlcursor.execute("""
                    INSERT INTO address(
                    `line1`,
                    `street`,
                    `suburb`,
                    `postcode`,
                    `state`
                    )
                    VALUES(
                      %s,%s,%s,%s,%s
                    )
                  """, (
                    data[0:5]
                    )
                        )
        mysqlcursor.execute("""
                    INSERT INTO profile(
                    `first_name`,
                    `last_name`,
                    `phone_number1`,
                    `phone_number2`,
                    `birth_date`,
                    `address_id`
                    )
                    VALUES(
                      %s,%s,%s,%s,%s,LAST_INSERT_ID()
                    )
                  """, (
                    data[6:]
                    )
                        )

def mysqlsearch_data(pattern):
    pattern = '%'+pattern+'%'
    mysqlconn.database = DB_NAME
    mysqlcursor.execute("""
                SELECT CONCAT_WS(' ',profile.first_name,profile.last_name),
                profile.phone_number1,
                profile.phone_number2,
                profile.birth_date,
                CONCAT_WS(' ',address.line1,
                address.street,
                address.suburb,
                address.postcode,
                address.state,
                address.country)
                FROM profile
                LEFT JOIN address ON  profile.address_id=address.id
                WHERE profile.first_name LIKE %s
                OR profile.last_name LIKE %s
                OR profile.phone_number1 LIKE %s
                OR profile.phone_number2 LIKE %s
                OR profile.birth_date LIKE %s
                OR address.line1 LIKE %s
                OR address.street LIKE %s
                OR address.suburb LIKE %s
                OR address.postcode LIKE %s
                OR address.state LIKE %s
                OR address.country LIKE %s;
              """,([pattern]*11)
              )
    result=[]
    for each in mysqlcursor.fetchall():
        result.append(each)
    print('MySQL Database searched!!')
    return result

def search_data(pattern):
    pattern = '%'+pattern+'%'
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
                    SELECT (profile.first_name || " " || profile.last_name),
                    profile.phone_number1,
                    profile.phone_number2,
                    profile.birth_date,
                    (address.line1 || " " ||
                    address.street || " " ||
                    address.suburb || " " ||
                    address.postcode || " " ||
                    address.state || " " ||
                    address.country)
                    FROM profile
                    LEFT JOIN address ON  profile.address_id=address.id
                    WHERE profile.first_name LIKE ?
                    OR profile.last_name LIKE ? 
                    OR profile.phone_number1 LIKE ?
                    OR profile.phone_number2 LIKE ?
                    OR profile.birth_date LIKE ?
                    OR address.line1 LIKE ?
                    OR address.street LIKE ?
                    OR address.suburb LIKE ?
                    OR address.postcode LIKE ?
                    OR address.state LIKE ?
                    OR address.country LIKE ?;
                  """,([pattern]*11)
                  )
        result=[]
        for each in c.fetchall():
            result.append(each)
        print('SQLite Database searched!!')
        return result

def mysqlsearch_index(pattern):
    pattern = pattern
    mysqlconn.database = DB_NAME
    mysqlcursor.execute("""
                SELECT CONCAT_WS(' ',profile.first_name,profile.last_name),
                profile.phone_number1,
                profile.phone_number2,
                profile.birth_date,
                CONCAT_WS(' ',address.line1,
                address.street,
                address.suburb,
                address.postcode,
                address.state,
                address.country)
                FROM profile
                LEFT JOIN address ON  profile.address_id=address.id
                WHERE profile.id=%s;
              """,[pattern]
              )
    result=[]
    for each in mysqlcursor.fetchall():
        result.append(each)
    print('MySQL Database index searched!!')
    return result

def search_index(pattern):
    pattern = pattern
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
                    SELECT (profile.first_name || " " || profile.last_name),
                    profile.phone_number1,
                    profile.phone_number2,
                    profile.birth_date,
                    (address.line1 || " " ||
                    address.street || " " ||
                    address.suburb || " " ||
                    address.postcode || " " ||
                    address.state || " " ||
                    address.country)
                    FROM profile
                    LEFT JOIN address ON  profile.address_id=address.id
                    WHERE profile.id =?;
                  """,[pattern]
                  )
        result=[]
        for each in c.fetchall():
            result.append(each)
        print('SQLite Database index searched!!')
        return result

def func_timer(func):
    start = time.clock()
    func
    end = time.clock()
    print(end-start)

if __name__ == '__main__':
    sqlite_db = create_table()
    mysql_db = mysqlcreate_db()
    while True:
        try:
            entries = input('How many records should I insert to SQL?')
            entries = int(entries)
            assert (entries >= 0)
            break
        except (TypeError, ValueError):
            print('Please input an integer')
            continue
        except AssertionError:
            print('Please input a positive integer')
            continue
    add_entries = insert_fakes(entries)
    general_pattern = input('Please input string to search')
    func_timer(search_data(general_pattern))
    func_timer(mysqlsearch_data(general_pattern))
    index_pattern = input('Please input index to search')
    func_timer(mysqlsearch_index(index_pattern))
    func_timer(search_index(index_pattern))
