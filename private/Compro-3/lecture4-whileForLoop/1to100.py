cols = int(input("Enter number of columns: "))
for i in range(1, 101):
    print(i, end='\t')
    if i % cols == 0:
        print()