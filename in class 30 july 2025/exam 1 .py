#โปรแกรรับชื่ออาหาร
i=0
y=1
fev_food=[]
while True:
    food = str(input(f"อาหารโปรดของคุณอันดับที่ {i+1} คือ :" ))
    fev_food.append(food)
    i += 1
    if food == ("exit"): 
        break
print("--------------------")
fev_food.pop()
for x in fev_food:
    print(f"รายการอาหารโปรดของคุณมีดังนี้ {y} คือ : {x}")
    y += 1