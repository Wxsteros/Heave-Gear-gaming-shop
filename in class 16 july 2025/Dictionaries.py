#ไม่มีการเรียงลำดับข้อมูล แต่จะเข้าถึงข้อมูลได้ผ่าน key
thisdict ={
    "fname" : "Kittikon",
    "lname" : "Kingwichit",
    "year" : 2006
}
#การเข้าถึงข้อมูลโดยระบุ  key 

x=thisdict["fname"]  
print(x)

#เปลี่ยนข้อมูล
thisdict["year"] = 2025 #เปลี่ยนจาก 2006เป็น2025
print(thisdict)

#เพิ่มข้อมูล สร้างkey ใหม่
thisdict["nation"] = "thai"  
print(thisdict)

#ลบข้อมูล
#thisdict.pop("year") # ลบข้อมูลที่มี Key คือ year
#thisdict.popitem() #ลบข้อมูลที่เพิ่มล่าสุด
del thisdict #ลบตัวแปล thisdict  
print(thisdict)  