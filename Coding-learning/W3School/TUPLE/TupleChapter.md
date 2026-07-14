# Python Tuple - รายการแบบคงที่ แก้ไขไม่ได้


#### Tuple Characteristic   
> สร้างด้วยวงเล็บโค้ง ( )
> มีลำดับ (Ordered): อ้างอิงตำแหน่งด้วย Index ได้เหมือน List
> แก้ไขไม่ได้ (Immutable): เมื่อสร้างแล้ว ห้ามเพิ่ม ลบ หรือเปลี่ยนค่าเด็ดขาด (ล็อคตายตัว)
> ซ้ำได้ (Allow Duplicates): เก็บข้อมูลซ้ำกันได้
> เหมาะสำหรับ: เก็บข้อมูลที่ไม่ต้องการให้ใครมาแก้ไขระหว่างรันโปรแกรมเพื่อความปลอดภัย เช่น พิกัดละติจูด/ลองจิจูด (13.7563, 100.5018) หรือค่าสี RGB


#### Example of simple tuple
```python
thistuple = ("apple",) > this is Tuple
thistuple = ("apple") > this is not Tuple
```


### Access Tuple
__มีทั้งแบบ Positive และ Negative__
```python
print(thistuple[1])
print(thistuple[0:2])
print(thistuple[:1])
print(thistuple[-1])
```

### Update Tuple
__โดยปกติ tuple ไม่สามารถเปลี่ยนแปลงไอเท็มที่อยู่ใน tuple ได้ แต่มันมีทางอื่นที่ทำได้__
1. add : เปลี่ยน tuple เป็น list และค่อยแปลง list กลับมาเป็น tuple
```python
x = ("apple", "banana", "cherry")
y = list(x) # แปลง x เป็น list ไปเก็บในตัวแปร y
y[2] = "mango" # แทรกค่าที่กำหนดเข้าไป
x = tuple(y) # แปลง y กลับมาเป็น tuple ไปใส่ใน x
```
2. append : เปลี่ยนกลับมาเป็น list ใช้ append แล้วค่อยแปลงเป็น tuple
```python
thistuple = ("apple", "banana", "cherry")
thislist = list(thistuple)
thislist.append("orange")
thistuple = tuple(thislist)
```
3. Add Items ด้วย tuple : โดยการสร้าง tuple ขึ้นมาอีกตัว และนำไป += เพื่อบวกค่าเข้าไป (* tuple ต้องเป็นแบบมี , เท่านั้น *)
```python
thistuple = ("apple", "banana", "cherry")
y = ("orange",) # สร้างตัวแปรที่มีค่า tuple อยู่ข้างใน สังเกต "orange",
thistuple += y # เพิ่มค่า tuple เข้าไปโดยใช้ +=
```
4. remove : เปลี่ยนกลับมาเป็น list ใช้ remove แล้วค่อยแปลงเป็น tuple
```python
thistuple = ("apple", "banana", "cherry")
x = list(thistuple)
x.remove("banana")
thistuple = tuple(x)
```


### Unpack Tuple
> การกำหนดค่า เรียกว่า 'packing'
> การดึงค่ากลับมาไว้ในตัวแปร เรียกว่า 'unpacking'
ตัวอย่างการ extract จาก tuple
```python
fruits = ("apple", "banana", "cherry")
(green, yellow, red) = fruits
print(green)
print(yellow)
print(red)
```
> ถ้าตัวแปรน้อยกว่าจำนวนค่า สามารถใช้ * นำหน้าชื่อตัวแปร และค่าเหล่านั้น จะถูกจัดในรูปแบบ list
```python 
(green, yellow, *red) = fruits
```


### Tuple Methods
> count() = output ค่าที่นับได้ใน tuple
> index() = หาค่าที่ระบุและคืนค่าที่พบตามระบุ