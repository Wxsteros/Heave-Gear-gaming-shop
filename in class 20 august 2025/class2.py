class Car :
    def __init__(self, name, color):
        self.name = name
        self.color = color

x = Car("Civic","Black")
print(x.name)
print(x.color)

class Car :
    def __init__(self, name, color):
        self.name = name
        self.color = color
        
    def show(self):
        print("car Information")
        print("name:", self.name)
        print("color:", self.color)

x = Car("accord", "Black")
x.show()