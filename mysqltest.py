import mysql.connector
from mysql.connector import errorcode
from faker import Faker

mysqlconn = mysql.connector.connect(
    user='richard',
    password='password',
    host='192.168.1.4',
    database='profile')
mysqlcursor = mysqlconn.cursor()
mysqlfake_gen = Faker('en_AU')

DB_NAME = 'profile'

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
    "   `line2` varchar(100) DEFAULT '',"
    "   `line3` varchar(100) DEFAULT '',"
    "   `line4` varchar(100) DEFAULT '',"
    "   `street` varchar(100) DEFAULT '',"
    "   `suburb` varchar(100)  DEFAULT '',"
    "   `postcode` varchar(100) DEFAULT '',"
    "   `state` varchar(100) DEFAULT '',"
    "   `country` varchar(100) DEFAULT 'Australia',"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

############
#Codes here are based from https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
############
def create_database(mysqlcursor):
    try:
        mysqlcursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    mysqlconn.database = DB_NAME
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(mysqlcursor)
        mysqlconn.database = DB_NAME
    else:
        print(err)
        exit(1)


for name, ddl in TABLES.items():
    try:
        print("Creating table {}: ".format(name), end='')
        mysqlcursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")
###########
#End of codes from https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
#############
def mysqlcreate_entry(quantity):
    for i in range(1,quantity):
        c = mysqlconn.cursor()
        c.execute("""
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
                  """,(
                    mysqlfake_gen.building_number(),
                    mysqlfake_gen.street_name(),
                    mysqlfake_gen.city(),
                    mysqlfake_gen.postcode(),
                    mysqlfake_gen.state_abbr()
                    )
                  )
        c.execute("""
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
                  """,(
                    mysqlfake_gen.first_name(),
                    mysqlfake_gen.last_name(),
                    mysqlfake_gen.phone_number(),
                    mysqlfake_gen.phone_number(),
                    mysqlfake_gen.date_time_this_century(before_now=True, after_now=False, tzinfo=None)
                    )
                )
        mysqlconn.commit()
        print(i)

def mysqlsearch_data(pattern):
    pattern = '%'+pattern+'%'
    c = mysqlconn.cursor()
    c.execute("""
                SELECT CONCAT_WS(' ',profile.first_name,profile.last_name),
                profile.phone_number1,
                profile.phone_number2,
                profile.birth_date,
                CONCAT_WS(' ',address.line1,
                address.line3,
                address.line4,
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
                OR address.line2 LIKE %s
                OR address.line3 LIKE %s
                OR address.line4 LIKE %s
                OR address.street LIKE %s
                OR address.suburb LIKE %s
                OR address.postcode LIKE %s
                OR address.state LIKE %s
                OR address.country LIKE %s;
              """,([pattern]*14)
              )
    result=[]
    for each in c.fetchall():
        result.append(each)
    return result
