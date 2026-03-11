class car:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        
    def show(self):
        print("car Information")
        print("name:", self.name)
        print("color:", self.color)

Mastang = car("Mastang", "Red")
Mastang.color='black'
Mastang.show()

BMW = car("BMW", "White")
BMW.color='black'
BMW.show()