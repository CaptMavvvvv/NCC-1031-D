def myfunc(n):
    return abs(n - 50)

thislist = [100, 50, 65, 82, 23]
thislist.sort(key = myfunc)
print(thislist)

#? > สามารถนำ Function มาใช้ได้ในการ Sort ด้วยคำสั่ง key = function