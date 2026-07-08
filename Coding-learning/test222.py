def generate_primes(n):
  """
  สร้างรายการของจำนวนเฉพาะทั้งหมดที่ไม่เกิน n
  โดยใช้วิธี 'Sieve of Eratosthenes'

  Args:
    n: เลขจำนวนเต็มที่เป็นขอบเขตบน (inclusive)

  Returns:
    ข้อความ (string) ที่แสดงจำนวนเฉพาะที่คั่นด้วย ", "
  """
  # กรณีที่ n น้อยกว่า 2 จะไม่มีจำนวนเฉพาะเลย
  if n < 2:
    return ""

  # สร้าง list เพื่อตรวจสอบว่าเลขแต่ละตัวเป็นจำนวนเฉพาะหรือไม่
  # ตั้งค่าเริ่มต้นให้ทุกตัวเป็น True
  is_prime = [True] * (n + 1)
  is_prime[0] = is_prime[1] = False # 0 และ 1 ไม่ใช่จำนวนเฉพาะ

  # เริ่มจาก 2 ซึ่งเป็นจำนวนเฉพาะตัวแรก
  for p in range(2, int(n**0.5) + 1):
    # ถ้า p ยังเป็นจำนวนเฉพาะ (ยังเป็น True)
    if is_prime[p]:
      # ให้คัดเลขที่เป็นผลคูณของ p ทั้งหมดออก (ตั้งค่าเป็น False)
      # โดยเริ่มจาก p*p เพราะตัวที่น้อยกว่านั้นจะถูกคัดออกไปแล้ว
      for multiple in range(p * p, n + 1, p):
        is_prime[multiple] = False

  # รวบรวมจำนวนเฉพาะทั้งหมดที่ยังเป็น True อยู่
  prime_numbers = []
  for i in range(2, n + 1):
    if is_prime[i]:
      prime_numbers.append(str(i)) # แปลงเป็น string เพื่อใช้ join

  # เชื่อม list ของตัวเลขด้วย ", " ให้เป็น string เดียว
  return ", ".join(prime_numbers)

# --- ตัวอย่างการใช้งาน (Example usage) ---
print(f'Primes up to 10: "{generate_primes(10)}"')
print(f'Primes up to 20: "{generate_primes(20)}"')
print(f'Primes up to 1: "{generate_primes(1)}"')
print(f'Primes up to 2: "{generate_primes(2)}"')