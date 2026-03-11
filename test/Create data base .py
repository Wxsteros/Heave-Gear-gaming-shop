import sqlite3
conn = sqlite3.connect(r"D:\python porgramming\project.db") # สร้างการเชื่อมต่อกับฐานข้อมูล'
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                Gmail TEXT NOT NULL,    
                Username TEXT NOT NULL,
                password TEXT NOT NULL,
                phone number NOT NULL,
                address TEXT NOT NULL,
                fname TEXT NOT NULL,)''')
          
c.execute( '''CREATE TABLE IF NOT EXISTS products
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name product TEXT NOT NULL,    
                price REAL NOT NULL,
                stock INTEGER NOT NULL,
                description TEXT NOT NULL,)''')

conn.commit() 
conn.close() 
