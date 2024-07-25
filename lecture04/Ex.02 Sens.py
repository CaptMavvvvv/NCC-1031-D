rows = int(input("How many rows? "))
columns = int(input("How many columns? "))

while rows <= 0 or columns <= 0:
    print("The number of rows and columns should be positive.")
    rows = int(input("How many rows? "))
    columns = int(input("How many columns? "))

for i in range(rows):
    row_asterisks = []
    for j in range(columns):
        row_asterisks.append('*')
    print(" ".join(row_asterisks))