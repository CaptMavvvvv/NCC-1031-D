thislist = ["apple", "banana", "cherry"]
tropical = ["mango", "papaya"]
thislist.append("orange") #! นำไปต่อท้าย list
thislist.insert(1, "pineapple") #! เอาไปแทรกในตำแหน่งที่กำหนด insert(position, "word to insert")
thislist.extend(tropical) #! เอา list ที่กำหนดเพิ่มมาต่อท้าย list เดิม
print(thislist)