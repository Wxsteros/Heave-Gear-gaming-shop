import sqlite3

conn=sqlite3.connect(r"D:\python porgramming\example.db")
c=conn.cursor()
try:
    c.execute('DROP TABLE users')
    conn.commit()
    c.close()
except sqlite3.Error as e:
    print(e)
finally:
    if conn:
        conn.close()