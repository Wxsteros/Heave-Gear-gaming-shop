class nisit :
    def __init__(self, name,surname,gender,grade,Major):
        self.name = name
        self.surname=surname
        self.gender=gender
        self.grade=grade
        self.Major=Major

    def show(self):
        print("ชื่อ:", self.name)
        print("นามสกุล:", self.surname)
        print("เพศ:", self.gender)
        print("ชั้นปี:", self.grade)
        print("สาขา:", self.Major)

print('{0:-<50}'.format(""))
print('{0:^50}'.format('แนะนำตัว'))
print('{0:-<50}'.format(""))
name= input("ชื่อ: ")
surname= input("นามสกุล: ")
gender= input("เพศ: ")
grade= input("ชั้นปี: ")
Major= input("สาขา: ")
print('{0:-<50}'.format(""))
print('{0:^50}'.format('ข้อมูลนักศึกษา'))
print('{0:-<50}'.format(""))
x= nisit(name,surname,gender,grade,Major)
x.show()