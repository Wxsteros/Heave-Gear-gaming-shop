#thisset={"com","ED","KKU"}
#print(thisset)

# การเข้าถึงข้อมูลใน set ไม่สามารถเข้าถึงได้เพราะไม่มีจัดตำแหน่งแบบ index 
#thisset ={"com","ED","KKU"}
#for x in thisset:
#    print(x)

#การเปลี่ยนแปลงข้อมูลใน set ไม่สามารถเปลี่ยนแปลงได้

#การเพิ่มข้อมูล
#thisset={"com","ED","KKU"}
#thisset.add("North") # เพิ่มที่ละ 1
#thisset.update(["I","so","good"]) # เพิ่มที่ละ 3 แต่ ตอน print สุ่มเหมือนเดิม
#print(thisset)

#การลบข้อมูลใน set
thisset={"com","ED","KKU"} #{"com","ED","KKU"}
#thisset.remove("com") # {"ED","KKU"}
#thisset.discard("com") #{"ED","KKU"}
#thisset.clear()#{}
del thisset
print(thisset)