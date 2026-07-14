thislist = ["apple", "banana", "cherry"]

#mylist = thislist.copy() #? Use the method '.copy'
#mylist = list(thislist) #? Use func 'list'
mylist = thislist[:] #? Use the slice ops (' : ')

print(mylist)