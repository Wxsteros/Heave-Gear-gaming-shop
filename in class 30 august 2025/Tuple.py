import sqlite3

conn = sqlite3.connect(r"D:\python porgramming\example.db")
c = conn.cursor()

name = ('Kittikon',)
c.execute('SELECT * FROM users WHERE fname=?', name)

result = c.fetchall()
for x in result:
    print(x)