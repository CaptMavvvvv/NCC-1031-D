print ("""pls select operation
       1.add
       2.subtract
       3.multiply
       4.divide
       """)
opt = int(input("Select operations form: "))
first_num = float(input("Enter first number: "))
second_num = float(input("Enter second number: "))

if opt == 1:
    print(first_num + second_num)
elif opt == 2:
    print(first_num - second_num)
elif opt == 3:
    print(first_num * second_num)
elif opt == 4:
    print(first_num / second_num)
else:
    print("There's not an option")