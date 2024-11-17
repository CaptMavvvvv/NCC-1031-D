from collections import defaultdict, Counter

def analyze_purchases(purchases):
    # ใช้เพื่อเก็บจำนวนครั้งที่ลูกค้าซื้อสินค้าซ้ำกันในแต่ละหมวดหมู่
    customer_repeats = defaultdict(lambda: defaultdict(int))
    # ใช้เพื่อเก็บจำนวนครั้งที่สินค้าถูกซื้อในแต่ละหมวดหมู่
    category_counts = defaultdict(Counter)
    
    # วนลูปผ่านแต่ละรายการการซื้อ
    for customer_id, category, product in purchases:
        # นับจำนวนครั้งที่ลูกค้าซื้อสินค้าซ้ำกันในหมวดหมู่นั้น
        customer_repeats[customer_id][category] += 1
        # นับจำนวนครั้งที่สินค้าถูกซื้อในหมวดหมู่นั้น
        category_counts[category][product] += 1
    
    # จัดเตรียมผลลัพธ์สำหรับสินค้าที่ซื้อบ่อยที่สุดในแต่ละหมวดหมู่
    most_frequent = {}
    for category, products in category_counts.items():
        most_common_product = max(products.items(), key=lambda item: (item[1], -ord(item[0][0])))
        most_frequent[category] = most_common_product[0]
    
    # ผลลัพธ์ที่ต้องการ
    result = {
        customer_id: {
            category: count - 1  # เนื่องจากเรานับการซื้อครั้งแรกแล้วจึงต้องลบ 1
            for category, count in categories.items()
            if count > 1  # เก็บเฉพาะหมวดหมู่ที่มีการซื้อซ้ำ
        }
        for customer_id, categories in customer_repeats.items()
    }
    
    result['most_frequent'] = most_frequent
    
    return result

# ตัวอย่างการใช้งาน
purchases = [
    ("cust1", "electronics", "laptop"),
    ("cust2", "groceries", "apple"),
    ("cust1", "electronics", "laptop"),
    ("cust1", "electronics", "mouse"),
    ("cust2", "groceries", "apple"),
    ("cust2", "groceries", "banana"),
    ("cust3", "groceries", "banana"),
    ("cust3", "groceries", "apple"),
    ("cust3", "electronics", "camera"),
]

print(analyze_purchases(purchases))