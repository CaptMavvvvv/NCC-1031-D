try:
    value = int(input("Enter a number: "))
    result = 10 / value
except ValueError:
    print('Invalid input')
except ZeroDivisionError:
    print('Cannot divide by zero')
else:
    print(f'The result is {result}')
finally:
    print("Execution completed")