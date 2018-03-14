import sqlite3
import timeit
from faker import Faker
from os import path


base_dir = path.dirname(path.abspath(__file__))
db_path = path.join(base_dir,'profile.db')
schema_path = path.join(base_dir,'schema.sql')
fake_gen = Faker('en_AU')

def create_table():
    with sqlite3.connect(db_path) as conn:
        with open(schema_path, 'rt') as f:
            schema = f.read()
        conn.executescript(schema)
        print('Table created!')


def create_entry(quantity):
    for i in range(1,quantity):
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute("""
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
                      """,(
                        fake_gen.building_number(),
                        fake_gen.street_name(),
                        fake_gen.city(),
                        fake_gen.postcode(),
                        fake_gen.state_abbr(),
                        'Australia'
                        )
                      )
            c.execute("""
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
                      """,(
                        fake_gen.first_name(),
                        fake_gen.last_name(),
                        fake_gen.phone_number(),
                        fake_gen.phone_number(),
                        fake_gen.date_time_this_century(before_now=True, after_now=False, tzinfo=None)
                        )
                    )
            conn.commit()
        print(i)

def search_data(pattern):
    pattern = '%'+pattern+'%'
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("""
                    SELECT (profile.first_name || " " || profile.last_name),
                    profile.phone_number1,
                    profile.phone_number2,
                    profile.birth_date,
                    (address.line1 || " " ||
                    address.line3 || " " ||
                    address.line4 || " " ||
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
                    OR address.line2 LIKE ?
                    OR address.line3 LIKE ?
                    OR address.line4 LIKE ?
                    OR address.street LIKE ?
                    OR address.suburb LIKE ?
                    OR address.postcode LIKE ?
                    OR address.state LIKE ?
                    OR address.country LIKE ?;
                  """,([pattern]*14)
                  )
        result=[]
        for each in c.fetchall():
            result.append(each)
        print('DB searched!!')
        return result

if __name__ == '__main__':
    if not path.exists(db_path): create_table()
    create_entry(20000)
    pattern = input('Seacrh for :')
    my_timer = timeit.timeit(stmt='search_data(pattern)', number=1,setup="from __main__ import search_data, pattern")
    print(my_timer)

