num1 = int(input("Enter the number of hours worked: "))
num2 = int(input("Enter the hourly pay late: "))

if num1 > 40:
    print("The gross pay is",(40*num2)+(num2*1.5)*(num1-40))
else:
    print("The gross pay is", num1*num2)