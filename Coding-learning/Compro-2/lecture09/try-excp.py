y = int(input("Enter a number: "))
try:
    x = 1/ y
    print(x)
except ZeroDivisionError as e:
    print(f"Error: {e}")

print("End of program")