Tems = float(input("Enter temperature in Celsius: "))
fahrenheit = (Tems * 9/5) + 32
kelvin = (fahrenheit - 32) * (5.0/9.0) + 273.15

print("Temperature in Fahrenheit is", format(fahrenheit, '.2f'))
print("Temperature in Kelvin is", format(kelvin, '.2f'))