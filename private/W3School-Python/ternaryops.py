user_input = int(input('Please enter number: '))
result = "Monday" if user_input == 1 else "Tuesday" if user_input == 2 else "Wednesday" if user_input == 3 else "Weekend"
print(result) 

''' หลักการคือ ในช่อง Result ตรวจค่าไปเรื่อย ๆ เหมือนจับเอาเงื่อนไข Else if มาใช้แต่อยู่ในรูปแบบเช็คไปในตัวแปรเลย 
    ตัวแปร = "ผลลัพธ์แรก" ถ้าเงื่อนไขเป็นจริง หรือ varieble = "result" if 'condition' == true 
    แต่ต้องมี else ปิดท้าย ไม่งั้นมันจะไม่ครบเงื่อนไขของ if '''

# !
# ?
# //
# todo
# *