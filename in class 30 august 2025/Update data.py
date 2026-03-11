import sqlite3

conn=sqlite3.connect(r"D:\python porgramming\example.db")
c=conn.cursor()
try:
    data=('ABC','XYZ','ABC@gmail.com',3) # 3 ตำแหน่ง id ที่ต้องการแก้ไข
    c.execute('''UPDATE users SET fname=?, lname=?, email=? WHERE id=?''',data)
    conn.commit()
except sqlite3.Error as e:
    print(e)
finally:
    if conn:
        conn.close()
# !!! ข้อควรระวังในการใช้คำสั่ง UPDATE หากไม่ระบุตำแหน่งที่ต้องการแก้ไข (WHERE) จะทำให้ข้อมูลในตารางทั้งหมดถูกแก้ไขเป็นค่าที่ระบุในคำสั่ง UPDATE