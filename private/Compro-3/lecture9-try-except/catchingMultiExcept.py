try:
    value = int(input("Enter a number: "))
    result = 10 / value
except ValueError:
    print('Invalid input! Pls enter a number')
except ZeroDivisionError:
    print('Cannot divide by zero')
print("End")