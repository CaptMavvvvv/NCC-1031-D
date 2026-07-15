x = 10
y = 20
z = 30
if x < y and y < z:
    print(f'x is less than y and y is less than z')
elif x < y or y > z:
    print(f'Either x is less than y or y is greater than z')
elif not (x > y):
    print(f'x is not greater than y')