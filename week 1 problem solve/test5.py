print("***Convert BMI***")

w = int(input("Enter your weight (kg): "))
h = int(input("Enter your height (m): "))

BMI = w/(h**2)

print(f'Your BMI is: {BMI:.5f}')