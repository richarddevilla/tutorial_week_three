create table profile (
    id           INTEGER PRIMARY KEY autoincrement NOT NULL,
    first_name   TEXT,
    last_name    TEXT,
    address_id   INTEGER,
    phone_number1 TEXT,
    phone_number2 TEXT,
    birth_date   DATE ,
    FOREIGN KEY(address_id) REFERENCES address(id)
);

create table address (
    id           INTEGER PRIMARY KEY autoincrement NOT NULL,
    line1        TEXT,
    street       TEXT,
    suburb       TEXT,
    postcode     TEXT,
    state        TEXT,
    country      TEXT
);