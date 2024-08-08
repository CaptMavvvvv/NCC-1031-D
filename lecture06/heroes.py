heroes = ['Ironman', 'Thor', 'Hulk', 'Spiderman']

def display_heroes():
    print(heroes)

def add_heroes():
    global heroes
    heroes_add = input("Pls input new heroes: ")
    heroes.append(heroes_add)
    print(heroes)

def insert_heroes():
    global heroes
    pass

display_heroes()
add_heroes()