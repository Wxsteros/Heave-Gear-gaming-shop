import sqlite3 # Import sqlite3 
conn = sqlite3.connect(r"D:\python porgramming\example.db") # สร้างการเชื่อมต่อกับฐานข้อมูล'
c = conn.cursor()
c.execute('''INSERT INTO users (id,fname, lname,email) VALUES (NULL,'Kittikon','Kingwichit','Kittikon.k')''')
c.execute('''INSERT INTO users VALUES (NULL,'Rapirat','Wangdongbang','Rapirat.w')''')
conn.commit() #บันทึกการเปลี่ยนแปลง 
conn.close() # ปิดการเชื่อมต่อกับฐานข้อมูล
