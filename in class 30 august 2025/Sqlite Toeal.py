import sqlite3 # Import sqlite3 
conn = sqlite3.connect(r"D:\python porgramming\example.db") # ทำการเชื่อมต่อกับฐานข้อมูล'
c = conn.cursor()
#สร้างตารางชื่อ users สร้างคอลัมน์ id เป็น integer ทำหน้าที่เป็น primary key และเพิ่มค่าอัตโนมัติทุกครั้งที่มีการเพิ่มแถวใหม่
c.execute('''CREATE TABLE users(id integer PRIMARY KEY AUTOINCREMENT, 
           fname varchar(30) NOT NULL,  
           lname varchar(30) NOT NULL,
           email varchar(100) NOT NULL)''') 
conn.commit() #บันทึกการเปลี่ยนแปลง      
conn.close() # ปิดการเชื่อมต่อกับฐานข้อมูล