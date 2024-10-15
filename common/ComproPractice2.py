from collections import defaultdict

def find_repeated_substrings(s: str) -> list:
    n = len(s)
    substring_count = defaultdict(int)
    substring_index = {}
    
    # สร้างชุดอักขระย่อยทั้งหมดที่มีความยาวตั้งแต่ 2 ตัวอักษรขึ้นไป
    for length in range(2, n + 1):
        for start in range(n - length + 1):
            substr = s[start:start + length]
            substring_count[substr] += 1
            if substr not in substring_index:
                substring_index[substr] = start

    # กรองชุดอักขระย่อยที่ปรากฏมากกว่าหนึ่งครั้ง
    repeated_substrings = [substr for substr, count in substring_count.items() if count > 1]

    # จัดเรียงตามตำแหน่งที่ปรากฏครั้งแรกในสตริง
    sorted_repeated_substrings = sorted(repeated_substrings, key=lambda x: substring_index[x])

    return sorted_repeated_substrings

# ตัวอย่างการใช้งาน
print(find_repeated_substrings("banana")) # Output: ['an', 'ana', 'na']
print(find_repeated_substrings("abcdefg")) # Output: []
print(find_repeated_substrings("abcabcabc")) # Output: ['ab', 'abc', 'abca', 'abcab', 'abcabc', 'bc', 'bca', 'bcab', 'bcabc', 'ca', 'cab', 'cabc']
print(find_repeated_substrings("aaaa")) # Output: ['aa', 'aaa']