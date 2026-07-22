print("MPH\tKPH")
print("-----------")
for mph in range(60, 130+1, 10):
    kph = mph / 0.6214
    print(f'{mph}\t{kph:.2f}')