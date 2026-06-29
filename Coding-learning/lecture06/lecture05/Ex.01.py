def is_armstrong(num):
    digits = str(num)
    power = len(digits)
    total = 0
    for digit in digits:
        total = total + int(digit)**power

    if total == num:
        return True
    else:
        return False
    
print(is_armstrong(153))
print(is_armstrong(9474))
print(is_armstrong(123))

