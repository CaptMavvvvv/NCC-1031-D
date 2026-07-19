# Python Match
---

## Match Characteristic
__แทนที่จะเขียน If Else หลาย ๆ อัน เราสามารถเขียน Match Statement แทนได้__
> the 'match' statement selects one of many code blocks to be executed
```python
match expression:
  case x:
    code block
  case y:
    code block
  case z:
    code block
```

__วิธีการทำงานของ Match__
* The match expression is evaluated once.
* The value of the expression is compared with the values of each case.
* If there is a match, the associated block of code is executed.

ตัวอย่างการใช้งาย
1. Basic Syntax
   รูปแบบการเขียนจะประกอบด้วยคีย์เวิร์ด match ตามด้วยตัวแปรที่ต้องการเช็ค และใช้ case สำหรับระบุเงื่อนไขต่าง ๆ ส่วนเครื่องหมาย _ (Underscore) จะทำหน้าที่เหมือน default หรือ else (ถ้าไม่ตรงกับ case ไหนเลย จะตกมาที่นี่)
```python
def check_status(status_code):
    match status_code:
        case 200:
            return "OK"
        case 404:
            return "NOT FOUND"
        case 500:
            return "Internal Server Error"
        case _: # Default Case (ทำงานเหมือน Else)
            return "Unknown Status"
print(check_status(200)) # Output : OK
print(check_status(999)) # Output : Unknown Status
```

2. การใช้เครื่องหมาย OR ( | ) ใน Case เดียวกัน
   เราสามารถยุบรวมหลาย ๆ ค่าที่ต้องการให้ผลลัพธ์เหมือนกัน มารวมอยู่ใน case เดียวกันได้โดยใช้เครื่องหมาย | (Pipe)
```python
def get_device_type(brand):
    match brand:
        case "Apple" | "Samsung" | "Oppo" :
            return "Smartphone"
        case "Dell" | "HP" | "Lenovo" :
            return "Laptop"
        case _ :
            return "Unknown Device"
```

3. การเช็คโครงสร้างข้อมูล (Structural Matching)
   สามารถแกะและตรวจสอบไส้ในของข้อมูลประเภท List, Tuple หรือ Dictionary ได้ทันที
```python
def procress_command(command):
    match command:
        case ["quit"]:
            print("GOODBYE ! ")
        case ["move", direction]: # เช็คว่าถ้าเป็น List ที่มี 2 ตัวชิ้น และตัวแรกคำว่า move
            print(f'Moving to the direction: {direction}')
        case ["teleport", x, y]: # ดึงค่า x และ y ออกมาจาก List มาใช้งานต่อได้เลย
            print(f'Teleporting to : X:{x}, Y:{y}')
        case _ :
            print("Unknown Command")
process_command(["move", "south"])
process_command(["teleport", 10, 20])
```

4. การใส่เงื่อนไขเพิ่มเติมด้วย if (Guards)
   ในแต่ละ case เราสามารถใส่เงื่อนไข if เพิ่มเข้าไปเพื่อสกรีนข้อมูลให้ละเอียดขึ้นได้ เรียกว่า Guard 
```python
def process_age(user_info):
    match user_info:
        case (name, age) if age < 10:
            print(f'{name} is a minor.')
        case (name, age):
            print(f'{name} is a adult.')
process_age(('Alice', 15))
```

