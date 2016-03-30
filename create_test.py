import sqlite3 as lite
import sys

con = lite.connect('test.db')

with con:
    
    cur = con.cursor()    
    cur.execute("CREATE TABLE Computers(Serial TEXT PRIMARY KEY NOT NULL,Tag TEXT  NOT NULL, Ship INT, Location INT);")

