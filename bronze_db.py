#
# This .py file have functions to generate fake profiles
# and store them in a SQLite and MySQL database
#
import mysql.connector
import sqlite3
import time
from faker import Faker
from os import path

#Static variables
BASE_DIR = path.dirname(path.abspath(__file__))
DB_PATH = path.join(BASE_DIR, 'profile.db')
SQLITE_SCHEMA_PATH = path.join(BASE_DIR, 'sqlite_schema.sql')
MYSQL_SCHEMA_PATH = path.join(BASE_DIR, 'mysql_schema.sql')
DB_NAME = 'profile'

#fake generator profile set to return Australian profiles
fake_gen = Faker('en_AU')

#create MySQL connector and cursor
mysql_conn = mysql.connector.connect(user='richard',
                                     password='password',
                                     host='35.189.34.179')
mysql_cursor = mysql_conn.cursor()

#create SQLite3 connector and cursor
sqlite_conn = sqlite3.connect(DB_PATH)
sqlite_cursor = sqlite_conn.cursor()

def mysql_create_db():
    """
        Create MySQL Database and Tables if not already existing
    """
    print('Checking if MySQL Database exist')
    try:
        with open(MYSQL_SCHEMA_PATH, 'rt') as f:
            schema = f.read().split(';')
            for command in schema:
                mysql_cursor.execute(command)
            print('MySQL Database profile created!')
    except:
        print('MySQL Database already exist')
    finally:
        mysql_conn.database = DB_NAME

def sqlite_create_db():
    """
        Create sqlite Database and Tables if not already existing
    """
    try:
        print('Checking if SQLite3 Database exist')
        with open(SQLITE_SCHEMA_PATH, 'rt') as f:
            schema = f.read()
            sqlite_conn.executescript(schema)
        print('SQLite3 Database profile created!')
    except Exception:
        print('SQLite3 Database already exist')

def create_fakes(quantity):
    """
    :param quantity: integer
    :return: list of contact info, size of list depends on param quantity
    """
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
    """
    :param entries: list of contact info

    function takes a list of mutliple personal info.
     iterate through the info and insert it
     to MySQL and Sqlite3 prints execution time on console
    """
    data = create_fakes(entries)
    start = time.clock()
    for each in data:
        sqlite_create_entry(each)
    sqlite_conn.commit()
    end = time.clock()
    print('Insert SQLite total time '+str(end-start))
    start = time.clock()
    for each in data:
        mysql_create_entry(each)
    mysql_conn.commit()
    end = time.clock()
    print('Insert MySQL total time ' + str(end - start))

def sqlite_create_entry(data):
    """
    :param data: list of a single person's info
    function would insert the info to Sqlite3 database
    """
    sqlite_cursor.execute("""
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
    sqlite_cursor.execute("""
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

def mysql_create_entry(data):
    """
    :param data: list of a single person's info
    function would insert the info to MySQL database
    """
    mysql_cursor.execute("""
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
    mysql_cursor.execute("""
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

def mysql_search_data(pattern):
    """
    :param pattern: takes a string
    :return result: list of match

    function takes a pattern and look for the pattern in the MySQL database
    this function would look into all fields and return the list of result
    with the full info of the matches
    """
    mysql_cursor.execute('USE {};'.format(DB_NAME), multi=True)
    pattern = '%'+pattern+'%'
    mysql_cursor.execute("""
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
              """, ([pattern]*11)
                         )
    result=[]
    for each in mysql_cursor.fetchall():
        result.append(each)
    print('MySQL Database searched!!')
    return result

def sqlite_search_data(pattern):
    """
    :param pattern: takes a string
    :return result: list of match

    function takes a pattern and look for the pattern in the Sqlite3 database
    this function would look into all fields and return the list of result
    with the full info of the matches
    """
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

def mysql_search_index(pattern):
    """
    :param pattern: takes a string
    :return result: list of match

    function takes a pattern and look for the pattern in the MySQL database
        this function would look into index and return the full info of the match
    """
    pattern = pattern
    mysql_cursor.execute("""
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
              """, [pattern]
                         )
    result=[]
    for each in mysql_cursor.fetchall():
        result.append(each)
    print('MySQL Database index searched!!')
    return result

def sqlite_search_index(pattern):
    """
        :param pattern: takes a string
        :return result: list of match

        function takes a pattern and look for the pattern in the Sqlite3 database
        this function would look into index and return the full info of the match
    """
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
    """
    :param func: takes a function
    :return runtime: time it takes for function to run
    """
    start = time.clock()
    func
    end = time.clock()
    print(end-start)
#calls the create_db functions
sqlite_db = sqlite_create_db()
mysql_db = mysql_create_db()

#main program to use functions
if __name__ == '__main__':
    while True:
        #Ask user to input quantity of fake records to create
        #it must be a positive integer or 0
        try:
            entries = input('How many records should I insert to SQL?\n'
                            '(more than 10,000 records might take awhile)\n')
            entries = int(entries)
            assert (entries >= 0)
            break
        except (TypeError, ValueError):
            print('Please input an integer')
            continue
        except AssertionError:
            print('Please input a positive integer')
            continue
    #insert fake records to MySQL and Sqlite3
    add_entries = insert_fakes(entries)
    #Ask user to input a general search query
    general_pattern = input('Please input string to search')
    #Run a search to all field in both database and return their time
    func_timer(sqlite_search_data(general_pattern))
    func_timer(mysql_search_data(general_pattern))
    #Ask user to input an index search query
    index_pattern = input('Please input index to search')
    # Run a search considering index only in both database and return their time
    func_timer(mysql_search_index(index_pattern))
    func_timer(sqlite_search_index(index_pattern))
