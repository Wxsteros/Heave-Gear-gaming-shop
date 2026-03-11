basket = []  
def Nike() :
    while True:
        print("-------------- Nike --------------")
        print('{0:<5}{1:<20}{2:<10}'.format('[1]','Air Max 97','5800' ))
        print('{0:<5}{1:<20}{2:<10}'.format('[2]','Air jordan 1','3600' ))
        print('{0:<5}{1:<20}{2:<10}'.format('[3]','Epic react flyknit','5600' ))
        print('{0:<5}{1:<20}{2:<10}'.format('[x]','return to menu','',''))
        print("-----------------------------------")
        y = str(input("select Nike shoes : "))
        y = y.lower()
        if y == "1":    
            basket.append(["Air Max 97",5800])
        elif y == "2":           
            basket.append(["Air jordan 1",3600])    
        elif y == "3":
            basket.append(["Epic react flyknit",5600])
        elif y == "x":  
            break       
def Adidas() :  
    while True:
        print("-------------- Adidas--------------")
        print('{0:<5}{1:<20}{2:<10}'.format('[1]','Super Star','3200' ))
        print('{0:<5}{1:<20}{2:<10}'.format('[2]','Ultras Booth','7900' ))
        print('{0:<5}{1:<20}{2:<10}'.format('[3]','Nemezis','2350' ))
        print('{0:<5}{1:<20}{2:<10}'.format('[x]','return to menu','',''))
        print("-----------------------------------")
        y = str(input("select Adidas shoes : "))
        y = y.lower()
        if y == "1":    
            basket.append(["Super Star",3200])  
        elif y == "2":
            basket.append(["Ultras Booth",7900])
        elif y == "3":
            basket.append(["Nemezis",2350])
        elif y == "x":
            break          
def Reebox() :
    while True:
        print("-------------- Reebox --------------")
        print('{0:<5}{1:<20}{2:<10}'.format('[1]','Energy Driftium','1690' ))
        print('{0:<5}{1:<20}{2:<10}'.format('[2]','Royal Bridge','2190' ))
        print('{0:<5}{1:<20}{2:<10}'.format('[3]','Fabukista Mid II','1190' ))
        print('{0:<5}{1:<20}{2:<10}'.format('[x]','return to menu','',''))
        print("-----------------------------------")
        y = str(input("select Reebox shoes : "))
        y = y.lower()
        if y == "1":
            basket.append(["Energy Driftium",1690])
        elif y == "2":                                      
            basket.append(["Royal Bridge",2190])
        elif y == "3":
            basket.append(["Fabukista Mid II",1190])
        elif y == "x":     
            break
def puma():
    while True:
        print("-------------- Puma --------------")
        print('{0:<5}{1:<20}{2:<10}'.format('[1]','Speedcat Leather','4200' ))
        print('{0:<5}{1:<20}{2:<10}'.format('[2]','Speedcat OG','3600' ))
        print('{0:<5}{1:<20}{2:<10}'.format('[3]','Suede XL','4000' ))
        print('{0:<5}{1:<20}{2:<10}'.format('[x]','return to menu','',''))
        print("-----------------------------------")
        y = str(input("select Puma shoes : "))
        y = y.lower()
        if y == "1":
            basket.append(["Speedcat Leather",4200])
        elif y == "2":                                      
            basket.append(["speedcat OG",3600])
        elif y == "3":
            basket.append(["Suede XL",4000])
        elif y == "x":     
            break
def converse():
    while True:
        print("-------------- Converse --------------")
        print('{0:<5}{1:<25}{2:<10}'.format('[1]','Chuck Taylor All Star','3200' ))
        print('{0:<5}{1:<25}{2:<10}'.format('[2]','Star Player 76 Suede','3200' ))
        print('{0:<5}{1:<25}{2:<10}'.format('[3]','Jack Purcell Pro Ox','4000' ))
        print('{0:<5}{1:<25}{2:<10}'.format('[x]','return to menu','',''))
        print("--------------------------------------")
        y = str(input("select Converse shoes : "))
        y = y.lower()
        if y == "1":
            basket.append(["Chuck Taylor All Star",3200])
        elif y == "2":                                      
            basket.append(["Star Player 76 Suede",3200])
        elif y == "3":
            basket.append(["Jack Purcell Pro Ox",4000])
        elif y == "x":     
            break
def show():
        print('{0:<5}{1:<20}{2:<10}{3:<14}{4:<15}'.format('', '', 'Shopping list', '', ''))
        print('{0:-<70}'.format(""))  # หัวตาราง
        print('{0:<5}{1:<25}{2:<10}{3:<14}{4:<15}'.format('NO', 'Name', 'Price', 'Discount', 'Discount_Price'))  # รายการในตาราง
        print('{0:-<70}'.format(""))  # หัวตาราง
        total = 0
        SDiscount = 0
        SDiscount_Price = 0 
        i=1
        for item in basket:
            name = item[0]
            price = item[1]
            Discount = price * 0.2
            Discount_Price = price - Discount
            SDiscount+= Discount
            SDiscount_Price += Discount_Price
            total += price
            print('{0:<5}{1:<25}{2:<10}{3:<14}{4:<15}'.format(i, name, price, Discount, Discount_Price))
            i += 1
        print('{0:-<70}'.format(""))  
        print('{0:<5}{1:<25}{2:<10}{3:<14}{4:<15}'.format('', 'total price', total, SDiscount , SDiscount_Price))  
        print('{0:-<70}'.format(""))         
while True: 
    print("-------------- Select shoes --------------")
    print("[1] Nike\n[2] Adidas\n[3] Reebox\n[4] Puma\n[5] converse\n[s] Show basket\n[x] Exit")    
    shose = str(input("select menu: "))
    shose = shose.lower()
    if shose == "1":
        Nike()          
    elif shose == "2":
        Adidas()
    elif shose == "3":
        Reebox()
    elif shose == "4":
        puma()
    elif shose == "5":
        converse()
    elif shose == "s": 
        show()     
    elif shose == "x":  
        confirm = input("Do you want to exit? (y/n): ")
        confirm = confirm.lower()
        if confirm == 'y':
            print("Thank you for shopping")
            break
        elif confirm == 'n':
            continue