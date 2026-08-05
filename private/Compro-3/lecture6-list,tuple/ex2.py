inventory = [
    ["Apple", 50, 0.75]
    ["Banana", 100, 0.50]
    ["Orange", 75, 0.80]
]

def update_inventory(inventory, item_name, quantity_sold):
    for item in inventory:
        if item_name == item[0]:
            item[1] = item[1] - quantity_sold


def calculate_total_value(inventory):
    pass

def find_most_expensive(inventory):
    pass

def add_item(inventory, item_name, quantity, price):
    pass