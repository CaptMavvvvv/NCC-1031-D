another_items = 'y'
while another_items == 'y':
    wholesale = float(input("Enter the item's wholesale cost: "))
    retail_price = wholesale * 2.5
    print(f'Retail price: ${retail_price:.2f}')
    another_items = input("Do you have another items? (Enter y for yes): ")