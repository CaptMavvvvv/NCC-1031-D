fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
newlist = [i for i in fruits if i != "apple"]
print(newlist)

#? > เงิ่อนไช if i != "apple" จะคืนค่า True ให้กับทุกค่ายกเว้น "apple" และก็จะได้ลิสต์ใหม่ที่มีทุกค่ายกเว้น "apple"