with open('sales.txt', 'r') as sales_file:
    for line in sales_file:
        amount = float(line)
        print(format(amount, '.2f'))