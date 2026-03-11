#for loop 
names=['a','b','c','d']
for x in names:
    print(x) 
       
names='python'
for x in names:
    print(x)

for x in range(5):
    print(x)

a=list(range(10)) #[0,1,2,3,4,5,6,7,8,9]
b=list(range(5,11))#[5,6,7,8,9,10]
c=list(range(0,10,2))#[0,2,4,6,8]
d=list(range(0,-10,-2))#[0,-2,-4,-6,-8]

department=["COMED","SCIED","MATHED"]
uiniversity=["KKU","CMU","CU"]
for x in department:
    for y in uiniversity:
        print(x +" "+ y)