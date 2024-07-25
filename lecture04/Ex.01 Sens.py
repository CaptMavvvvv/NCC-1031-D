keep = 'y' or 'Y'

while keep == 'y' or 'Y':
    wholesale = float(input("Enter the item's wholesale price: "))
    price = wholesale * 2.5

    print("The profit is $", price)
    keep = input('Do you have another item? (Enter y,Y for yes): ')