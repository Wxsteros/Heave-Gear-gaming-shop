#ภาระกิจที่ 1
#เป็นโคดที่เกี่ยวกับการส่งข้อมูลออกทางหน้าจอ หรือที่เรียกว่า Output  โดยใช้คำสั่งprint และส่วนคำสั้ง\n คือการนำคำที่อยู่ต่อท้ายคำสั่งมาขึ้นบรรทัดใหม่
#print('Ktitikon\nKingwichit\n2\n673050379-2')

#ภาระกิจที่ 2
#ต่อมาโคดนี้เป็นที่เกี่ยวข้องกับการ รับข้อมูล(input)และและส่งออกข้อมูล(output)โดยโคดนี้จะเป็นได้ว่ามีตัวแปล2ตัวได้แก่ firstname และ hightschool 
#ซึ่งจะรับข้อมูลจากแป้นพิมพ์แล้วเก็บไว้ในตัวแปลและนำมาแสดงผลผ่านทางหน้าจอโดยใช้คำสั่งprintเหมือนกันโคดในข้อก่อนหน้า
#firstname=input('Entrt your name :')
#hightschool=inpu('Enter hight school name :')
#print(firstname)
#print(hightschool)

#ภาระกิจที่ 3
#โคดนี้เป็นการกำหนดค่าตัวแปลของ w,x,y,z แล้วนำมาแสดงผ่านทางหน้าจอผ่านการ print ถ้าเป็นข้อมูลประเภทตัวอักษร ถ้าใช้เครื่องหมายบวกยกตัวอย่างเช่นในบรรทัดที่ 
#print(x+y) x และ y ซึ่งเป็นข้อมูลประเภทตัวอักษรตอน output จะนำอักษรมาเรียงต่อกันและถ้าเป็นประเภทตัวเลขอย่างเช่นตัวแปล wและz ซึ่งถ้าprint(w+z)ะนำตัวเลขในตัวแปลมาบวกกัน
#w,x,y,z,= 5 , 'computer' , 'education' ,6
#print(x)
#print(y)
#print(x+y)
#print("I am student of"+x+""+y )
#print(w+z)

#ภาระกิจที่ 4
#firstname=input('Enter your name :')
#surname=input('Enter your ser name :')
#college_year=input('Enter your college :')
#student_id=input('Enter your studen id :')
#print(firstname)
#print(surname)
#print(college_year)
#print(student_id
#x="""Millions of fans are bidding farewell to Squid Game, the Emmy award-winning TV series that has topped Netflix's charts and become a symbol of South Korea's ascendance in Hollywood.
#The fictional show follows cash-strapped players as they battle it out in a series of traditional Korean children's games - with a gory twist, as losers are killed in every round.
#Squid Game has sucked in viewers since 2021 with its candy-coloured sets and bleak messages about capitalism and humanity. And with its third and final season released last Friday, fans across the world are returning to reality."""
#print(x)

#ภาระกิจที่ 5
#first_number=input('Enter your first number :')
#second_number=input('Enter your second number :')
#thirnd_number=input('Enter your thirnd number :')
#fourth_number=input('Enter your fourth number :')
#fiveth_number=input('Enter your fiveth number :')
#print('float of first number is ',float(first_number))
#print('complex of first number is',complex(first_number))
#print('float of second number is',float(second_number))
#print('complex of second number is',complex(second_number))
#print('float of thirnd number is',float(thirnd_number))
#print('complex of thirnd number is',complex(thirnd_number))
#rint('float of fourth number is',float(fourth_number))
#print('complex of fourth number is',complex(fourth_number))
#print('float of fiveth number is',float(fiveth_number))
#print('complex of fiveth number is',complex(fiveth_number))

#ภาระกิจที่ 6
#number1=input('Enter first number :')
#number2=input('Enter second number :')
#print('number1 = number2 is' ,number1==number2)

#โปรแกรมรับค่าอายุ
my_age=input('Input your age')
my_friend_age=input('Input your friend age')
if my_age > my_friend_age :
    print('I am older than you !!')
else :
    print("No, you older than me")