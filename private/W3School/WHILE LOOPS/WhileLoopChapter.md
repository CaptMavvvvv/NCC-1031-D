# Python While Loops
---

## While loop Characteristic
__While Loop เป็นลูปประเภท 'Condition-Controlled Loop' หรือลูปที่จะทำงานตามเงื่อนไข เงื่อนไขเป็นจริงก็ทำงานตามลูปจนกว่าเงื่อนไขจะเป็นเท็จ__

### Basic While Loop
> การทำงานจะเกิดขึ้นเมื่อเงื่อนไขเป็นจริงเท่านั้น
```python
i = 1
while i < 6: # ตราบใดที่ i ยังน้อยกว่า 6 ลูปก็จะถูกรัน
    print(i)
    i += 1 # เพิ่มค่าของ i ขึ้นทีละหนึ่ง
```

### Break Statement
> 'Break' สามารถทำให้หลุดออกจากลูปได้ แม้ว่าเงื่อนไขจะยังเป็นจริงอยู่ก็ตาม
```python
i = 1
while i < 6:
    print(i)
    if i == 3: # ถ้า i มีค่าเท่ากับ 3 เมื่อไหร่ ให้ break ออกจากลูป
        break
    i += 1
```

### Continue Statement
> 'Continue' สามารถให้เราหยุดการลูปในปัจจุบัน และทำคำสั่งถัดไปได้
```python
i = 0
while i < 6:
    i += 1
    if i == 3: # ถ้า i มีค่าเท่ากับ 3 ให้ทำคำสั่งถัดไปต่อ
        continue
    print(i) # Note: Output จะมีแค่ 1 2 4 5 6 ข้าม 3 ไป
```

### Else Statement
> 'Else' ทำให้เราสามารถใช้ Code Block นั้น ๆ ได้เพียงครั้งเดียว เมื่อเงื่อนไขไม่เป็นจริงอีกต่อไป
```python
i = 0
while i < 10:
    print(i)
    i += 1
else:
    print(f'i is no longer less than 10')
```