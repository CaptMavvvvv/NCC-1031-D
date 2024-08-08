inventory = [
    ["Apple", 50, 0.75],
    ["Banana", 100, 0.50],
    ["Orange", 75, 0.80]
]

def update_inventory(inventory, item_name, quantity_sold):
    for item in inventory:
        if item_name == item[0]:
            item[1] = item[1] - quantity_sold

def calcurate_total_value(inventory):
    for value in inventory:
        if value == value[1]:
            value[2] = value[2]
            print(value)
            

def find_most_expensive(inventory):
    pass

def add_item(inventory, item_name, quantity, price):
    pass

calcurate_total_value(inventory)
#update_inventory(inventory, "Banana", 20)
#print(inventory)