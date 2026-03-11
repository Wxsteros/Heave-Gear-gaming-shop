print("-" * 50) 
print("โปรแกรมหยิบสินค้าใส่ตะกร้า")
print("-" * 50)

# ตะกร้าที่ไว้เก็บสินค้า 
basket = []
# รับชื่อสินค้า
item1 = input("หยิบสินค้า ชิ้นที่ 1 :")
basket.append(item1)
item2 = input("หยิบสินค้า ชิ้นที่ 2 :")
basket.append(item2)
item3 = input("หยิบสินค้า ชิ้นที่ 3 :")
basket.append(item3)
item4 = input("หยิบสินค้า ชิ้นที่ 4 :")
basket.append(item4)
item5 = input("หยิบสินค้า ชิ้นที่ 5 :")
basket.append(item5)
print("-" * 50)
#แสดงชื่อสินค้า
print("\nสินค้าในตะกร้ามีดังนี้")
print ("1.",basket[0])
print ("2.",basket[1])
print ("3.",basket[2])
print ("4.",basket[3])
print ("5.",basket[4])