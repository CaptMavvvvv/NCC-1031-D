def add(first, second):
    result = first + second
    print(f'{first} + {second} = {result}')
def subtract(first, second):
    result = first - second
    print(f'{first} - {second} = {result}')
def multiply(first, second):
    result = first * second
    print(f'{first} * {second} = {result}')
def divide(first, second):
    result = first, second
    print(f'{first} / {second} = {result}')

print(f'''Please select operation
      1.Add
      2.Subtract
      3.Multiply
      4.Divide''')
userOps = int(input(f'Select operation form 1,2,3,4 : '))
first, second = int(input(f'Enter first number: ')), int(input(f'Enter second number: '))
if userOps == 1:
    add(first, second)
elif userOps == 2:
    subtract(first, second)
elif userOps == 3:
    multiply(first, second)
elif userOps == 4:
    divide(first, second)
else:
    print(f'Please select the valid values')