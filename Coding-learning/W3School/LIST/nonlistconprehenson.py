fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
newlist = []

''' Loop for ข้างล่างเป็นการเช็คว่า หากคำใด ๆ ในลิสต์มีตัว "a" ประกอบ
    มันจะถูกยัดไปใส่ใน newlist ด้วยคำสั่ง append'''
for x in fruits:
    if "a" in x:
        newlist.append(x)

print(newlist)