with open('sales.txt', 'r') as sales_file:
    line = sales_file.readline()
    while line != '':
        amount = float(line)
        print(format(amount, '.2f'))
        line = sales_file.readline()
         