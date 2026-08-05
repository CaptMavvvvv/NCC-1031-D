# Python List

## List Characteristic
> ลิสต์ (List) เป็นแบบ __เปลี่ยนแปลงได้ (mutable)__ หมายความว่าโปรแกรมสามารถเปลี่ยนแปลงเนื้อหาภายในลิสต์ได้
> เรียงเป็นลำดับ, เปลี่ยนแปลงค่าได้, เก็บข้อมูลได้ทุกประเภท

### List Methods
- append(): เพิ่มค่า 1 ค่าไปที่ท้าย List
- extend(): เพิ่มสมาชิกทั้งหมดจาก List อื่นไปท้าย List ปัจจุบัน
- insert(): แทรกค่าที่ตำแหน่งที่ระบุ
- remove(): ลบค่าที่พบครั้งแรกของค่าที่ระบุ
- pop(): ลบและคืนค่าจากตำแหน่งที่ระบุ
- index(): คืนค่าตำแหน่งแรกที่พบค่าที่ระบุ
- count(): นับจำนวนครั้งที่ปรากฎใน List
- clear(): ลบค่าทั้งหมดใน List
- sort(): จัดเรียงค่าจากน้อยไปมาก
- reverse(): สลับลำดับของสมาชิกใน List

### Methods Append
append() ใช้เพิ่มค่าหนึ่งค่าไปที่ท้ายของ List ซึ่งจะช่วยให้สามารถเพิ่มสมาชิกได้แบบ Dynamic และสมาชิกใหม่จะถูกเพิ่มต่อท้ายเสมอ
```python
fruits = ["apple", "banana", "cherry"]
more_fruits = ["mango", "pineapple"]
for fruit in more_fruits:
    fruits.append(fruit)
print(f'Fruits after append: {fruits}')
```

### Methods Insert
```python
berries = ["raspberry", "blackberry"]
berries.insert(1, "strawberry")
berries.insert(2, "blueberry")
print(f'Berries after insert: {berries}')
```

### Methods Remove
```python
fruits_with_dup = ["apple", "banana", "apple", "cherry", "apple", "kiwi"]
while "apple" in fruits_with_dup:
    fruits_with_dup.remove("apple")
print(f'Fruits after remove: {fruits_with_dup}')
```

### Methods Index
```python
animals = ["cat", "dog", "rabbit", "hamster", "dog", "parrot"]
fist_dog_index = animals.index("dog")
print(f'The first occurrence of "dog" is at index: {first_dog_index}')
second_dog_index = animals.index("dog", first_dog_index + 1)
print(f'The second occurrence of "dog" is at index: {second_dog_index}')
```

### Summary of all Methods
```python
heroes = ['Ironman', 'Thor', 'Hulk', 'Superman', 'Spiderman']
h2 = ['Dr.Stange', 'Cpt.America', 'Black Panther', 'Ant Man']

heroes.insert(0, h2[0])
print(heroes.index('Thor'), h2[1])
heroes.insert(heroes.index('Thor'), h2[1])
print(heroes)
heroes.remove('Superman')
heroes.append('Ant Man')
print(heroes)
heroes.sort()
print(heroes)
heroes.reverse()
print(heroes)
newheroes = heroes
newheroes[0] = 'Wonder Women'
print(heroes)
copyheroes = [] + heroes
print(copyheroes)
copyheroes[0] = 'Hanuman'
print(heroes)
print(copyheroes)
```
