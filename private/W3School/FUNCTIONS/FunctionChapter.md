# Python Functions
---

## Functions Characteristic
- __Function เป็นกลุ่มโค้ดที่จะทำงานต่อเมื่อถูกเรียกใช้เท่านั้น__
- __Function สามารถส่งคืนข้อมูลเป็นผลลัพธ์ได้__
- __Function ช่วยลดการเขียนโค้ดที่ซ้ำซ้อน__

### Basic Function Syntax
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

### Return Values
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

#### Numbers of Argument
โดยหลักแล้ว Function จะถูกเรียกใช้ด้วยจำนวน Argument ที่ถูกต้อง
สมมติถ้า Function คาดหวัง 2 Argument เราก็ต้องเรียกใช้ให้ครบทั้ง 2 Argument
```python
def my_function(fname, lname):
    print(fname + "" + lname)
my_function("Adolf", "Hitler")
```