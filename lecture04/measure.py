print('----------------')
print('KPH\t\tMPH')
print('----------------')

for kph in range(60, 131):
    mph = kph * 0.6214
    print(kph, '\t\t', format(float(mph), ',.1f'))