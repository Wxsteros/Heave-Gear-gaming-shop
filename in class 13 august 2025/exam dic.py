dictionary = []
def add_word():
    word = input("เพิ่มคำศัพท์ : ")
    wordtype = input("ชนิดคำ (n. , v. , adj. , adv.) : ")
    meaning = input("ความหมาย : ")
    dictionary.append([word,wordtype,meaning])
    print("คำศัพท์ถูกเพิ่มเรียบร้อยแล้ว")

def show_words():
    count = 0
    i=0
    for i in dictionary:
        count += 1
    print('{0:-<50}'.format(""))
    print('{0:^50}'.format(f'คำศัพท์มีทั้งหมด {count} คำ'))
    print('{0:-<50}'.format(""))       
    print('{0:<20}{1:<20}{2:<20}'.format("คำศัพท์", "ประเภท", "ความหมาย"))
    for vocap in dictionary:
        print('{0:<20}{1:<20}{2:<20}'.format(vocap[0], vocap[1], vocap[2]))
        

def delete_word():
    show_words()
    delword = input("คำศัพท์ที่ต้องการลบ: ")
    found = False
    for vocap in dictionary:
        if vocap[0] == delword:
            confirm = input(f"คุณต้องการลบ {delword} ใช่หรือไม่ (y/n): ")
            if confirm.lower() == "y":
                dictionary.remove(vocap)
                print('ลบคำศัพท์นี้เรียบร้อยแล้ว')
                show_words()
            else:
                print('ยกเลิกการลบคำศัพท์นี้')
            found = True
            break
    if not found:
        print("ไม่พบคำศัพท์นี้")
while True : 
    print('{0:-<50}'.format(""))
    print('{0:^50}'.format('dictionary program'))
    print('{0:-<50}'.format(""))
    print("1.เพิ่มคำศัพท์\n2.แสดงคำศัพท์\n3.ลบคำศัพท์\n4.ออกจากโปรแกรม")
    print('{0:-<50}'.format(""))
    selec=str(input("selec menu :"))
    if selec == "1":
        add_word()
    elif selec=="2":
        show_words()
    elif selec =="3":
        delete_word()
    elif selec =="4":
        confirm = input("คุณต้องการจะออกจากโปรแกรมหรือไม่ (y/n): ")
        confirm = confirm.lower()
        if confirm == 'y':
            print("ออกจากโปรแกรมเรียบร้อย")
            break
        elif confirm == 'n':
            continue 