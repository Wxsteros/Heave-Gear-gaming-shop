try:
    print("Hello"+5)
except:
    print("Error")

try:
    print("Hello"+"hi")
except:
    print("Error")
else:
    print("No Error")
finally:
    print("Finish")