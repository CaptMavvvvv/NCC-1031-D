# Python If ... Else

---

## If Else conditions and statement
> เท่ากับ: a == b
> ไม่เท่ากับ: a != b
> น้อยกว่า: a < b
> น้อยกว่าหรือเท่ากับ: a <= b
> มากกว่า: a > b
> มากกว่าหรือเท่ากับ: a >= b


### Shorthand IF
__Shorthand if คือการเขียนเงื่อนไข if else ในรูปแบบที่ย่อให้โค้ดมาอยู่กันในบรรทัดเดียวกัน__
ตัวอย่างเช่น

_รูปย่อของ if_ 
```python
a = 5
b = 2
if a > b: print(f'a is greater than b')
```


_รูปย่อของ if else_
```python
score = 75
result = "Pass" if score >= 50 else "Fail"
print(result) #
```

_กำหนดค่าด้วย if else_
```python
a = 10
b = 20
bigger = a if a > b else b
print(f'Bigger is {bigger}')
```

*__ไวยากรณ์ของส่วน 'กำหนดค่าด้วย if else'__*
```python 
ตัวแปร = ผลลัพธ์ถ้าเป็นจริง if เงื่อนไข else ผลลัพธ์ถ้าเป็นเท็จ
```

_หลายเงื่อนไชในบรรทัดเดียว_
```python
a = 330
b = 330
print("A") if a > b else print("=") if a == b else print("B")
```

```python
score = 75
result = "Pass" if score >= 50 else "Fail"
print(result)
```

### Logical Operator
> and - คืนค่าต่อเมื่อค่าทั้งคู่เป็นจริง
> or - คืนค่าต่อเมื่อค่าใดค่าหนึ่งเป็นจริง
> not - ย้อนผลลัพธ์ จะคืนค่าที่เป็นเท็จหากค่าที่ออกมาเป็นจริง


### Nested If
```python
age = 25
has_license = True
if age >= 18: # เริ่มเช็คเงื่อนไขของ age
  if has_license: # เช็คเงื่อนไขของ license
    print("You can drive")
  else:
    print("You need a license")
else: # สิ้นสุดการเช็คเงื่อนไขของ age
  print("You are too young to drive")
```

__Nested If with Logical Operator__
```python
temperature = 25
is_sunny = True
if temperature > 20 and is_sunny:
  print("Perfect beach weather!")
```