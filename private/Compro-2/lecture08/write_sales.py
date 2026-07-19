num_days = int(input('For how many days do you have sales? '))
with open('sales.txt', 'w') as sales_file :
    for count in range(1, num_days + 1):
        sales = float(input(f'Enter the sales for day #{count}: '))
        sales_file.write(str(sales) + '\n')

    print('Data written to sales.txt.')