
class Nike:
    def __init__(self):
        self.product = [['Nike Air Max',3500],['Nike Zoom',4000],['Nike React',3000],['Nike Air Force',4500]]
        
    def show_item(self):
        if not self.product:
            print("ไม่มีรายการสินค้า")
        else:
            print('{0:-<40}'.format(""))
            print('{0:<13}{1:<17}{2:>8}'.format('ลำดับ','name','price'))
            print('{0:-<40}'.format(""))
            i = 1
            for item in self.product:
                print('{0:<6}{1:<22}{2:>8}'.format(i,item[0],item[1]))
                i += 1

    def add_item(self):
        while True:
            name = input("ชื่อสินค้า: ")
            price = int(input("ราคาสินค้า: "))
            self.product.append([name, price])
            print('เพิ่มสินค้านี้เรียบร้อยแล้ว')
            self.show_item()
            more = input("ต้องการเพิ่มสินค้าอีกหรือไม่ (y/n): ").lower()
            if more == 'y':
                continue
            elif more == 'n':
                break
           
    def delete_item(self):
        self.show_item()
        del_item = input("ชื่อสินค้าที่ต้องการลบ: ")
        for item in self.product:
            if item[0] == del_item:
                confirm = input(f"คุณต้องการลบ {del_item} ใช่หรือไม่ (y/n): ")
                if confirm.lower() == "y":
                    self.product.remove(item)
                    print('ลบสินค้านี้เรียบร้อยแล้ว')
                    self.show_item()
                else:
                    print('ยกเลิกการลบสินค้า')
                return
    
    def menu(self):
        while True:
            print('{0:-<40}'.format(""))
            print('{0:<30}{1:>5}'.format("แสดงรายการสินค้า","[a]"))
            print('{0:<32}{1:>5}'.format("เพิ่มรายการสินค้า","[s]"))
            print('{0:<30}{1:>5}'.format("ลบรายการสินค้า","[d]"))
            print('{0:<28}{1:>5}'.format("ออกจากโปรแกรม","[x]"))
            print('{0:-<40}'.format(""))
            selec = str(input("เลือกคำสั่ง: ")).lower()
            if selec == 'a':
                self.show_item()
            elif selec == 's':  
                self.add_item()
            elif selec == 'd':
                self.delete_item()
            elif selec == 'x':
                confirm = input("คุณต้องการจะออกจากโปรแกรมหรือไม่ (y/n): ").lower()
                if confirm == 'y':
                    print("ออกจากโปรแกรมเรียบร้อย")
                    break
                elif confirm == 'n':
                    continue 
my_store = Nike()
my_store.menu()