import sqlite3

conn=sqlite3.connect(r"D:\python porgramming\example.db")
c=conn.cursor()

try:
    c.execute('''SELECT * FROM users LIMIT 3''')
    result=c.fetchall()
    for x in result:   
        print(x)
except Exception as e:
    print(e)
finally:
    if conn:
        conn.close()

        