def find_pairs_with_product(nums: list, target: int) -> list:
    result = [] # สร้างตัวแปรสำหรับเก็บค่าผลลัพธ์
    n = len(nums) # กำหนด n ให้เก็บการนับค่าทั้งหมดของ nums ไว้
    for i in range(n): # รันลูปตามระยะของ n เพื่อหาค่าตำแหน่งแรก
        for j in range(i+1, n): # รันลูปหาตำแหน่งที่สอง
            if nums[i] * nums[j] == target: # ถ้าตำแหน่งแรก * ตำแหน่งสอง == เป้าหมาย
                result.append([nums[i], nums[j]]) 
    return result

print(find_pairs_with_product([1,2,3,4,6], 6))
#Output: [[1,6], [2,3]]
print(find_pairs_with_product([2,4,5,7], 14))
#Output: [[2,7]
print(find_pairs_with_product([3,5,9,10], 25))
#Output: []
print(find_pairs_with_product([1,2,3,4,5], 20))
#Output: [[4,5]]