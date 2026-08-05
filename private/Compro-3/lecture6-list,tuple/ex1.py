heroes = ['Ironman', 'Thor', 'Hulk', 'Spiderman']

def display_heroes():
    if not heroes:
        print("The hero list is currently empty.")
        return
    print("Current heroes:")
    for index, hero in enumerate(heroes, start=1):
        print(f"{index}. {hero}")


def add_heroes():
    user_add = input("Please enter the hero you want to add: ").strip()
    if user_add:
        heroes.append(user_add)
        print(f"{user_add} has been added.")
    else:
        print("No hero entered. Nothing was added.")


def insert_heroes():
    try:
        user_pos = int(input("Please enter the position in the list where you want to insert: "))
        user_insert = input("Please enter the hero you want to insert: ").strip()
        if not user_insert:
            print("No hero entered. Nothing was inserted.")
            return
        insert_index = max(0, min(user_pos - 1, len(heroes)))
        heroes.insert(insert_index, user_insert)
        print(f"{user_insert} has been inserted at position {insert_index + 1}.")
    except ValueError:
        print("Invalid position. Please enter a number.")


def remove_heroes():
    if not heroes:
        print("The hero list is empty. There is nothing to remove.")
        return
    user_remove = input("Please enter the hero you want to remove: ").strip()
    if user_remove in heroes:
        heroes.remove(user_remove)
        print(f"{user_remove} has been removed.")
    else:
        print(f"{user_remove} is not in the hero list.")


def display_sorted_heroes():
    if not heroes:
        print("The hero list is currently empty.")
        return
    order = input("Enter 'A' for ascending or 'D' for descending sort: ").strip().lower()
    if order == 'd':
        sorted_heroes = sorted(heroes, reverse=True)
        print("Heroes sorted descending:")
    else:
        sorted_heroes = sorted(heroes)
        print("Heroes sorted ascending:")
    for index, hero in enumerate(sorted_heroes, start=1):
        print(f"{index}. {hero}")


user_choice = 'y'
while user_choice.lower() == 'y':
    user_ops = input('''Please enter the operation
1. Display Heroes
2. Add Heroes
3. Insert Heroes
4. Remove Heroes
5. Display Sorted Heroes (Ascending / Descending)
Enter choice: ''').strip()

    if user_ops == '1':
        display_heroes()
    elif user_ops == '2':
        add_heroes()
    elif user_ops == '3':
        insert_heroes()
    elif user_ops == '4':
        remove_heroes()
    elif user_ops == '5':
        display_sorted_heroes()
    else:
        print("Invalid option. Please choose a number from 1 to 5.")

    user_choice = input("Do you want another operation? (y for yes): ").strip()

print("Goodbye!")