# Python Functions
---

## Functions Characteristic (คุณลักษณะของ Function)
- __Function เป็นกลุ่มโค้ดที่จะทำงานต่อเมื่อถูกเรียกใช้เท่านั้น__
- __Function สามารถส่งคืนข้อมูลเป็นผลลัพธ์ได้__
- __Function ช่วยลดการเขียนโค้ดที่ซ้ำซ้อน__

### Basic Function Syntax (ไวยากรณ์พื้นฐาน)
> Function มี 'def' เป็นคีย์เวิร์ดหลัก และตามด้วยชื่อ Function และวงเล็บ
```python
def my_function():
    print("Hello from my function")

my_function() # ตรงนี้คือการเรียกใช้ Function
# และสามารถเรียกใช้ได้หลาย ๆ ครั้ง
my_function()
my_function()
```

### ทำไมถึงต้องใช้ Function ?
ลองนึกภาพถ้าอยากจะคำนวณการแปลงหน่วยอุณหภูมิจาก Fahrenheit ไป Celsius มันก็ต้องเขียนคำนวณในทุก ๆ รอบ ซึ่งมันจะเยอะ
```python
temp1 = 77
celsius1 = (temp1 - 32) * 5 / 9
print(celsius1)

temp2 = 95
celsius2 = (temp2 - 32) * 5 / 9
print(celsius2)

temp3 = 50
celsius3 = (temp3 - 32) * 5 / 9
print(celsius3)
```

เมื่อเราใช้ Function มันก็จะออกมาหน้าตาอย่างงี้
```python
def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95)) # เหล่านี้คือการนำ Function มาใช้ในการคำนวณอุณหภูมิ
print(fahrenheit_to_celsius(60))
```

### Return Values (การคืนค่ากลับ)
Func จะสามารถส่งค่าคืนกลับมายังโค้ดโดยการใช้คำสั่ง return 
```python
def get_greeting():
    return "Hello from a function"
message = get_greeting()
print(message)
```

### Parameter and Argument 
Arguments คือข้อมูลจริงที่ถูกส่งเข้าไปใน __ตอนเรียกใช้งานฟังก์ชัน__
- สามารถส่งข้อมูลเข้าไปใน Function ได้โดยการใช้ Parameter
- Parameter จะถูกระบุไว้หลังชื่อ Function และอยู่ในวงเล็บอีกที ซึ่งเราสามารถเพิ่ม Parameter ได้มากตามต้องการ เพียงแค่คั่นด้วย comma ( , )

ตัวอย่างต่อไปนี้จะมี Parameter 1 ตัว (fname)
```python
def my_function(fname): # fname = parameter
    print(fname + "Refsnes")
my_function("Emil") # Emil = argument
my_function("Tobias") # Tobias = argument
my_function("Linus") # Linus = argument
# Output :
'''
EmilRefsnes
TobiasRefsnes
LinusRefsnes
'''
```

#### Numbers of Argument (จำนวนของ Arg)
โดยหลักแล้ว Function จะถูกเรียกใช้ด้วยจำนวน Argument ที่ถูกต้อง
สมมติถ้า Function คาดหวัง 2 Argument เราก็ต้องเรียกใช้ให้ครบทั้ง 2 Argument
```python
def my_function(fname, lname):
    print(fname + "" + lname)
my_function("Adolf", "Hitler")
```

ถ้าเกิด Function รับได้เพียงแค่ 1 ค่า ทั้งๆ ที่ควรจะได้ 2 (fname, lname) จะโดนข้อความ error
```python
def my_function(fname, lname):
    print(fname + "" + lname)
my_function("Adolf") # Error
```

#### Dafault Parameter Values
เราสามารถกำหนดค่าตั้งต้นของ Parameter ไว้ได้ ซึ่งกรณีที่ Function ถูกเรียกใช้โดยที่ไม่มี Argument มันก็จะใช้ Default Values หรือค่าตั้งต้นของ Parameter
```python
def my_function(name = "friend"):
    print("Hello", name)
my_function("Adolf") # Hello Adolf
my_function("Stalin") # Hello Stalin
my_function() # Hello friend
my_function("Truman") # Hello Truman
```

#### Keyword Arguments
เราสามารถส่ง Argument ได้ด้วยไวยากรณ์แบบ key = value
```python
def my_function(animal, name):
    print("I have a", animal)
    print(f"My {animal} 's name is {name}")
my_function(animal = "dog", name = "Buddy") 
"""Output = 
I have a dog
My dog's name is Buddy"""
```

#### Positional Arguments (การเรียก Arg ตามตำแหน่ง)
เมื่อเราเรียกใช้ Function ที่มี Argument แต่ไม่มีการใช้ keyword, Argument แบบนั้นจะเรียกว่า Positional Arguments หรือการเรียกตามตำแหน่ง
__Reminder__ : Postional Arg จะต้องถูกเรียงตามลำดับที่ถูกต้อง
```python
def my_function(animal, name):
    print("I have a", animal)
    print(f"My {animal} 's name is {name}")
my_function("dog", "Buddy") # animal = dog, name = Buddy
```

#### การนำ Positional กับ Keyword Arguments มาใช้คู่กัน
เราสามารถนำสองสิ่งมาใช้รวมกันได้ โดยที่ __Positional__ ต้องมาก่อน __Keyword__ เสมอ
```python
def my_function(animal,name, age):
    print(f'I have a {age} year old {animal} named {name}')
my_function("dog", name = "buddy", age = 5)
```

#### Passing Different Data Type (การส่งผ่านข้อมูลประเภทต่าง ๆ)
เราสามารถส่งข้อมูลประเภทใดก็ได้เป็น Argument ให้กับ Function เช่น String, Number, List, Dictionary, ฯลฯ โดยที่ประเภทข้อมูลจะถูกรักษาไว้ภายในฟังก์ชัน
```python
def my_function(fruits): # ส่ง List เป็น Arg
    for fruit in fruits:
        print(fruit)
my_fruits = ["apple", "banana", "cherry"]
my_function(my_fruits)
```

```python
def my_function(person): # ส่ง Dict เป็น Arg
    print("Name": person["name"])
    print("Age": person["age"])
my_person = {"name": "Emil", "age": 25}
my_function(my_person)
```

