fruits = ["apple", "banana", "cherry", "kiwi", "mango"]

#newlist = [x.upper() for x in fruits]
#newlist = ['hello' for x in fruits]

newlist = [x if x != "banana" else "orange" for x in fruits]
#! ตัวอย่างนี้คือ คืนค่าเดิมถ้าค่านั้นไม่ใช่ banana ถ้าค่าใด ๆ เป็น banana จะถูกคืนค่าเป็น orange
print(newlist)