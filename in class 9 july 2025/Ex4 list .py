#Northlist = ["Kittikon","kingwichit","673050379-2","19","099-369-0768","Sisaket"]
#print(Northlist)
#print(Northlist[4]) # ตำแหน่งที่ 4
#print(Northlist[-1]) #ถ้าเป็น - จะนับจากด้านหลังก่อน
#print(Northlist[1:3]) #เริ่มที่1-3
#print(Northlist[:3])  
#print(Northlist[1:]) 

#การแก้ใขข้อมูลใน list
#thislist=["com","ED","KKU",99]
#thislist[0] = "comED" #เป็นการเรียงลำดับแบบ Index
#thislist[1:3] = "en","cu"
#print(thislist)

#การเพิ่มข้อความในlist append
#thislist = ["Com","ED","kku",99]
#thislist.append("com21")
#print("this is your new list ",thislist)

#insert เพิ่มข้อมูลแบบระบุตำแหน่ง
#thislist=["com","Ed","kku",99]
#thislist.insert(1,"x")
#print("this is your new list ",thislist)

#remove ลบข้อมูล
#thislist=["com","Ed","kku",99]
#thislist.remove("com")
#print("this is your new list ",thislist)

#pop การดึงข้อมูลตัวสุดท้ายออกมา
#thislist=["com","Ed","kku",99]
#thislist.pop()
#print("this is your new list ",thislist)

#thislist=["com","Ed","kku",99]
#del thislist[3] #ลบตำแหน่งที่3
#del thislist #ลบทั้งหมด
#print("this is your new list ",thislist)


thislist=["com","Ed","kku",99]
thislist.clear()
print("this is your new list ",thislist)