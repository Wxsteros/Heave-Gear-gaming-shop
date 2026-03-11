import sqlite3
def add_student():
    conn = sqlite3.connect(r"D:\python porgramming\register_studen_data.db")
    c = conn.cursor()
    while True:
            fname = input("ชื่อ : ")
            lname = input("นามสกุล : ")
            email = input("อีเมล : ")
            sex = input("เพศ : ")
            age = int(input("อายุ : "))
            grade = int(input("ระดับชั้น : "))
            c.execute('''INSERT INTO users (id, fname, lname, email,sex, age, grade) 
              VALUES (NULL, ?, ?, ?, ?, ?, ?)''', (fname, lname, email,sex, age, grade))
            confirm = input("ต้องการเพิ่มข้อมูลนักเรียนต่อหรือไม่ (y/n) : ")
            if confirm.lower() == 'y':
                continue
            elif confirm.lower() == 'n':
                break       
    conn.commit()
    conn.close()

def show_students():
    conn = sqlite3.connect(r"D:\python porgramming\register_studen_data.db")
    c = conn.cursor()
    c.execute('''SELECT * FROM users''')
    result = c.fetchall() 
    print("{0:^100}".format("Student Information"))
    print("{0:-<100}".format(""))
    print("{0:<5}{1:<20}{2:<20}{3:<30}{4:<10}{5:<5}{6:<5}".format("ID","Firstname","Lastname","Email","Gender","Age","Grade"))
    print("{0:-<100}".format(""))
    for x in result:
        print("{0:<5}{1:<20}{2:<20}{3:<30}{4:<10}{5:<5}{6:<5}".format(x[0],x[1],x[2],x[3],x[4],x[5],x[6]))
    print("{0:-<100}".format(""))
    conn.close()

def delete_student():
    conn = sqlite3.connect(r"D:\python porgramming\register_studen_data.db")
    c = conn.cursor()
    while True:
        student_id=input('กรากรหัสนักเรียนที่ต้องการลบ')
        c.execute('''DELETE FROM users WHERE id=?''', (student_id,))
        confirm = input("ต้องการลบข้อมูลนักเรียนต่อหรือไม่ (y/n) : ")
        if confirm.lower() == 'y':
            continue
        elif confirm.lower() == 'n':
            break       
    conn.commit()
    conn.close()

def Updat_data_studen():
    conn = sqlite3.connect(r"D:\python porgramming\register_studen_data.db")
    c = conn.cursor()
    edit_studen_data = input("กรุณากรอกรหัสนักเรียน: ")
    c.execute("SELECT id, fname, lname, email, sex, age, grade FROM users WHERE id = ?", (edit_studen_data,))
    result = c.fetchone()
    if result : 
        print("{0:<110}".format(""))
        print("ข้อมูลของนักเรียนที่ต้องการแก้ไข")
        print("{0:<110}".format(""))
        print("{0:-<115}".format(""))
        print(f"Studen ID : {result[0]} | Name : {result[1]} Lastname : {result[2]} Email : {result[3]} Sex : {result[4]} Age : {result[5]} grade : {result[6]}") 
        print("{0:-<115}".format(""))
        print('{0:^48}'.format("เลือกข้อมูลที่ต้องการแก้ไข"))
        print('{0:<36}{1:>5}'.format("ชื่อ","[1]"))
        print('{0:<35}{1:>5}'.format("นามสกุล","[2]"))
        print('{0:<35}{1:>5}'.format("อีเมล","[3]"))
        print('{0:<34}{1:>5}'.format("เพศ","[4]"))
        print('{0:<35}{1:>5}'.format("อายุ","[5]"))
        print('{0:<37}{1:>5}'.format("ระดับชั้น ","[6]"))
        print('{0:<35}{1:>5}'.format("ออกจากการแก้ไข","[x]"))
        print("{0:-<40}".format(""))

        while True:
            choice=input("เลือกข้อมูลที่ต้องการแก้ไข :")
            if choice=='1':
                print(f"ชื่อเดิม : {result[1]}")
                new_data =input("กรุณากรอกชื่อใหม่ที่จะแก้ไข :")
                c.execute('''UPDATE users SET fname=? WHERE id=?''',(new_data,edit_studen_data))
                conn.commit()
                print("แก้ไขชื่อเรียบร้อย")
            elif choice=='2':
                print(f"นามสกุลเดิม : {result[2]}")
                new_data= input("กรุณากรอกนามสกุลใหม่ที่จะแก้ไข :")
                c.execute('''UPDATE users SET lname=? WHERE id=?''',(new_data,edit_studen_data))
                conn.commit()
                print("แก้ไขนามสกุลเรียบร้อย")
            elif choice=='3':
                print(f"อีเมลเดิม : {result[3]}")
                new_data= input("กรุณากรอกอีเมลใหม่ที่จะแก้ไข :")
                c.execute('''UPDATE users SET email=? WHERE id=?''',(new_data,edit_studen_data))
                conn.commit()
                print("แก้ไขอีเมลเรียบร้อย")
            elif choice=='4':
                print(f"เพศเดิม : {result[4]}")
                new_data= input("กรุณากรอกเพศที่ต้องการจะแก้ไข :")
                c.execute('''UPDATE users SET sex=? WHERE id=?''',(new_data,edit_studen_data))
                conn.commit()
                print("แก้ไขเพศเรียบร้อย")
            elif choice=='5':
                print(f"อายุเดิม : {result[5]}")
                new_data= input("กรุณากรอกอายุที่จะแก้ไข :")
                c.execute('''UPDATE users SET age=? WHERE id=?''',(new_data,edit_studen_data))
                conn.commit()
                print("แก้ไขอายุเรียบร้อย")
            elif choice=='6':
                print(f"ระดับชั้นเดิม {result[6]}")
                new_data= input("กรุณากรอกระดับชั้นที่จะแก้ไข :")
                c.execute('''UPDATE users SET grade=? WHERE id=?''',(new_data,edit_studen_data))
                conn.commit()
                print("แก้ไขระดับชั้นเรียบร้อย")
            elif choice=='x':
                break
            confirm = input("ต้องการแก้ข้อมูลนักเรียนต่อใช่หรือไม่ (y/n) : ")
            if confirm.lower() == 'y':
                continue
            elif confirm.lower() == 'n':
                break          
    else:
        print("ไม่พบรหัสนักเรียน")    
    conn.close()
   
while True:
    print('{0:-<40}'.format(""))
    print('{0:<41}{1:>5}'.format("เพิ่มข้อมูลนักเรียน","[a]"))
    print('{0:<39}{1:>5}'.format("แสดงข้อมูลนักเรียน","[s]"))
    print('{0:<39}{1:>5}'.format("ลบข้อมูลนักเรียน","[d]"))
    print('{0:<40}{1:>5}'.format("แก้ไขข้อมูลนักเรียน","[e]"))
    print('{0:<35}{1:>5}'.format("ออกจากโปรแกรม","[x]"))
    print('{0:-<40}'.format(""))
    choice = input("เลือกทำรายการ : ")
    if choice.lower() == 'a':
        add_student()      
    elif choice.lower() == 's':
        show_students()
    elif choice.lower() == 'd':
        delete_student()
    elif choice.lower()== 'e':
        Updat_data_studen()
    elif choice.lower()== 'x':
        confirm = input("ต้องการออกจากโปรแกรมใช่หรือไม่ (y/n) : ")
        if confirm.lower() == 'y':
            continue
        elif confirm.lower() == 'n':
            break       