print("*** Calculate the sum between start and stop number ***")

x = int(input("Enter the start number: "))
y = int(input("Enter the end number: "))

result = 0
for i in range(x, y + 1):
    result += i

print(f'The sum from {x} to {y} is: {result}')
