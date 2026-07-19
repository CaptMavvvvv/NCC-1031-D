travel_range = int(input("Enter your travel range: "))
cartype = str(input("Enter your car type: "))


rangegas = gas
rangeev = ev

if cartype == gas:
    print(f'Total cost in range is: {rangegas}')
else:
    print(f'Total cost in range is: {rangeev}')