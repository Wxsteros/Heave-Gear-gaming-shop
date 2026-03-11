#def standaerd_arg(arg): #เรียกใช้งานได้ทั้ง positional argument และ keyword argument 
#    print(arg)
#standaerd_arg(1)
#standaerd_arg(arg=2006)

#def possition_only(arg,/): 
#      print (arg)
#possition_only(1)
#possition_only(arg=1)

#def keyword_only(*,arg):
#    print(arg)
#keyword_only(arg=2006)

def combined(pos_only , / , standard , *, ked_only):
    print(pos_only,standard,ked_only)
#combined(1,2,3)
combined('North',4,ked_only=2006)
combined(1,standard=2,ked_only=3)

def exponents (base,power):
    return base**power 
print (exponents(2,3))

#exam 2*3.14*r
def circle(r,pi=3.14):
    return pi*r**2
print(circle(21))
    
def triagle(base,high):
    return 0.5*base*high
print(triagle(4,6))

def squar_kangmoo(base1,base2,high):
    return 0.5*(base1+base2)*high
print(squar_kangmoo(6,8,10))
