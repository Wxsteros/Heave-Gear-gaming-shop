x=int(input("input your number : "))
if x % 3 == 0:
    print("Fizz")
elif x % 5 == 0:
    print("Buzz")
elif x % 15 == 0 :
    print("Fizz - Buzz")

#if แบบย่อ 
me=24
myfriend=30 
print('I am older than you !!') if me > myfriend else print("No !!")
#หรือมากกว่า2 เงื่อนไขได้แต่ไม่สามารถใช้ elif ในรูปแบบย่อได้
x,y=24,30
print('older') if x > y else print("Equal") if x==y else print ("No !!")

x = int(input("Enter your age :"))
if x >= 7:
   if x <= 12: 
     print("Elementary School")
   elif x <= 18:
     print("High School")
   else:
     print("Older")
else:
    print("Pre-School")