#thistuple=("com","ED","KKU")
#print(thistuple)

#การเข้าถึงข้อมูล
#print(thistuple[1])
#print(thistuple[-1])
#print(thistuple[0:1])

#การแก้ไขtuple
#x=("com","ED","KKU") #("com","ED","KKU")
#y=list(x) #["com","ED","KKU"]
#y[0]="ComED"
#x=tuple(y)
#print(x)

#เมื่อTupleถูกสร้างขึ้นจะไม่สามารถเพิ่มข้อมูล

#การลบข้อมูล
x=("com","ED","KKU")
del x(2) #ลบข้อมูลใน x 
print(x)