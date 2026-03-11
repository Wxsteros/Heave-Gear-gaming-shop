#def introduce():
#    print("Hello, I'm a function!")
#    print("I'll do nothing at all.")
#    print("call me if you need to help.")
#introduce()

#argument เป็นตัวแปรที่ใช้ในการรับค่าเข้ามาในฟังก์ชัน โดยจะต้องระบุชื่อของตัวแปรในวงเล็บ
#def introduce(name):
#    print("Hello,I'm " + name)
#introduce("Python")

#name=str(input("กรุณากรอกชื่อของคุณ : "))
#def introduce(name):
#    print("Hello,I'm " + name)
#introduce(name)

#ในการประกาศฟังก์ชันสามารมารถกมี argument ได้ไม่จำกัดจำนวน
#def introduce(province, nation,):
#    print(f"Hello,I'm from " + province + " " + nation)
#introduce("khonkaen","Thailand",)

#def introduce(age1, age2="com",age3="ed",age4="kku"):
#    print("hello,I'm " + age1 + "," + age2 + "," + age3 + "," + age4)

#introduce() #Error เพราะไม่มีการกำหนดค่าให้กับ argument
#introduce(age1="python","CMU") #Error ถ้าใช้ keyword argument แล้วตัวถัดไปต้องเป็น keyword ด้วยเท่านั้น 
#introduce("python 2",age1="python 3") #Python ไม่ยอมให้กำหนดค่าให้ argument เดียวกัน 2 ครั้ง
#introduce(arg99 = "CMU") #Error เพราะ arg99 ไม่ได้ถูกกำหนดในฟังก์ชัน

def Introduce(name, *hobby, **address): # * ใช้สำหรับรับค่าหลายค่าเป็น tuple และ ** รับแบบระบุชื่อ dictionary
    print("Hello, I am " + name + ".")
    print("My address:")
    for kw in address: 
        print(kw + " : " + address[kw])
    print("My hobby:")
    for arg in hobby:
        print(arg)

Introduce('P', 'Sport', 'Music', 'game', province='Khon Kaen', nation='Thailand')
