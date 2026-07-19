m = int(input("Enter your loan: "))
if m <= 1000:
    i = m*0.1
elif m <= 10000:
    i = m*0.05
else:
    i = m*0.02
print(f'total loan you need to return is: {m+i}')