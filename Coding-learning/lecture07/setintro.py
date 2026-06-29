seta = {1, 2, 3, 4}
setb = set([8, 9, 10])

seta.add(5)
setb.update([6, 7])
Uset = seta | setb
print(Uset)
print(len(Uset))

setb.update('ABCD')
seta.update([6, 7, 8])
print(setb)

print(seta.intersection(setb))
print(seta ^ setb)

setb.remove('B')
setb.discard(10)
print(setb)
print(seta.clear())
for val in Uset:
    print(val)
    