x = ("apple", "banana", "cherry")
y = list(x)
y[2] = "mango"
x = tuple(y)

print(x)