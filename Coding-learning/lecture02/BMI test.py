weight = float(input("Enter your weight in kilograms: "))
height = float(input("Enter your height in meters: "))
bmi = weight / (height * height)

print("Your BMI is: ", format(bmi, '.2f'))