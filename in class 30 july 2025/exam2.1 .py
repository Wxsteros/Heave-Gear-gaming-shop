print("NN IT SHOP")
Box = []
j = 1
while True:
    print("=====================================") 
    print("เพิ่มข้อมูลลูกค้า   [a]\nแสดงข้อมูลลูกค้า  [s]\nออกจากระบบ     [x]")
    print("=====================================")          
    x = input("กรุณาเลือกคำสั่ง : ")
    if x == "a":
        data = input("กรุณากรอกข้อมูลลูกค้า (รหัส:ชื่อ:จังหวัด) ")
        Box.append(data)
    elif x == "s":
        print("{0:-<30}".format(""))
        print("{0:<10} {1:<10} {2:<10}".format("รหัส","ชื่อ","จังหวัด"))
        print("{0:-<30}".format(""))
        for c in Box:
            e = c.split(':')
            print('{0[0]:<10} {0[1]:<10} {0[2]:<10}'.format(e))
       
    elif x == "x":
        confirm = input("คุณต้องการออกจากระบบหรือไม่ (y/n) : ")
        if confirm == 'n':
            break
