create table profile (
    id           INTEGER PRIMARY KEY autoincrement NOT NULL,
    first_name   TEXT DEFAULT '',
    last_name    TEXT DEFAULT '',
    address_id   INTEGER,
    phone_number1 TEXT,
    phone_number2 TEXT,
    birth_date   DATE ,
    FOREIGN KEY(address_id) REFERENCES address(id)
);

create table address (
    id           INTEGER PRIMARY KEY autoincrement NOT NULL,
    line1        TEXT DEFAULT '',
    line2        TEXT DEFAULT '',
    line3        TEXT DEFAULT '',
    line4        TEXT DEFAULT '',
    street       TEXT DEFAULT '',
    suburb       TEXT DEFAULT '',
    postcode     TEXT DEFAULT '',
    state        TEXT DEFAULT '',
    country      TEXT DEFAULT '',
    profile_id   INTEGER
);