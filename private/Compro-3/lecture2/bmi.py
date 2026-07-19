weight, height = float(input(f'Enter your weight in kilograms: ')), float(input(f'Enter your height in meters: '))
bmi = weight / (height ** 2)
print(f'Your BMI is {bmi:.2f}')