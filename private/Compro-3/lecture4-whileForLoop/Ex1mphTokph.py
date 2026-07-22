print("KPH\tMPH")
print("----------")
for kph in range(60, 130+1, 10):
    mph = kph * 0.6214
    print(f'{kph}\t{mph:.2f}')