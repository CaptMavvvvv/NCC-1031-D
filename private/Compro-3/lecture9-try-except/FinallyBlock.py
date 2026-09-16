try:
    numerator = float(input("Enter the numerator: "))
    denominator = float(input("Enter the denominator: "))
    result = numerator / denominator
    print(f'The result is: {result}')
except ZeroDivisionError:
    print("Error: You cannot divide by zero")
except ValueError:
    print("Error: Invalid input. Pls enter numeric values")
finally:
    print("Execution completed, whether an exception occurred or not")
print('End')