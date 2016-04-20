import sqlite3 as lite
import sys

con = lite.connect('Computers.db')

with con:
    
    cur = con.cursor()    
    cur.execute("SELECT * from Computers;")

    rows = cur.fetchall()
    for row in rows:
        print row
    
