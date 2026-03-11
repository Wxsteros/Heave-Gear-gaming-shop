import sqlite3
conn = sqlite3.connect(r"D:\python porgramming\register_studen_data.db")
c = conn.cursor()
c.execute('''CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT,
    fname VARCHAR(30) NOT NULL,  
    lname VARCHAR(30) NOT NULL,
    email VARCHAR(100) NOT NULL,
    sex VARCHAR(10) NOT NULL,
    age INTEGER(5) NOT NULL,
    grade INTEGER(5) NOT NULL)''')
conn.commit() # บันทึกการเปลี่ยนแปลง
conn.close() # ปิดการเชื่อมต่อกับฐานข้อมูล
