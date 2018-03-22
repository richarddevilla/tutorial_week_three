#Test Environment
OS:Windows 10
IDE:PyCharm 2017.3
MYSQL:MySQL 5.7 on Google Cloud
PYTHON:3.4

#required python packages
tkinter
faker 0.81
mysql-python-connector 2.0.4

#Additional Note
place all files to the same directory.
bronze_gui.py calls function from bronze_db.py
bronze_db.py uses mysql_schema.sql and sqlite_schema.sql
profile.db and mysql server have 120,104 identical records

#Usage
bronze.py - demonstrate simple creation of database
broze_db.py - allows creation of sqlite3 database and have a fake info generator
    just run and follow prompt if you wish to add more entry, be warned that 20,000
    records and up would probably take mins or hours
bronze_gui.py - display a form for a general search and index search on the
    sqlite3 and MySQL database

