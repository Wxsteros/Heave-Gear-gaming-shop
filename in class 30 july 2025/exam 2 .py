print("NN IT SHOP")
Box=[]
j=1
while True:
    print("=====================================") 
    print("เพิ่มข้อมูลลูกค้า   [a]\nแสดงข้อมูลลูกค้า  [s]\nออกจากระบบ    [x]")
    print("=====================================")          
    x = str(input("กรุณาเลือกคำสั่ง : "))
    if x == "a":
        data= input("กรุณากรอกข้อมูลลูกค้า (รหัส: ชื่อ: จังหวัด) ")
        Box.append(data)
    elif x == "s":
        for c in Box:
            print(f"ข้อมูลลูกค้าคนที่ {j}: {c}")
            j += 1
    elif x == "x":
        confirm = input("คุณต้องการออกจากระบบหรือไม่ (y/n) : ")
        if confirm == 'n':
            continue  
        elif confirm == 'y':
            break






