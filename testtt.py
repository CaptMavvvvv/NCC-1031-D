def is_armstrong(number):
  """
  ตรวจสอบว่าตัวเลขที่กำหนดเป็น Armstrong number หรือไม่

  Args:
    number: ตัวเลขจำนวนเต็มที่ต้องการตรวจสอบ

  Returns:
    True หากเป็น Armstrong number, False หากไม่ใช่
  """
  # 1. แปลงตัวเลขเป็นข้อความ (string) เพื่อหาจำนวนหลักและวนลูปผ่านเลขโดด
  s_number = str(number)
  
  # 2. หาจำนวนหลักของตัวเลข
  num_digits = len(s_number)
  
  # 3. สร้างตัวแปรเพื่อเก็บผลรวมเริ่มต้นให้เป็น 0
  armstrong_sum = 0
  
  # 4. วนลูปเพื่อนำเลขโดดแต่ละตัวมายกกำลัง
  for digit in s_number:
    # เพิ่มค่าของ (เลขโดดแปลงเป็น int) ยกกำลัง (จำนวนหลัก) เข้าไปในผลรวม
    armstrong_sum += int(digit) ** num_digits
    
  # 5. เปรียบเทียบผลรวมที่ได้กับตัวเลขดั้งเดิม
  # ถ้าเท่ากันให้คืนค่า True, ไม่เท่ากันคืนค่า False
  return armstrong_sum == number

# --- ตัวอย่างการใช้งาน (Example usage) ---
print(f"153 is an Armstrong number: {is_armstrong(153)}") # Output : True (153 = 1^3 + 5^3 + 3^3)
print(f"9474 is an Armstrong number: {is_armstrong(9474)}") # Output : True (9474 = 9^4 + 4^4 + 7^4 + 4^4)
print(f"123 is an Armstrong number: {is_armstrong(123)}") # Output : False (123 is not an Armstrong number)