def find_single_occurrence_numbers(numbers: list) -> list:
    from collections import defaultdict

    # ใช้ defaultdict เพื่อนับจำนวนการเกิดขึ้นของแต่ละค่า
    count = defaultdict(int)
    
    # ใช้เซ็ตเพื่อติดตามค่าที่มีการปรากฏมากกว่าหนึ่งครั้ง
    multiple_occurrences = set()
    
    # นับจำนวนการเกิดขึ้นของแต่ละค่า
    for number in numbers:
        count[number] += 1
    
    # ตรวจสอบค่าที่มีการปรากฏมากกว่าหนึ่งครั้ง
    for number in count:
        if count[number] > 1:
            multiple_occurrences.add(number)
    
    # กรองค่าที่ปรากฏเพียงครั้งเดียวตามลำดับการปรากฏในรายการต้นฉบับ
    single_occurrences = [number for number in numbers if count[number] == 1]
    
    # กรองค่าที่มีการปรากฏมากกว่าหนึ่งครั้งออก
    result = [number for number in single_occurrences if number not in multiple_occurrences]
    
    return result

# ตัวอย่างการใช้งาน
print(find_single_occurrence_numbers([4, 5, 6, 4, 7, 5, 8]))  # Output: [6, 7, 8]
print(find_single_occurrence_numbers([1, 2, 2, 3, 3, 4, 4]))  # Output: [1]
print(find_single_occurrence_numbers([1, 2, 3, 4, 5, 6]))      # Output: [1, 2, 3, 4, 5, 6]
print(find_single_occurrence_numbers([1, 1, 1, 1, 1]))          # Output: []