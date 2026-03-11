import sqlite3
conn = sqlite3.connect(r"D:\python porgramming\example.db")
c = conn.cursor()

try:
    c.execute('DELETE FROM users')
    conn.commit()

except sqlite3.Error as e:
    print(e)

finally:
    if conn:
        conn.close()