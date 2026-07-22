rows =  int(input("How many rows: "))
columns = int(input("How many columns: "))
for i in range(rows):
    for j in range(columns):
        print("*", end="")
    print()