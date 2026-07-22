# Python For Loops
---

## For loop Characteristic
__เป็นลูปประเภท "Collection-Controlled Loop" หรือ "Count-Controlled Loop" คือมันจะทำหน้าที่ "เดินเหยียบไปบนสมาชิกทีละตัว" (Iterate) ในวัตถุหรือชุดข้อมูลที่เรากำหนดไว้จนครบถ้วน__
*__ # เหมาะกับสถานการณ์ที่ทราบจำนวนครั้งในการวนซ้ำล่วงหน้า__*

### Basic For loop Syntax
```python
fruits = ["apple", "banana", "cherry"]
for x in fruits: # แทนค่า fruits เป็น x
    print(x)
```

### Break Statement
> 'Break' สามารถหยุดลูปก่อนที่จะวนซ้ำทุกรายการในลูปได้
```python
fruits = ["apple", "banana", "cherry"]
for x in fruits:
    print(x) # print ก่อนค่อยเช็คการ break
    if x == "banana":
        break

for x in fruits:
    if x == "banana": # เช็คการ break ก่อนค่อย print
        break
    print(x)
```

### Continue Statement
> 'Continue' สามารถให้เราหยุดการลูปในปัจจุบัน และทำคำสั่งถัดไปได้
```python
fruits = ["apple", "banana", "cherry"]
for x in fruits:
    if x == "banana":
        continue
    print(x)
```

### Range() Function
- Range() สามารถให้เรารันลูปตามจำนวนที่เราใส่ลงไปได้ ว่าอยากให้เริ่มต้นหรือสิ้นสุดที่เท่าไหร่
- ค่า Default ของ Range() จะส่ง output เริ่มต้นเป็น 0 และเพิ่มทีละ 1 และสิ้นสุดในเลขที่กำหนด
```python
for x in range(6):
    print(x)
```
---
หรือจะเป็นการกำหนด Parameter เลขเริ่มต้นและเลขที่จะสิ้นสุด
```python
for x in range(2, 6): # Remark ไว้ว่ามันจะไม่รันไปถึงเลข 6
    print(x)
```
---
หรือจะกำหนดการเพิ่มขึ้นของตัวเลขก็ได้ ว่าอยากให้เพิ่มทีละเท่าไหร่ (default คือ เพิ่มที่ละ 1)
```python
for x in range(2, 30, 3): # เพิ่มทีละ 3 ใน parameter สุดท้าย
    print(x)
```

### Else in For loop
- else จะทำงานเมื่อสิ้นสุดลูปแล้วเท่านั้น
ตัวอย่าง : ถูกรันเมื่อสิ้นสุดลูป
```python
for x in range(6):
    print(x)
else:
    print("The loop is finished!")
```

หรือจะเป็นการใช้ break แทนเพื่อสิ้นสุดลูปไปเลย
```python
for x in range(5):
    if x == 3: break
    print(x)
else:
    print(f'The loop is finished')
```

### Nested For loop
- ลูปย่อย (inner loop) จะถูกทำงานเพียงครั้งเดียวต่อการวนของลูปใหญ่ (outer loop)
- nested loop คือลูปย่อยที่อยู่ภายใต้ลูปใหญ่อีกที
```python
colors = ["red", "green", "blue"]
fruits = ["apple", "banana", "cherry"]

for x in colors:
    for y in fruits:
        print(x,y)
```