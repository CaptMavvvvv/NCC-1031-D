print("***calculate sum of odd and even number (Exit press 0)***")

sum_even = 0
sum_odd = 0

while True:
        number = int(input("Enter number: "))
        if number == 0:
            break
        elif number % 2 == 0:
            sum_even += number
        else:
            sum_odd += number


print(f'sum of even numbers = {sum_even}')
print(f'sum of odd numbers = {sum_odd}')