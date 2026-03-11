print('{0:-<50}'.format(""))  
print('{0:^50}'.format('เลือกเมนูเพื่อทำรายการ'))
print('{0:-<50}'.format(""))
print('{0:^50}'.format('กด1 เลือกเหมาจ่าย'))
print('{0:^50}'.format('กด2 เลือกจ่ายเพิ่ม'))
select=input("select menu :")
distance=int(input("please input distance :"))
if select=='1':
    if distance <=25 :
        total=25
    elif distance >25:
        total=55
    print('ค่าใช้จ่าย รวมทั้งหมด',total)
elif select  =='2':
    if distance <25 :
            total=25
    elif distance >25:
            total=25+55
    print('ค่าใช้จ่าย รวมทั้งหมด',total)
else:
    print("errer try again")
    
