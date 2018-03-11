import sqlite3
import timeit
from faker import Faker
from os import path

base_dir = path.dirname(path.abspath(__file__))
db_path = path.join(base_dir,'profile.db')
schema_path = path.join(base_dir,'schema.sql')
fake_gen = Faker('en_AU')

def create_table(db_path):
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
                          "{}","{}","{}","{}","{}","{}"
                        )
                      """.format(
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
                          "{}","{}","{}","{}","{}",LAST_INSERT_ROWID()
                        )
                      """.format(
                        fake_gen.first_name(),
                        fake_gen.last_name(),
                        fake_gen.phone_number(),
                        fake_gen.phone_number(),
                        fake_gen.date_time_this_century(before_now=True, after_now=False, tzinfo=None)
                        )
                    )
            conn.commit()

if __name__ == '__main__':
    if not path.exists(db_path): create_table()
    my_timer = timeit.timeit(stmt='create_entry(10000)', number=1,setup="from __main__ import create_entry")
    print(my_timer)
