thistuple = ("apple", "banana", "cherry")
thislist = list(thistuple)
thislist.append("orange")
thistuple = tuple(thislist)

print(thistuple)