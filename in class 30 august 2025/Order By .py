import sqlite3
conn=sqlite3.connect(r"D:\python porgramming\example.db")
c=conn.cursor()

#DESC เรียงจากมากไปน้อย
#ASC เรียงจากน้อยไปมาก
try:
    c.execute('''SELECT * FROM users ORDER BY id ASC''')
    conn.commit()
    result=c.fetchall()
    for x in result:   
        print(x)
except Exception as e:
    print(e)

finally:
    if conn:
        conn.close()