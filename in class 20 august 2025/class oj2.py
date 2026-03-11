class Car:
    def __init__(self, name, color):
        self.name = name
        self.color = color
    def showcar(self):
        print('Information : Name:', self.name, 'Color:', self.color)

class NewCar(Car): 
    pass #การสืบทอดคลาส Car มาใช้ในคลาส NewCar 

class NewCar(Car):
    def __init__(self, name, color): 
        Car.__init__(self, name, color) #Car. คือการสือบทอดคุณสมบัติจาก Class Car มาใช้ในคลาส NewCar โดยตรง
    
class NewCar(Car):
    def __init__(self, name, color):
        super().__init__(name, color) #super() คือการสืบทอดคุณสมบัติและMethodจากคลาสแม่มาใช้ในคลาสลูก

class NewCar(Car):
    def __init__(self, name, color,gear):
        super().__init__(name, color)
        self.gear = gear  
         
    def showcar2(self): 
        print('Information : Name :', self.name, 'Color :', self.color, 'Gear :', self.gear)

x = NewCar("Lamborghini", "Yellow","Auto")
x.showcar2()